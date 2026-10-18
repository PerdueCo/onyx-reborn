"""Students router — list, create, edit, detail."""
import datetime
import re

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app import audit
from app.db import get_db
from app.models import Employer, Employment, Program, Student, UserAccount
from app.security import check_csrf, get_user_permissions, require_permission
from app.services.kpis import is_current_job
from app.templates_env import templates

router = APIRouter(prefix="/students", tags=["students"])
_read_dep = require_permission("students.read")
_manage_dep = require_permission("students.manage")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_PHONE_RE = re.compile(r"^\(\d{3}\) \d{3}-\d{4}$")


def _phone_ok(value: str) -> bool:
    """Return True if value matches (555) 555-0101 format or is blank."""
    return not value or bool(_PHONE_RE.match(value.strip()))


def _next_student_number(db: Session) -> str:
    """Generate STU-#### sequential number."""
    last = (
        db.query(Student)
        .filter(Student.student_number.like("STU-%"))
        .order_by(Student.id.desc())
        .first()
    )
    if last:
        try:
            n = int(last.student_number.split("-")[1]) + 1
        except (IndexError, ValueError):
            n = 1
    else:
        n = 1
    return f"STU-{n:04d}"


def _seed_programs(db: Session):
    """Ensure the 5 default programs exist."""
    defaults = [
        ("CIS101", "Computer Information Systems"),
        ("ACC110", "Accounting"),
        ("BUS201", "Business Administration"),
        ("MKT130", "Marketing"),
        ("OFT120", "Office Technology"),
    ]
    for code, name in defaults:
        if not db.query(Program).filter_by(code=code).first():
            db.add(Program(code=code, name=name, active=True))
    db.commit()


def _validate_form(
    first_name: str,
    last_name: str,
    home_phone: str,
    work_phone: str = "",
) -> list[str]:
    """Return a list of error messages (empty = valid)."""
    errors = []
    if not first_name.strip():
        errors.append("First name is required.")
    if not last_name.strip():
        errors.append("Last name is required.")
    if home_phone and not _phone_ok(home_phone):
        errors.append("Home phone must be in (555) 555-0101 format.")
    if work_phone and not _phone_ok(work_phone):
        errors.append("Work phone must be in (555) 555-0101 format.")
    return errors


def _ctx(current_user: UserAccount, db: Session) -> dict:
    """Common template context keys."""
    return {
        "current_user": current_user,
        "user_perms": get_user_permissions(current_user, db),
    }


# ---------------------------------------------------------------------------
# List
# ---------------------------------------------------------------------------

@router.get("", response_class=HTMLResponse)
async def student_list(
    request: Request,
    q: str = "",
    current_user: UserAccount = Depends(_read_dep),
    db: Session = Depends(get_db),
):
    _seed_programs(db)
    query = db.query(Student)
    if q:
        like = f"%{q}%"
        query = query.filter(
            Student.first_name.ilike(like)
            | Student.last_name.ilike(like)
            | (Student.first_name + " " + Student.last_name).ilike(like)
            | Student.student_number.ilike(like)
        )
    students = query.order_by(Student.last_name, Student.first_name).all()
    programs = {p.id: p for p in db.query(Program).all()}
    return templates.TemplateResponse(
        request,
        "students/list.html",
        {
            **_ctx(current_user, db),
            "students": students,
            "programs": programs,
            "q": q,
        },
    )


# ---------------------------------------------------------------------------
# New
# ---------------------------------------------------------------------------

@router.get("/new", response_class=HTMLResponse)
async def student_new_form(
    request: Request,
    current_user: UserAccount = Depends(_manage_dep),
    db: Session = Depends(get_db),
):
    _seed_programs(db)
    programs = db.query(Program).filter_by(active=True).order_by(Program.name).all()
    return templates.TemplateResponse(
        request,
        "students/form.html",
        {
            **_ctx(current_user, db),
            "student": None,
            "programs": programs,
            "errors": [],
            "duplicate": None,
            "vals": {},
        },
    )


@router.post("/new", response_class=HTMLResponse)
async def student_new_save(
    request: Request,
    csrf_token: str = Form(""),
    first_name: str = Form(""),
    last_name: str = Form(""),
    program_id: str = Form(""),
    status: str = Form("active"),
    email: str = Form(""),
    home_phone: str = Form(""),
    work_phone: str = Form(""),
    address: str = Form(""),
    city: str = Form(""),
    state: str = Form(""),
    zip: str = Form(""),
    high_school: str = Form(""),
    seeking_employment: str = Form(""),
    desired_job: str = Form(""),
    current_user: UserAccount = Depends(_manage_dep),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf_token)
    _seed_programs(db)
    programs = db.query(Program).filter_by(active=True).order_by(Program.name).all()
    vals = {
        "first_name": first_name, "last_name": last_name,
        "program_id": program_id, "status": status,
        "email": email, "home_phone": home_phone, "work_phone": work_phone,
        "address": address, "city": city, "state": state, "zip": zip,
        "high_school": high_school, "seeking_employment": seeking_employment,
        "desired_job": desired_job,
    }
    errors = _validate_form(first_name, last_name, home_phone, work_phone)

    # Duplicate check
    duplicate = None
    if not errors and home_phone:
        dup = (
            db.query(Student)
            .filter(
                Student.first_name.ilike(first_name.strip()),
                Student.last_name.ilike(last_name.strip()),
                Student.home_phone == home_phone.strip(),
            )
            .first()
        )
        if dup:
            duplicate = dup  # warn but allow save

    if errors:
        return templates.TemplateResponse(
            request,
            "students/form.html",
            {
                **_ctx(current_user, db),
                "student": None,
                "programs": programs,
                "errors": errors,
                "duplicate": duplicate,
                "vals": vals,
            },
            status_code=422,
        )

    student = Student(
        student_number=_next_student_number(db),
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        program_id=int(program_id) if program_id else None,
        status=status or "active",
        email=email.strip() or None,
        home_phone=home_phone.strip() or None,
        work_phone=work_phone.strip() or None,
        address=address.strip() or None,
        city=city.strip() or None,
        state=state.strip() or None,
        zip=zip.strip() or None,
        high_school=high_school.strip() or None,
        seeking_employment=(seeking_employment == "yes") if seeking_employment else None,
        desired_job=desired_job.strip() or None,
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    audit.log_event(db, current_user.id, "student_create", "student", student.id,
                    {
                        "student_number": student.student_number,
                        "student_name": f"{student.first_name} {student.last_name}",
                    })
    return RedirectResponse(f"/students/{student.id}", status_code=303)


# ---------------------------------------------------------------------------
# Edit
# ---------------------------------------------------------------------------

@router.get("/{student_id}/edit", response_class=HTMLResponse)
async def student_edit_form(
    student_id: int,
    request: Request,
    current_user: UserAccount = Depends(_manage_dep),
    db: Session = Depends(get_db),
):
    student = db.get(Student, student_id)
    if student is None:
        return HTMLResponse("Student not found", status_code=404)
    programs = db.query(Program).filter_by(active=True).order_by(Program.name).all()
    return templates.TemplateResponse(
        request,
        "students/form.html",
        {
            **_ctx(current_user, db),
            "student": student,
            "programs": programs,
            "errors": [],
            "duplicate": None,
            "vals": {},
        },
    )


@router.post("/{student_id}/edit", response_class=HTMLResponse)
async def student_edit_save(
    student_id: int,
    request: Request,
    csrf_token: str = Form(""),
    first_name: str = Form(""),
    last_name: str = Form(""),
    program_id: str = Form(""),
    status: str = Form("active"),
    email: str = Form(""),
    home_phone: str = Form(""),
    work_phone: str = Form(""),
    address: str = Form(""),
    city: str = Form(""),
    state: str = Form(""),
    zip: str = Form(""),
    high_school: str = Form(""),
    seeking_employment: str = Form(""),
    desired_job: str = Form(""),
    current_user: UserAccount = Depends(_manage_dep),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf_token)
    student = db.get(Student, student_id)
    if student is None:
        return HTMLResponse("Student not found", status_code=404)

    programs = db.query(Program).filter_by(active=True).order_by(Program.name).all()
    vals = {
        "first_name": first_name, "last_name": last_name,
        "program_id": program_id, "status": status,
        "email": email, "home_phone": home_phone, "work_phone": work_phone,
        "address": address, "city": city, "state": state, "zip": zip,
        "high_school": high_school, "seeking_employment": seeking_employment,
        "desired_job": desired_job,
    }
    errors = _validate_form(first_name, last_name, home_phone, work_phone)

    # Duplicate check (exclude this student)
    duplicate = None
    if not errors and home_phone:
        dup = (
            db.query(Student)
            .filter(
                Student.first_name.ilike(first_name.strip()),
                Student.last_name.ilike(last_name.strip()),
                Student.home_phone == home_phone.strip(),
                Student.id != student_id,
            )
            .first()
        )
        if dup:
            duplicate = dup

    if errors:
        return templates.TemplateResponse(
            request,
            "students/form.html",
            {
                **_ctx(current_user, db),
                "student": student,
                "programs": programs,
                "errors": errors,
                "duplicate": duplicate,
                "vals": vals,
            },
            status_code=422,
        )

    student.first_name = first_name.strip()
    student.last_name = last_name.strip()
    student.program_id = int(program_id) if program_id else None
    student.status = status or "active"
    student.email = email.strip() or None
    student.home_phone = home_phone.strip() or None
    student.work_phone = work_phone.strip() or None
    student.address = address.strip() or None
    student.city = city.strip() or None
    student.state = state.strip() or None
    student.zip = zip.strip() or None
    student.high_school = high_school.strip() or None
    student.seeking_employment = (seeking_employment == "yes") if seeking_employment else None
    student.desired_job = desired_job.strip() or None
    student.version = (student.version or 1) + 1
    db.commit()
    audit.log_event(db, current_user.id, "student_edit", "student", student.id,
                    {
                        "version": student.version,
                        "student_number": student.student_number,
                        "student_name": f"{student.first_name} {student.last_name}",
                    })
    return RedirectResponse(f"/students/{student.id}", status_code=303)


# ---------------------------------------------------------------------------
# Detail
# ---------------------------------------------------------------------------

@router.get("/{student_id}", response_class=HTMLResponse)
async def student_detail(
    student_id: int,
    request: Request,
    current_user: UserAccount = Depends(_read_dep),
    db: Session = Depends(get_db),
):
    student = db.get(Student, student_id)
    if student is None:
        return HTMLResponse("Student not found", status_code=404)
    program = db.get(Program, student.program_id) if student.program_id else None
    all_jobs = (
        db.query(Employment, Employer)
        .join(Employer, Employment.employer_id == Employer.id)
        .filter(Employment.student_id == student_id)
        .order_by(Employment.start_date.desc())
        .all()
    )
    today = datetime.date.today()
    current_jobs = [(emp, employer) for emp, employer in all_jobs if is_current_job(emp, today)]
    history_jobs = [(emp, employer) for emp, employer in all_jobs if not is_current_job(emp, today)]
    return templates.TemplateResponse(
        request,
        "students/detail.html",
        {
            **_ctx(current_user, db),
            "student": student,
            "program": program,
            "current_jobs": current_jobs,
            "history_jobs": history_jobs,
            "today": today,
        },
    )
