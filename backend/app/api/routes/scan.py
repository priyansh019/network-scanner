from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.model.scan import ScanRequest
from app.model.db_model import ScanHistory
from app.database import get_db
from app.model.scan import ScanRequest, ScanResponse
from app.model.scan import ScanRequest, ScanResponse, ScanStatusUpdate
from app.model.scan import ScanRequest, ScanResponse, ScanStatusUpdate, ScanResult


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

from fastapi import APIRouter, Depends, HTTPException, Query

@router.get("/scan/history", response_model=List[ScanResponse])
def get_scan_history(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    scans = db.query(ScanHistory).offset(skip).limit(limit).all()
    return scans

from fastapi import APIRouter, Depends, HTTPException

@router.get("/scan/{scan_id}", response_model=ScanResponse)
def get_scan(scan_id: int, db: Session = Depends(get_db)):
    scan = db.query(ScanHistory).filter(ScanHistory.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan

@router.patch("/scan/{scan_id}/status", response_model=ScanResponse)
def update_scan_status(scan_id: int, update: ScanStatusUpdate, db: Session = Depends(get_db)):
    scan = db.query(ScanHistory).filter(ScanHistory.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    scan.status = update.status
    db.commit()
    db.refresh(scan)
    return scan



@router.post("/scan/{scan_id}/results")
def submit_scan_results(scan_id: int, result: ScanResult, db: Session = Depends(get_db)):
    scan = db.query(ScanHistory).filter(ScanHistory.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    scan.open_ports = result.open_ports
    scan.services = result.services
    scan.risk_level = result.risk_level
    scan.status = "completed"
    db.commit()
    db.refresh(scan)
    return {
        "message": "Scan results saved",
        "scan_id": scan.id,
        "status": scan.status,
        "open_ports": scan.open_ports,
        "risk_level": scan.risk_level
    }
    



