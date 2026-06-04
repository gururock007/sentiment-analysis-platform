# core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentiment Job Service"
    API_V1_STR: str = "/api/v1"
    
    # Connection pointers

    # redis configuration
    REDIS_HOST: str = "redis"
    REDIS_SERVICE_PORT: int = 6379
    REDIS_QUEUE_NAME: str = "sentiment_jobs"

    # Postgres configuration
    POSTGRES_HOST: str = "postgres"
    POSTGRES_USER: str = "app"
    POSTGRES_PASSWORD: str = "app"
    POSTGRES_DB: str = "sentiment"
    POSTGRES_PORT: int = 5432

    class Config:
        env_file = ".env"

settings = Settings()