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

    class Config:
        from_attributes = True