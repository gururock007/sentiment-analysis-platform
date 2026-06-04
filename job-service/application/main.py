# main.py
import uvicorn
from fastapi import FastAPI
from core.config import settings
from api.v1.router import api_router
from db.database import engine, Base

# Automatically create local SQLite database tables if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["health"])
async def service_health():
    return {"status": "operational", "service": settings.PROJECT_NAME}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)