from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.model.scan import ScanRequest
from backend.app.model.db_model import ScanHistory
from backend.app.database import get_db

router = APIRouter()

@router.get("/scan/status")
def scan_status():
    return {"status": "ready", "message": "Scanner is ready to run"}

@router.post("/scan/start")
def start_scan(request: ScanRequest, db: Session = Depends(get_db)):
    scan = ScanHistory(
        target=request.target,
        ports=str(request.ports),
        status="initiated"
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return {
        "message": "Scan initiated",
        "scan_id": scan.id,
        "target": scan.target,
        "ports": request.ports,
        "status": scan.status
    }