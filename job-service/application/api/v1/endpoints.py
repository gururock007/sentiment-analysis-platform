# api/v1/endpoints.py
import json
import uuid
import redis
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.config import settings
from core.schemas import JobCreateInput, JobStatusResponse
from db.database import get_db
from db.models import JobModel

router = APIRouter()

# Initialize the Redis connection pool
redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_SERVICE_PORT, decode_responses=True)

@router.post("/jobs", response_model=JobStatusResponse, status_code=status.HTTP_201_CREATED)
async def create_job(payload: JobCreateInput, db: Session = Depends(get_db)):
    """
    Creates a new job token inside the tracking database, registers its initial state,
    and pushes the execution context directly into the Redis task array pipeline.
    """
    job_id = str(uuid.uuid4())
    
    # 1. Instantiate the row tracking item
    new_job = JobModel(
        id=job_id,
        text=payload.text,
        status="pending"
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    
    # 2. Package transactional context for your downstream ML workers
    queue_payload = {
        "job_id": job_id,
        "text": payload.text
    }
    
    try:
        # Push context string to the right side of the Redis list
        redis_client.rpush(settings.REDIS_QUEUE_NAME, json.dumps(queue_payload))
    except redis.exceptions.ConnectionError:
        # Graceful failure state tracking if your broker vanishes unexpectedly
        new_job.status = "failed"
        db.commit()
        raise HTTPException(
            status_code=503, 
            detail="The message broker is unavailable. Job tracking has been aborted."
        )

    return new_job

@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str, db: Session = Depends(get_db)):
    """
    Fetches historical or processing states matching your exact unique tracking key.
    """
    job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Requested Job context registry not found.")
    return job