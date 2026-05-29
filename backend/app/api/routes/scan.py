from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.model.scan import ScanRequest
from app.model.db_model import ScanHistory
from app.database import get_db
from app.model.scan import ScanRequest, ScanResponse

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
from typing import List

@router.get("/scan/history", response_model=List[ScanResponse])
def get_scan_history(db: Session = Depends(get_db)):
    scans = db.query(ScanHistory).all()
    return scans