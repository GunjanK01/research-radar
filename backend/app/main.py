# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Research Radar API",
    description="Search, filter, and explore a corpus of research papers, with embedding-based similar-paper lookup.",
    version="0.1.0",
)

# Wide-open CORS for local dev / take-home evaluation. Note this tradeoff in the README:
# in a real production platform this would be locked to specific origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Basic liveness check — also useful for docker-compose healthchecks later."""
    return {"status": "ok"}


# Routers get mounted here as they're built, e.g.:
# from app.routers import papers
# app.include_router(papers.router)
