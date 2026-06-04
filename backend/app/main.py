from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import scan
from app.database import engine, Base
from app.config import APP_TITLE, DEBUG

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_TITLE,
    description="Network Security Scanning Platform",
    version="0.1.0"
)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if not DEBUG else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scan.router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "SentinelPy backend is running"}