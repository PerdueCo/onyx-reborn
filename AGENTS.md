# Onyx Reborn — Rules for Bob (read this every session)

You are helping Clarence Perdue Jr. modernize the 1998 VB4 "BSSI / ONYX Student Information
System" into **Onyx Reborn**, a cloud web app, for the AngelHack × IBM Bob hackathon
(Theme 2: *Modernize What Matters*). Deadline: **Sun Oct 18, 2026, 11:59 PM ET** — we submit by 6 PM.

## Before doing anything
1. Read, in order: `docs/plan/scope.md`, `docs/plan/prd.md`, `docs/plan/spec.md`,
   `docs/design/DATABASE_SCHEMA.md` (**the schema source of truth**),
   `docs/analysis/legacy-inspection-report.md` (verified 1998 rules),
   `docs/plan/decisions.md`, `docs/plan/checklist.md`.
   If two docs disagree: DATABASE_SCHEMA.md > decisions.md > spec.md > prd.md. Point out the
   conflict to me instead of picking one quietly.
2. Read the last entry in `docs/bob-log.md` to see where we stopped.
3. Tell me in 3 lines: what's done, what's next on the checklist, anything blocking.

## How we work
- **One checklist item at a time.** Finish it, run the tests, then STOP and tell me how to
  check it in the browser (URL + what to click). Do not start the next item until I say go.
- **Ask, don't guess.** If the PRD/spec doesn't answer something, ask me a numbered list of
  questions. Record my answers in `docs/plan/decisions.md`.
- **Keep the docs true.** When we change a decision, update the doc in the same step.
- Check off finished items in `docs/plan/checklist.md` (`- [x]`).
- Never modify anything under `docs/legacy-reference/` — it is the read-only original.
- Never store or display real SSNs. The legacy importer drops SSNs (see spec §5).
- Never commit secrets. Config comes from `.env` (and `.env.example` lists the keys).
- Every new route or rule gets a pytest test. `pytest` must pass before an item is checked off.
- Keep it simple: server-rendered pages (FastAPI + Jinja2), no front-end framework.

## Stack (do not change without asking)
Python 3.12 · FastAPI · Jinja2 · SQLAlchemy 2 + Alembic · SQLite (foreign keys ON) locally,
PostgreSQL as roadmap/upgrade · pyotp (MFA) · passlib/bcrypt · pytest · Docker · deploy to IBM
Cloud Code Engine (fallback: Render). No paid services without Clarence's OK.

## Honest credit
Bob writes the application code. The planning docs were drafted with ChatGPT (schema) and
Claude (scope/PRD/spec/checklist) from Clarence's decisions. Never describe those docs as
Bob's work in `bob-log.md`. Log real prompts, outputs, corrections, commit IDs and test
results.

## Design
Match the mockups in `docs/design-reference/design/mockups/`: navy left sidebar, white cards,
blue primary buttons, "Onyx Reborn" wordmark. Plain CSS in `app/static/css/onyx.css`.
