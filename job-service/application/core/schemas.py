# core/schemas.py
from pydantic import BaseModel
from typing import Optional

class JobCreateInput(BaseModel):
    text: str

class JobStatusResponse(BaseModel):
    id: str
    text: str
    status: str
    result: Optional[str] = None
    confidence: Optional[float] = None

    class Config:
        from_attributes = True # Allows Pydantic to read raw SQLAlchemy objects directly