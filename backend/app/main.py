from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import submission
from app.database.database import init_db

app = FastAPI(
    title="EvidenceLens API",
    description="Explainable misinformation evidence retrieval system",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


# Only Submission Router
app.include_router(
    submission.router,
    prefix="/api/submission",
)


@app.get("/")
def root():
    return {
        "project": "EvidenceLens",
        "version": "2.0.0",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}