# core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentiment Gateway"
    API_V1_STR: str = "/api/v1"
    
    JOB_SERVICE_URL: str = "http://job:8001" 

    class Config:
        env_file = ".env"

settings = Settings()