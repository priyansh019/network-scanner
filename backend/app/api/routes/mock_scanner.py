import random
import time
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.model.db_model import ScanHistory
from app.core.dependencies import get_current_user
from app.model.db_user import User

router = APIRouter()

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 443, 3306, 5432, 8080, 8443]

SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt"
}

def calculate_risk(open_ports: list[int]) -> str:
    dangerous_ports = [21, 23, 3306, 5432]
    if any(port in dangerous_ports for port in open_ports):
        return "critical"
    elif len(open_ports) > 5:
        return "high"
    elif len(open_ports) > 2:
        return "medium"
    return "low"

def run_scan_in_background(scan_id: int):
    db = SessionLocal()
    try:
        time.sleep(5)
        scan = db.query(ScanHistory).filter(ScanHistory.id == scan_id).first()
        if not scan:
            return
        open_ports = random.sample(COMMON_PORTS, random.randint(1, 6))
        services = {str(port): SERVICES[port] for port in open_ports}
        risk_level = calculate_risk(open_ports)
        scan.open_ports = open_ports
        scan.services = services
        scan.risk_level = risk_level
        scan.status = "completed"
        db.commit()
    except Exception:
        scan = db.query(ScanHistory).filter(ScanHistory.id == scan_id).first()
        if scan:
            scan.status = "failed"
            db.commit()
    finally:
        db.close()

@router.post("/mock/scan/{scan_id}/run")
def run_mock_scan(
    scan_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    scan = db.query(ScanHistory).filter(ScanHistory.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if scan.status != "initiated":
        raise HTTPException(
            status_code=400,
            detail=f"Scan already processed with status: {scan.status}"
        )
    scan.status = "processing"
    db.commit()
    background_tasks.add_task(run_scan_in_background, scan_id)
    return {
        "message": "Scan started in background",
        "scan_id": scan_id,
        "status": "processing"
    }