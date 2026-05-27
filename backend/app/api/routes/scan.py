from fastapi import APIRouter
from backend.app.model.scan import ScanRequest

router = APIRouter()

@router.get("/scan/status")
def scan_status():
    return {"status": "ready", "message": "Scanner is ready to run"}

@router.post("/scan/start")
def start_scan(request: ScanRequest):
    return {
        "message": "Scan initiated",
        "target": request.target,
        "ports": request.ports
    }