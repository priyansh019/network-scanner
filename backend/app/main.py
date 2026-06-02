from fastapi import FastAPI
from app.api.routes import scan
from app.database import engine, Base
from app.config import APP_TITLE

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SentinelPy",
    description="Network Security Scanning Platform",
    version="0.1.0"
)

app.include_router(scan.router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "SentinelPy backend is running"}