from fastapi import FastAPI

app = FastAPI(
    title="SentinelPy",
    description="Network Security Scanning Platform",
    version="0.1.0"
)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "SentinelPy backend is running"}