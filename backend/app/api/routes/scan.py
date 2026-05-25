from fastapi import APIRouter

router = APIRouter()

@router.get("/scan/status")
def scan_status():
    return {"status": "ready", "message": "Scanner is ready to run"}