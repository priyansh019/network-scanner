from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.model.scan import ScanRequest
from app.model.db_model import ScanHistory
from app.database import get_db
from app.model.scan import ScanRequest, ScanResponse, ScanStatusUpdate, ScanResult
from app.core.dependencies import get_current_user
from app.model.db_user import User
from typing import List, Optional

router = APIRouter()

@router.post("/scan/start")
def start_scan(
    request: ScanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
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

@router.get("/scan/history", response_model=List[ScanResponse])
def get_scan_history(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    status: Optional[str] = Query(default=None),
    target: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(ScanHistory)
    if status:
        query = query.filter(ScanHistory.status == status)
    if target:
        query = query.filter(ScanHistory.target.contains(target))
    scans = query.offset(skip).limit(limit).all()
    return scans


       



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
    



