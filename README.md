# Onyx Reborn

A 1998 Visual Basic 4 student information system (BSSI / ONYX), originally built as a
student capstone project, rebuilt as a secure web app with IBM Bob.
AngelHack x IBM Bob hackathon - Theme 2: Modernize What Matters.

**Live demo:** https://onyx-reborn.onrender.com
**Judges:** click **Sign in -> Try as Staff -> Use demo code**. No app or phone needed.
The free host sleeps when idle; the first visit can take about a minute.

## 1998 vs 2026

| Area | 1998 BSSI | 2026 Onyx Reborn |
| --- | --- | --- |
| Sign-in | None (SSN lookup) | Password + 2-step code (TOTP), lockout after 5 tries |
| Home | Switchboard | Dashboard with live numbers |
| Data | Fixed-width flat files | SQLite + SQLAlchemy + Alembic |
| Student ID | Social Security number | STU-#### numbers; SSNs discarded on import |
| Jobs | One, overwritten | Two at once, full history |
| Runs on | One PC | Docker on Render |

## Features

- Students: add, search, edit, duplicate warning
- Jobs: add, end, current vs history; employers list
- Dashboard: employment rate by program, top employers, recent activity
- Report: current employment, filters, CSV export, print layout
- Admin: users, unlock locked accounts, audit log
- 1998 importer: reads the original Student.txt / Employment.txt, keeps no SSNs
- Works on desktop, tablet and phone browsers

## Demo accounts (fictional data)

| Email | Password | 2-step |
| --- | --- | --- |
| admin@onyx.demo | OnyxAdmin2026! | Demo code shown on screen, or setup key JBSWY3DPEHPK3PXP |
| staff@onyx.demo | OnyxStaff2026! | Demo code shown on screen, or setup key JBSWY3DPEHPK3PXQ |
| newstaff@onyx.demo | OnyxNew2026! | First sign-in shows the QR setup page |

Demo mode (DEMO_MODE=true) adds the one-click buttons and shows the code for the two
demo accounts only. It is off in production; real accounts always use an authenticator app.

## Run locally

    py -3.12 -m venv .venv
    .venv\Scripts\pip install -r requirements.txt
    copy .env.example .env   (then set SESSION_SECRET and MFA_ENC_KEY)
    .venv\Scripts\python scripts\reset_db.py
    .venv\Scripts\uvicorn app.main:app --reload

## Tests

    .venv\Scripts\pytest -q     # 165 passed

## Deploy

See docs/DEPLOY.md (Render, Docker, render.yaml).

## How IBM Bob was used

- **Ask:** read the VB4 code and 1998 file layouts; wrote docs/analysis/legacy-inspection-report.md
- **Plan:** designed sign-in and 2-step; we answered its questions before any code
- **Agent:** built each step, wrote and ran tests, committed and pushed
- Rules for Bob: AGENTS.md. Decisions: docs/plan/decisions.md. Every session: docs/bob-log.md

## Roadmap

Student portal - update requests + review queue - full user management -
IBM Code Engine + Postgres - native mobile app

## About the project

Onyx began as a 1998 student capstone project by a five-person team. Onyx Reborn
brings that project into 2026 while keeping its core job: helping staff track
students and their employment.
