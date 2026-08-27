"""
backend/app/main.py

Run from the backend/ folder:
    uvicorn app.main:app --reload --port 8000

Then check:
    http://localhost:8000/docs        — interactive Swagger UI
    http://localhost:8000/api/health  — should show model_loaded: true
"""

import sys
from pathlib import Path

# Make the sibling `engine/` package importable without installing it.
# Cleaner long-term option: turn engine/ into a proper package
# (add engine/pyproject.toml) and `pip install -e ../engine` — fine to defer.
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "engine"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api import health, model_info, predict
from app.core.limiter import limiter
from inference import HabitatInferenceEngine

app = FastAPI(title="Elephant Habitat API", version="1.0.0")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Restrict to actual known origins — never "*" once this isn't just a local test.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        # "https://your-production-domain.com",  # add once the frontend is deployed
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Loaded once at startup, shared across every request via app.state —
# NOT re-loaded per request. If the .pkl files are missing or corrupt,
# this raises immediately on startup rather than failing silently later.
app.state.engine = HabitatInferenceEngine()

app.include_router(health.router, prefix="/api")
app.include_router(model_info.router, prefix="/api")
app.include_router(predict.router, prefix="/api")