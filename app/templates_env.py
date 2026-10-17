"""Shared Jinja2Templates instance.

All routers import from here so they share one Environment.
Globals (e.g. csrf_token) registered in app/main.py propagate everywhere.
"""
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
