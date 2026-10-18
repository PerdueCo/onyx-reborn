FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# If DEMO_MODE=true, reset the DB before starting the server.
# PORT is injected by Render (defaults to 8000).
CMD set -e; \
    if [ "${DEMO_MODE}" = "true" ]; then \
        echo "==> DEMO_MODE: seeding fresh database..."; \
        python scripts/reset_db.py; \
    fi; \
    exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
