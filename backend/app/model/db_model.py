from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.database import Base

class ScanHistory(Base):
    __tablename__ = "scan_history"

    id = Column(Integer, primary_key=True, index=True)
    target = Column(String, nullable=False)
    ports = Column(String, nullable=False)
    status = Column(String, default="initiated")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))