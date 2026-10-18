"""Employment router — employers CRUD + add job + end job.

Routes:
  GET       /employment                    overview (current jobs + employers tabs)
  GET/POST  /employment/employers          list + add
  GET/POST  /employment/employers/{id}/edit
  GET/POST  /employment/new?student_id=    add job to a student
  GET/POST  /employment/{id}/end           end a current job

All routes require employment.manage permission.
Current-job definition: start_date <= today AND (end_date IS NULL OR end_date >= today).
"""
import datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app import audit
from app.db import get_db
from app.models import Employer, Employment, Student, UserAccount
from app.security import check_csrf, get_user_permissions, require_permission
from app.templates_env import templates

router = APIRouter(prefix="/employment", tags=["employment"])
_manage_dep = require_permission("employment.manage")

# US state abbreviations (reused from students form pattern)
_US_STATES = [
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA",
    "KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
    "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT",
    "VA","WA","WV","WI","WY","DC",
]

JOB_TYPES = ["part_time", "full_time", "other", "unknown"]


# ---------------------------------------------------------------------------
# /employment overview — current jobs + employers
# ---------------------------------------------------------------------------

@router.get("", response_class=HTMLResponse)
async def employment_overview(
    request: Request,
    tab: str = "jobs",
    current_user: UserAccount = Depends(_manage_dep),
    db: Session = Depends(get_db),
):
    """Overview page: 'Current jobs' tab and 'Employers' tab."""
    today = datetime.date.today()

    # Current jobs: start_date <= today AND (end_date IS NULL OR end_date > today)
    raw_jobs = (
        db.query(Employment, Student, Employer)
        .join(Student, Student.id == Employment.student_id)
        .join(Employer, Employer.id == Employment.employer_id)
        .filter(
            Employment.start_date <= today,
            (Employment.end_date == None) | (Employment.end_date > today),  # noqa: E711
        )
        .order_by(Student.last_name, Student.first_name)
        .all()
    )
    current_jobs = [
        {
            "employment": job,
            "student": student,
            "employer": employer,
        }
        for job, student, employer in raw_jobs
    ]

    employers = db.query(Employer).filter(Employer.active == True).order_by(Employer.name).all()  # noqa: E712

    active_tab = tab if tab in ("jobs", "employers") else "jobs"

    return templates.TemplateResponse(
        request,
        "employment/overview.html",
        {
            **_ctx(current_user, db),
            "current_jobs": current_jobs,
            "employers": employers,
            "active_tab": active_tab,
        },
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ctx(current_user: UserAccount, db: Session) -> dict:
    return {
        "current_user": current_user,
        "user_perms": get_user_permissions(current_user, db),
    }


def _validate_employer(name: str) -> list[str]:
    errors = []
    if not name.strip():
        errors.append("Employer name is required.")
    return errors


def _parse_date(value: str) -> datetime.date | None:
    """Parse YYYY-MM-DD string; return None if blank."""
    value = value.strip()
    if not value:
        return None
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        return None  # caller will catch None where required


def _validate_job(
    employer_id: str,
    job_title: str,
    job_type: str,
    start_date_str: str,
    end_date_str: str,
    hours_str: str,
) -> tuple[list[str], datetime.date | None, datetime.date | None]:
    """Validate job form fields; return (errors, start_date, end_date)."""
    errors: list[str] = []

    if not employer_id:
        errors.append("Employer is required.")
    if not job_title.strip():
        errors.append("Job title is required.")
    if job_type not in JOB_TYPES:
        errors.append("Invalid job type.")

    start_date = _parse_date(start_date_str)
    if not start_date:
        errors.append("Start date is required and must be YYYY-MM-DD.")

    end_date = _parse_date(end_date_str)
    if end_date and start_date and end_date < start_date:
        errors.append("End date cannot be before start date.")

    if hours_str.strip():
        try:
            h = int(hours_str.strip())
            if h < 0:
                errors.append("Hours per week cannot be negative.")
        except ValueError:
            errors.append("Hours per week must be a whole number.")

    return errors, start_date, end_date


# ---------------------------------------------------------------------------
# Employers — list
# ---------------------------------------------------------------------------

@router.get("/employers", response_class=HTMLResponse)
async def employers_list(
    request: Request,
    current_user: UserAccount = Depends(_manage_dep),
    db: Session = Depends(get_db),
):
    employers = db.query(Employer).filter(Employer.active == True).order_by(Employer.name).all()  # noqa: E712
    return templates.TemplateResponse(
        request,
        "employment/employers_list.html",
        {**_ctx(current_user, db), "employers": employers},
    )


# ---------------------------------------------------------------------------
# Employers — new
# ---------------------------------------------------------------------------

@router.get("/employers/new", response_class=HTMLResponse)
async def employer_new_form(
    request: Request,
    current_user: UserAccount = Depends(_manage_dep),
    db: Session = Depends(get_db),
):
    return templates.TemplateResponse(
        request,
        "employment/employer_form.html",
        {**_ctx(current_user, db), "employer": None, "errors": [], "vals": {},
         "us_states": _US_STATES},
    )


@router.post("/employers/new", response_class=HTMLResponse)
async def employer_new_save(
    request: Request,
    csrf_token: str = Form(""),
    name: str = Form(""),
    address: str = Form(""),
    city: str = Form(""),
    state: str = Form(""),
    zip: str = Form(""),
    phone: str = Form(""),
    company_type: str = Form(""),
    current_user: UserAccount = Depends(_manage_dep),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf_token)
    vals = {"name": name, "address": address, "city": city,
            "state": state, "zip": zip, "phone": phone, "company_type": company_type}
    errors = _validate_employer(name)
    if errors:
        return templates.TemplateResponse(
            request,
            "employment/employer_form.html",
            {**_ctx(current_user, db), "employer": None, "errors": errors,
             "vals": vals, "us_states": _US_STATES},
            status_code=422,
        )
    employer = Employer(
        name=name.strip(),
        address=address.strip() or None,
        city=city.strip() or None,
        state=state.strip() or None,
        zip=zip.strip() or None,
        phone=phone.strip() or None,
        company_type=company_type.strip() or None,
        active=True,
    )
    db.add(employer)
    db.commit()
    db.refresh(employer)
    audit.log_event(db, current_user.id, "employer_create", "employer", employer.id,
                    {"name": employer.name})
    return RedirectResponse("/employment/employers", status_code=303)


# ---------------------------------------------------------------------------
# Employers — edit
# ---------------------------------------------------------------------------

@router.get("/employers/{employer_id}/edit", response_class=HTMLResponse)
async def employer_edit_form(
    employer_id: int,
    request: Request,
    current_user: UserAccount = Depends(_manage_dep),
    db: Session = Depends(get_db),
):
    employer = db.get(Employer, employer_id)
    if employer is None:
        return HTMLResponse("Employer not found", status_code=404)
    return templates.TemplateResponse(
        request,
        "employment/employer_form.html",
        {**_ctx(current_user, db), "employer": employer, "errors": [], "vals": {},
         "us_states": _US_STATES},
    )


@router.post("/employers/{employer_id}/edit", response_class=HTMLResponse)
async def employer_edit_save(
    employer_id: int,
    request: Request,
    csrf_token: str = Form(""),
    name: str = Form(""),
    address: str = Form(""),
    city: str = Form(""),
    state: str = Form(""),
    zip: str = Form(""),
    phone: str = Form(""),
    company_type: str = Form(""),
    current_user: UserAccount = Depends(_manage_dep),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf_token)
    employer = db.get(Employer, employer_id)
    if employer is None:
        return HTMLResponse("Employer not found", status_code=404)
    vals = {"name": name, "address": address, "city": city,
            "state": state, "zip": zip, "phone": phone, "company_type": company_type}
    errors = _validate_employer(name)
    if errors:
        return templates.TemplateResponse(
            request,
            "employment/employer_form.html",
            {**_ctx(current_user, db), "employer": employer, "errors": errors,
             "vals": vals, "us_states": _US_STATES},
            status_code=422,
        )
    employer.name = name.strip()
    employer.address = address.strip() or None
    employer.city = city.strip() or None
    employer.state = state.strip() or None
    employer.zip = zip.strip() or None
    employer.phone = phone.strip() or None
    employer.company_type = company_type.strip() or None
    db.commit()
    audit.log_event(db, current_user.id, "employer_edit", "employer", employer.id,
                    {"name": employer.name})
    return RedirectResponse("/employment/employers", status_code=303)


# ---------------------------------------------------------------------------
# Add job (from student detail → /employment/new?student_id=)
# ---------------------------------------------------------------------------

@router.get("/new", response_class=HTMLResponse)
async def job_new_form(
    request: Request,
    student_id: int = 0,
    current_user: UserAccount = Depends(_manage_dep),
    db: Session = Depends(get_db),
):
    student = db.get(Student, student_id) if student_id else None
    if student is None:
        return HTMLResponse("Student not found", status_code=404)
    employers = db.query(Employer).filter_by(active=True).order_by(Employer.name).all()
    return templates.TemplateResponse(
        request,
        "employment/job_form.html",
        {
            **_ctx(current_user, db),
            "student": student,
            "employers": employers,
            "job_types": JOB_TYPES,
            "employment": None,
            "errors": [],
            "vals": {},
        },
    )


@router.post("/new", response_class=HTMLResponse)
async def job_new_save(
    request: Request,
    csrf_token: str = Form(""),
    student_id: int = Form(0),
    employer_id: str = Form(""),
    job_title: str = Form(""),
    job_type: str = Form("unknown"),
    hours_per_week: str = Form(""),
    start_date: str = Form(""),
    end_date: str = Form(""),
    supervisor: str = Form(""),
    hourly_rate: str = Form(""),
    current_user: UserAccount = Depends(_manage_dep),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf_token)
    student = db.get(Student, student_id) if student_id else None
    if student is None:
        return HTMLResponse("Student not found", status_code=404)
    employers = db.query(Employer).filter_by(active=True).order_by(Employer.name).all()

    vals = {
        "employer_id": employer_id, "job_title": job_title, "job_type": job_type,
        "hours_per_week": hours_per_week, "start_date": start_date,
        "end_date": end_date, "supervisor": supervisor, "hourly_rate": hourly_rate,
    }

    errors, start_dt, end_dt = _validate_job(
        employer_id, job_title, job_type, start_date, end_date, hours_per_week
    )

    if errors:
        return templates.TemplateResponse(
            request,
            "employment/job_form.html",
            {
                **_ctx(current_user, db),
                "student": student,
                "employers": employers,
                "job_types": JOB_TYPES,
                "employment": None,
                "errors": errors,
                "vals": vals,
            },
            status_code=422,
        )

    hours_int = int(hours_per_week.strip()) if hours_per_week.strip() else None
    rate = None
    if hourly_rate.strip():
        try:
            from decimal import Decimal
            rate = Decimal(hourly_rate.strip().replace("$", "").replace(",", ""))
        except Exception:
            pass

    job = Employment(
        student_id=student.id,
        employer_id=int(employer_id),
        job_title=job_title.strip(),
        job_type=job_type,
        hours_per_week=hours_int,
        start_date=start_dt,
        end_date=end_dt,
        supervisor=supervisor.strip() or None,
        hourly_rate=rate,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    employer_obj = db.get(Employer, job.employer_id)
    audit.log_event(db, current_user.id, "job_add", "employment", job.id,
                    {
                        "student_id": student.id,
                        "student_name": f"{student.first_name} {student.last_name}",
                        "employer_id": job.employer_id,
                        "employer_name": employer_obj.name if employer_obj else "",
                    })
    return RedirectResponse(f"/students/{student.id}", status_code=303)


# ---------------------------------------------------------------------------
# End job
# ---------------------------------------------------------------------------

@router.get("/{employment_id}/end", response_class=HTMLResponse)
async def end_job_form(
    employment_id: int,
    request: Request,
    current_user: UserAccount = Depends(_manage_dep),
    db: Session = Depends(get_db),
):
    job = db.get(Employment, employment_id)
    if job is None:
        return HTMLResponse("Employment record not found", status_code=404)
    if job.end_date is not None:
        return HTMLResponse("Job already ended", status_code=400)
    student = db.get(Student, job.student_id)
    employer = db.get(Employer, job.employer_id)
    return templates.TemplateResponse(
        request,
        "employment/end_job_form.html",
        {
            **_ctx(current_user, db),
            "job": job,
            "student": student,
            "employer": employer,
            "errors": [],
            "today": datetime.date.today().isoformat(),
        },
    )


@router.post("/{employment_id}/end", response_class=HTMLResponse)
async def end_job_save(
    employment_id: int,
    request: Request,
    csrf_token: str = Form(""),
    end_date: str = Form(""),
    current_user: UserAccount = Depends(_manage_dep),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf_token)
    job = db.get(Employment, employment_id)
    if job is None:
        return HTMLResponse("Employment record not found", status_code=404)
    if job.end_date is not None:
        return HTMLResponse("Job already ended", status_code=400)
    student = db.get(Student, job.student_id)
    employer = db.get(Employer, job.employer_id)

    end_dt = _parse_date(end_date)
    errors = []
    if not end_dt:
        errors.append("End date is required and must be YYYY-MM-DD.")
    elif end_dt < job.start_date:
        errors.append("End date cannot be before the job start date "
                      f"({job.start_date}).")

    if errors:
        return templates.TemplateResponse(
            request,
            "employment/end_job_form.html",
            {
                **_ctx(current_user, db),
                "job": job,
                "student": student,
                "employer": employer,
                "errors": errors,
            },
            status_code=422,
        )

    job.end_date = end_dt
    job.version = (job.version or 1) + 1
    db.commit()
    audit.log_event(db, current_user.id, "job_end", "employment", job.id,
                    {
                        "end_date": str(end_dt),
                        "student_name": f"{student.first_name} {student.last_name}",
                        "employer_name": employer.name if employer else "",
                    })
    return RedirectResponse(f"/students/{job.student_id}", status_code=303)
