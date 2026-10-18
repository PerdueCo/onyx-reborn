"""Reports router — /reports.

Routes:
  GET  /reports                     HTML table (current employment)
  GET  /reports/current-employment/export.csv   CSV download

Permission: reports.read
"""
import csv
import io

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import UserAccount
from app.security import get_user_permissions, require_permission
from app.services.reports import get_current_employment, get_employers, get_programs
from app.templates_env import templates

router = APIRouter(prefix="/reports", tags=["reports"])
_read_dep = require_permission("reports.read")

# CSV column headers — must match the on-screen table headers
_CSV_HEADERS = [
    "Student Name",
    "STU Number",
    "Program",
    "Employer",
    "Job Title",
    "Hours/Week",
    "Hourly Rate",
]

# Map dict keys → CSV header order
_ROW_KEYS = ["student_name", "stu_number", "program", "employer", "job_title", "hours", "rate"]


def _ctx(current_user: UserAccount, db: Session) -> dict:
    return {
        "current_user": current_user,
        "user_perms": get_user_permissions(current_user, db),
    }


# ---------------------------------------------------------------------------
# HTML report page
# ---------------------------------------------------------------------------

@router.get("", response_class=HTMLResponse)
async def reports_index(
    request: Request,
    program_id: int | None = Query(default=None),
    employer_id: int | None = Query(default=None),
    current_user: UserAccount = Depends(_read_dep),
    db: Session = Depends(get_db),
):
    rows = get_current_employment(db, program_id=program_id, employer_id=employer_id)
    programs = get_programs(db)
    employers = get_employers(db)
    return templates.TemplateResponse(
        request,
        "reports/current_employment.html",
        {
            **_ctx(current_user, db),
            "rows": rows,
            "programs": programs,
            "employers": employers,
            "selected_program_id": program_id,
            "selected_employer_id": employer_id,
            "active_page": "reports",
        },
    )


# ---------------------------------------------------------------------------
# CSV export
# ---------------------------------------------------------------------------

@router.get("/current-employment/export.csv")
async def export_csv(
    request: Request,
    program_id: int | None = Query(default=None),
    employer_id: int | None = Query(default=None),
    current_user: UserAccount = Depends(_read_dep),
    db: Session = Depends(get_db),
):
    rows = get_current_employment(db, program_id=program_id, employer_id=employer_id)

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(_CSV_HEADERS)
    for row in rows:
        writer.writerow([row[k] for k in _ROW_KEYS])

    buf.seek(0)
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="current_employment.csv"'},
    )
