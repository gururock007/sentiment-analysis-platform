# api/v1/router.py
from fastapi import APIRouter
from api.v1.endpoints import router as endpoints_router

api_router = APIRouter()
api_router.include_router(endpoints_router, tags=["jobs-orchestrator"])