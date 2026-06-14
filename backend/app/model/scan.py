from pydantic import BaseModel

class ScanRequest(BaseModel):
    target: str
    ports: list[int] = [22, 80, 443]
    
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ScanResponse(BaseModel):
    id: int
    target: str
    ports: str
    status: str
    created_at: datetime
from pydantic import BaseModel, ConfigDict

class ScanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    target: str
    ports: str
    status: str
    created_at: datetime
        
class ScanStatusUpdate(BaseModel):
    status: str

class ScanResult(BaseModel):
    scan_id: int
    open_ports: list[int]
    services: dict[str, str] = {}
    risk_level: str = "low"

