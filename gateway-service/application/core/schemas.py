# core/schemas.py
from pydantic import BaseModel, Field
from typing import Optional

# Input validation model for incoming requests
class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="The tweet or text to analyze.")

# Output model when a job is successfully queued
class JobCreatedResponse(BaseModel):
    job_id: str
    status: str = "queued"

# Output model for checking results
class JobResultResponse(BaseModel):
    job_id: str
    status: str
    sentiment: Optional[str] = None
    confidence: Optional[float] = None