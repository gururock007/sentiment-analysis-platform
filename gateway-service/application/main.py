# main.py
import uvicorn
from fastapi import FastAPI
from core.config import settings
from api.v1.router import api_router

app = FastAPI(title=settings.PROJECT_NAME)

# Mount the versioned API router under /api/v1
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["health"])
async def root_health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME}

if __name__ == "__main__":
    # Runs the server locally on port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)