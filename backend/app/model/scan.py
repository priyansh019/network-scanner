from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from pydantic import field_validator
import re

class ScanRequest(BaseModel):
    target: str
    ports: list[int] = [22, 80, 443]

    @field_validator('target')
    def validate_target(cls, v):
        # Allow IPs and valid hostnames only
        if not re.match(r'^[a-zA-Z0-9.\-]+$', v):
            raise ValueError('Invalid target format')
        return v
    
class ScanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    target: str
    ports: str
    status: str
    created_at: datetime
    open_ports: Optional[list] = None
    services: Optional[dict] = None
    risk_level: Optional[str] = None
        
class ScanStatusUpdate(BaseModel):
    status: str

class ScanResult(BaseModel):
    scan_id: int
    open_ports: list[int]
    services: dict[str, str] = {}
    risk_level: str = "low"

