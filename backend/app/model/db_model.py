from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime, timezone
from app.database import Base

class ScanHistory(Base):
    __tablename__ = "scan_history"

    id = Column(Integer, primary_key=True, index=True)
    target = Column(String, nullable=False)
    ports = Column(String, nullable=False)
    status = Column(String, default="initiated")
    open_ports = Column(JSON, nullable=True)
    services = Column(JSON, nullable=True)
    risk_level = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))