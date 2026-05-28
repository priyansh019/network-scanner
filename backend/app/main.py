from fastapi import FastAPI
from backend.app.api.routes import scan
from backend.app.database import engine, Base

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