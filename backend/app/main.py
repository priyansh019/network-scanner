from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.routes import scan
from app.database import engine, Base
from app.config import APP_TITLE, DEBUG
from app.api.routes import scan, mock_scanner
from app.config import APP_TITLE, DEBUG, ALLOWED_ORIGINS



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
app.include_router(mock_scanner.router, prefix="/api/v1")


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if not DEBUG else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if DEBUG else "Something went wrong"
        }
    )

app.include_router(scan.router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "SentinelPy backend is running"}