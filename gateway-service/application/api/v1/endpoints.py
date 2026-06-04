# api/v1/endpoints.py
from fastapi import APIRouter, HTTPException, status
import httpx
from core.config import settings
from core.schemas import AnalyzeRequest, JobCreatedResponse, JobResultResponse

router = APIRouter()

@router.post("/analyze", response_model=JobCreatedResponse, status_code=status.HTTP_202_ACCEPTED)
async def analyze_text(payload: AnalyzeRequest):
    """
    Accepts text, generates a background tracking Job ID,
    and forwards the payload to the Job Service queue.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.JOB_SERVICE_URL}{settings.API_V1_STR}/jobs",
                json=payload.model_dump()
            )

            if response.status_code != status.HTTP_201_CREATED:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Downstream Job Service failed to initialize task."
                )
            
            job_data = response.json()
            return JobCreatedResponse(job_id=job_data['id'])
        
        except httpx.RequestError:
            raise HTTPException(
                status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Job Service orchestrator is offline or unreachable."
            )
            

@router.get("/result/{job_id}", response_model=JobResultResponse)
async def get_result(job_id: str):
    """
    Fetches the state/results of a specific processing job from the data store.
    """
    async with httpx.AsyncClient() as client:
        try:
            # Querying the state machine database through the Job Service
            response = await client.get(
                f"{settings.JOB_SERVICE_URL}{settings.API_V1_STR}/jobs/{job_id}"
            )
            
            if response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(status_code=404, detail="The specified Job ID does not exist.")
                
            job_data = response.json()
            
            # Map the Job Service model directly to the Gateway's expected schema
            return JobResultResponse(
                job_id=job_data["id"],
                status=job_data["status"],
                sentiment=job_data.get("result"),
                confidence=job_data.get("confidence")
            )
            
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to fetch job status. Downstream core database is unreachable."
            )