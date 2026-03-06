"""
FastAPI application entry point.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routers import catalog, proposals


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialise the SQLite database on startup."""
    init_db()
    yield


app = FastAPI(
    title="AI Sustainable Commerce API",
    description=(
        "AI-powered modules for sustainable B2B commerce:\n\n"
        "- **Module 1**: AI Auto-Category & Tag Generator\n"
        "- **Module 2**: AI B2B Proposal Generator\n\n"
        "All AI calls are made via Google Gemini API and logged to the database."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ────────────────────────────────────────────────────────────────
app.include_router(catalog.router)
app.include_router(proposals.router)


# ─── Health check ───────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "AI Sustainable Commerce API", "version": "1.0.0"}


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "AI Sustainable Commerce API is running",
        "docs": "/docs",
        "modules": {
            "module1": "POST /api/v1/catalog/categorize",
            "module2": "POST /api/v1/proposals/generate",
        },
    }
