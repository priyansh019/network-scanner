from pydantic import BaseModel

class ScanRequest(BaseModel):
    target: str
    ports: list[int] = [22, 80, 443]