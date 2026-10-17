"""Seed demo data — ~250 fictional students, ~12 employers, ~170 jobs.

Rules
-----
- Never touches records where legacy_source=True.
- Idempotent: guarded by a DEMO_SEED_MARKER employer (legacy_code='DEMO_SEED').
  If that employer already exists, the whole seed is skipped.
- ~250 students spread across the 5 programs.
- ~12 employers with realistic GA company names (includes names from dashboard mockup).
- ~170 jobs with realistic start/end dates.
  - Some jobs ended (end_date set).
  - 17 students hold exactly 2 concurrent jobs (no end_date on either).
  - ~40 students have seeking_employment=True, no current job.
- Assigned STU-#### numbers continue from wherever the legacy import left off.

Usage:
    .venv\\Scripts\\python.exe scripts/seed_demo.py
"""
from __future__ import annotations

import sys
import os
import random
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy.orm import Session

from app.db import engine
from app.models import Employer, Employment, Program, Student
import app.models  # noqa: F401

# ---------------------------------------------------------------------------
# Deterministic RNG — same output on every run (idempotency via guard)
# ---------------------------------------------------------------------------
RNG = random.Random(20261009)

# ---------------------------------------------------------------------------
# Demo employer data (includes company names from dashboard mockup context)
# ---------------------------------------------------------------------------

DEMO_EMPLOYERS = [
    # (name, address, city, state, zip, phone, company_type, legacy_code)
    ("Peachtree Technology Group",   "100 Peachtree Center Ave", "Atlanta",      "GA", "30303", "(404) 555-0100", "Technology Services",   "DEMO001"),
    ("Metro Business Solutions",     "200 Commerce Drive",       "Decatur",      "GA", "30030", "(404) 555-0200", "Business Services",     "DEMO002"),
    ("Creative Digital Agency",      "300 Studio Row",           "Marietta",     "GA", "30060", "(770) 555-0300", "Media and Design",      "DEMO003"),
    ("Southern Network Associates",  "400 Systems Blvd",         "Smyrna",       "GA", "30080", "(770) 555-0400", "Information Technology","DEMO004"),
    ("Summit Accounting Group",      "500 Ledger Pkwy",          "College Park", "GA", "30337", "(404) 555-0500", "Accounting Services",   "DEMO005"),
    ("Northside Medical Center",     "600 Healthcare Way",       "Roswell",      "GA", "30076", "(770) 555-0600", "Healthcare",            "DEMO006"),
    ("Atlanta Financial Partners",   "700 Capital Blvd",         "Atlanta",      "GA", "30301", "(404) 555-0700", "Financial Services",    "DEMO007"),
    ("Gwinnett Technical Services",  "800 Techpark Ln",          "Lawrenceville","GA", "30043", "(770) 555-0800", "Technology Services",   "DEMO008"),
    ("Sandy Springs Marketing",      "900 Marketing Way",        "Sandy Springs","GA", "30328", "(770) 555-0900", "Marketing",             "DEMO009"),
    ("Kennesaw Office Systems",      "1000 Business Park Dr",    "Kennesaw",     "GA", "30144", "(770) 555-1000", "Office Technology",     "DEMO010"),
    ("Duluth Data Management",       "1100 Data Center Rd",      "Duluth",       "GA", "30096", "(770) 555-1100", "Information Technology","DEMO011"),
    ("Buckhead Professional Group",  "1200 Professional Pkwy",   "Atlanta",      "GA", "30305", "(404) 555-1200", "Business Services",     "DEMO012"),
]

# ---------------------------------------------------------------------------
# Student name pools (fictional)
# ---------------------------------------------------------------------------

FIRST_NAMES = [
    "Alex", "Blake", "Cameron", "Dakota", "Drew", "Ellis", "Finley", "Gray",
    "Harper", "Indigo", "Jamie", "Kendall", "Logan", "Morgan", "Noel", "Oakley",
    "Parker", "Quinn", "Reese", "Sage", "Taylor", "Val", "Wren", "Zara",
    "Avery", "Bailey", "Casey", "Dana", "Emery", "Frankie", "Hayden", "Jordan",
    "Kyle", "Lane", "Marley", "Nico", "Olive", "Peyton", "Riley", "Skyler",
    "Tatum", "Uma", "Venice", "Whitney", "Xander", "Yael", "Zoe", "Ash",
    "Brook", "Caden", "Devon", "Eden", "Flyn", "Glenn", "Harlow", "Imani",
]

LAST_NAMES = [
    "Adams", "Baker", "Campbell", "Davis", "Evans", "Foster", "Garcia",
    "Harris", "Ingram", "Jones", "King", "Lewis", "Martin", "Nelson",
    "Owens", "Parker", "Quinn", "Roberts", "Scott", "Thomas", "Underwood",
    "Vega", "Walker", "Xavier", "Young", "Zhang", "Anderson", "Brown",
    "Clark", "Dixon", "Ellis", "Ford", "Green", "Hill", "Irwin", "Jackson",
    "Knight", "Lee", "Moore", "Nash", "Oliver", "Patel", "Reed", "Shaw",
    "Turner", "Upton", "Vargas", "Webb", "Xu", "York", "Zimmerman",
    "Allen", "Bell", "Cruz", "Dean", "Edwards", "Fletcher", "Grant", "Hayes",
]

HIGH_SCHOOLS = [
    "Northside High School",
    "Central High School",
    "Westview High School",
    "Lakeside High School",
    "East Point High School",
    "Dunwoody High School",
    "Tucker High School",
    "Norcross High School",
    "Brookwood High School",
    "Grayson High School",
]

GA_CITIES = [
    ("Atlanta",       "GA", "30301"),
    ("Decatur",       "GA", "30030"),
    ("Marietta",      "GA", "30060"),
    ("Smyrna",        "GA", "30080"),
    ("College Park",  "GA", "30337"),
    ("Roswell",       "GA", "30076"),
    ("Lawrenceville", "GA", "30043"),
    ("Sandy Springs", "GA", "30328"),
    ("Kennesaw",      "GA", "30144"),
    ("Duluth",        "GA", "30096"),
]

JOB_TITLES_BY_PROGRAM = {
    "CIS101": ["Computer Support Specialist", "Help Desk Technician", "IT Support Intern",
               "Data Entry Specialist", "Network Assistant"],
    "ACC110": ["Accounting Clerk", "Payroll Assistant", "Bookkeeper", "Tax Preparer Aide",
               "Accounts Receivable Clerk"],
    "BUS201": ["Administrative Assistant", "Office Coordinator", "Business Analyst Intern",
               "Operations Clerk", "Customer Service Rep"],
    "MKT130": ["Marketing Assistant", "Social Media Coordinator", "Sales Support Rep",
               "Event Planner Aide", "Brand Ambassador"],
    "OFT120": ["Office Assistant", "Receptionist", "Data Processor", "Records Clerk",
               "Administrative Aide"],
}

# Legacy code→program code mapping
DEMO_EMPLOYER_PROGRAM_AFFINITY = {
    "DEMO001": "CIS101",
    "DEMO002": "BUS201",
    "DEMO003": "MKT130",
    "DEMO004": "CIS101",
    "DEMO005": "ACC110",
    "DEMO006": "BUS201",
    "DEMO007": "ACC110",
    "DEMO008": "CIS101",
    "DEMO009": "MKT130",
    "DEMO010": "OFT120",
    "DEMO011": "CIS101",
    "DEMO012": "BUS201",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _next_student_number(db: Session) -> str:
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


def _random_phone() -> str:
    area = RNG.choice(["404", "770", "678"])
    return f"({area}) 555-{RNG.randint(1000, 9999):04d}"


def _random_address() -> str:
    return f"{RNG.randint(100, 9999)} {RNG.choice(['Oak', 'Maple', 'Pine', 'Cedar', 'Elm'])} {RNG.choice(['St', 'Ave', 'Dr', 'Ln', 'Way'])}"


def _random_enrolled() -> date:
    # Enrolled 2019–2024
    year = RNG.randint(2019, 2024)
    month = RNG.randint(1, 12)
    day = RNG.randint(1, 28)
    return date(year, month, day)


def _random_grad(enrolled: date) -> date | None:
    if RNG.random() < 0.6:
        grad_months = RNG.randint(18, 30)
        return enrolled + timedelta(days=grad_months * 30)
    return None


# ---------------------------------------------------------------------------
# Main seeder
# ---------------------------------------------------------------------------

def seed(session: Session) -> None:
    """Insert demo employers, students, and jobs.  Skips if already seeded."""

    # Idempotency guard
    if session.query(Employer).filter_by(legacy_code="DEMO_SEED").first():
        print("Demo seed already present — skipping.")
        return

    # Marker employer (not used for jobs)
    marker = Employer(
        name="[Demo Seed Marker]",
        legacy_code="DEMO_SEED",
        active=False,
    )
    session.add(marker)
    session.flush()

    # 1. Upsert programs
    PROGRAMS = [
        ("CIS101", "Computer Information Systems"),
        ("ACC110", "Accounting Technology"),
        ("BUS201", "Business Administration"),
        ("MKT130", "Marketing"),
        ("OFT120", "Office Technology"),
    ]
    prog_map: dict[str, Program] = {}
    for code, name in PROGRAMS:
        p = session.query(Program).filter_by(code=code).first()
        if not p:
            p = Program(code=code, name=name, active=True)
            session.add(p)
            session.flush()
        prog_map[code] = p

    # 2. Upsert demo employers
    emp_map: dict[str, Employer] = {}
    for (name, address, city, state, zip_, phone, company_type, demo_code) in DEMO_EMPLOYERS:
        e = session.query(Employer).filter_by(legacy_code=demo_code).first()
        if not e:
            e = Employer(
                name=name,
                address=address,
                city=city,
                state=state,
                zip=zip_,
                phone=phone,
                company_type=company_type,
                legacy_code=demo_code,
                active=True,
            )
            session.add(e)
            session.flush()
        emp_map[demo_code] = e

    employer_list = list(emp_map.values())

    # 3. Build student pool
    # Distribute ~250 students across 5 programs
    program_codes = list(prog_map.keys())
    N_STUDENTS = 250

    # Pre-assign unique (first, last) combos
    name_pool = [
        (f, l) for f in FIRST_NAMES for l in LAST_NAMES
        if (f, l) not in {("Alex", "Adams")}  # avoid exact duplicates
    ]
    RNG.shuffle(name_pool)
    name_pool = name_pool[:N_STUDENTS]

    all_students: list[Student] = []
    for i, (first, last) in enumerate(name_pool):
        prog_code = program_codes[i % len(program_codes)]
        enrolled = _random_enrolled()
        grad = _random_grad(enrolled)
        city, state, zip_ = RNG.choice(GA_CITIES)
        high_school = RNG.choice(HIGH_SCHOOLS)

        s = Student(
            student_number=_next_student_number(session),
            first_name=first,
            last_name=last,
            home_phone=_random_phone(),
            work_phone=_random_phone() if RNG.random() < 0.4 else None,
            address=_random_address(),
            city=city,
            state=state,
            zip=zip_,
            high_school=high_school,
            date_graduated=grad,
            enrolled_date=enrolled,
            seeking_employment=False,  # set below for seeking cohort
            status="active",
            program_id=prog_map[prog_code].id,
            legacy_source=False,
        )
        session.add(s)
        session.flush()
        all_students.append(s)

    session.flush()

    # 4. Assign jobs
    # Target: ~170 jobs.  17 students get 2 current jobs.  ~40 students seeking only.
    # Strategy:
    #   - Students 0..39  → seeking only (no job)
    #   - Students 40..56 → 2 concurrent current jobs (no end_date)
    #   - Students 57..169 → 1 current job (no end_date)  (113 students)
    #   - Students 170..249 → 1 ended job                  (80 students)
    # Total jobs: 17*2 + 113 + 80 = 34 + 113 + 80 = 227 → trim to ~170 by using
    # only ended=50, current-single=99, dual=17: 34+99+50=183 ≈ close enough.
    # Actual: dual=17 (34 jobs) + single_current=99 + single_ended=50 = 183 jobs.

    SEEKING_COUNT     = 40
    DUAL_CURRENT      = 17
    SINGLE_CURRENT    = 99
    SINGLE_ENDED      = 50
    # Remaining ~44 students get no job and are not seeking

    seeking_students   = all_students[:SEEKING_COUNT]
    dual_students      = all_students[SEEKING_COUNT : SEEKING_COUNT + DUAL_CURRENT]
    single_c_students  = all_students[SEEKING_COUNT + DUAL_CURRENT : SEEKING_COUNT + DUAL_CURRENT + SINGLE_CURRENT]
    single_e_students  = all_students[SEEKING_COUNT + DUAL_CURRENT + SINGLE_CURRENT :
                                      SEEKING_COUNT + DUAL_CURRENT + SINGLE_CURRENT + SINGLE_ENDED]

    # Mark seeking
    for s in seeking_students:
        s.seeking_employment = True
        s.desired_job = RNG.choice([
            "Entry-level accounting position",
            "Office assistant role",
            "IT help desk position",
            "Marketing coordinator role",
            "Business operations support",
        ])
    session.flush()

    today = date.today()

    def _emp_for_student(s: Student) -> Employer:
        """Pick an employer with affinity to the student's program."""
        prog = session.get(Program, s.program_id)
        prog_code = prog.code if prog else "CIS101"
        preferred = [
            emp_map[dc]
            for dc, pc in DEMO_EMPLOYER_PROGRAM_AFFINITY.items()
            if pc == prog_code and dc in emp_map
        ]
        if preferred:
            return RNG.choice(preferred)
        return RNG.choice(employer_list)

    def _job_title_for(s: Student) -> str:
        prog = session.get(Program, s.program_id)
        prog_code = prog.code if prog else "CIS101"
        return RNG.choice(JOB_TITLES_BY_PROGRAM.get(prog_code, ["Office Assistant"]))

    def _start_date(enrolled: date | None) -> date:
        base = enrolled or date(2020, 1, 1)
        offset = RNG.randint(30, 180)
        d = base + timedelta(days=offset)
        return min(d, today - timedelta(days=1))

    def _end_date(start: date) -> date:
        """Ended job: 3–24 months after start, before today."""
        months = RNG.randint(3, 24)
        end = start + timedelta(days=months * 30)
        return min(end, today - timedelta(days=30))

    def _hourly_rate() -> float:
        return round(RNG.uniform(13.0, 28.0), 2)

    def _hours() -> int:
        return RNG.choice([20, 24, 30, 32, 40])

    # Dual current jobs
    for s in dual_students:
        emp1 = _emp_for_student(s)
        emp2 = RNG.choice([e for e in employer_list if e.id != emp1.id])
        start1 = _start_date(s.enrolled_date)
        start2 = _start_date(s.enrolled_date)
        session.add(Employment(
            student_id=s.id, employer_id=emp1.id,
            job_title=_job_title_for(s), job_type="part_time",
            hours_per_week=_hours(), start_date=start1, end_date=None,
            hourly_rate=_hourly_rate(),
        ))
        session.add(Employment(
            student_id=s.id, employer_id=emp2.id,
            job_title=_job_title_for(s), job_type="part_time",
            hours_per_week=_hours(), start_date=start2, end_date=None,
            hourly_rate=_hourly_rate(),
        ))

    # Single current jobs
    for s in single_c_students:
        emp = _emp_for_student(s)
        start = _start_date(s.enrolled_date)
        session.add(Employment(
            student_id=s.id, employer_id=emp.id,
            job_title=_job_title_for(s),
            job_type=RNG.choice(["full_time", "part_time"]),
            hours_per_week=_hours(), start_date=start, end_date=None,
            hourly_rate=_hourly_rate(),
        ))

    # Single ended jobs
    for s in single_e_students:
        emp = _emp_for_student(s)
        start = _start_date(s.enrolled_date)
        end = _end_date(start)
        session.add(Employment(
            student_id=s.id, employer_id=emp.id,
            job_title=_job_title_for(s),
            job_type=RNG.choice(["full_time", "part_time", "other"]),
            hours_per_week=_hours(), start_date=start, end_date=end,
            hourly_rate=_hourly_rate(),
        ))

    session.commit()

    # Report
    total_students = session.query(Student).filter_by(legacy_source=False).count()
    total_jobs     = (
        session.query(Employment)
        .join(Student, Employment.student_id == Student.id)
        .filter(Student.legacy_source == False)  # noqa: E712
        .count()
    )
    print(
        f"Demo seed complete: {total_students} fictional students, "
        f"{len(employer_list)} demo employers, {total_jobs} jobs."
    )


if __name__ == "__main__":
    with Session(engine) as s:
        seed(s)
