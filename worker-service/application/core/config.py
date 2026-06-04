# core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    # Connection points

    # Redis configurations

    REDIS_HOST: str = "redis"
    REDIS_SERVICE_PORT: int = 6379
    REDIS_QUEUE_NAME: str = "sentiment_jobs"
    
    # Postgres configuration
    
    POSTGRES_HOST: str = "postgres"
    POSTGRES_USER: str = "app"
    POSTGRES_PASSWORD: str = "app"
    POSTGRES_DB: str = "sentiment"
    POSTGRES_PORT: int = 5432

    # Model paths

    MODEL_PATH: str = "models/sentiment_model.pkl"
    VECTORIZER_PATH: str = "models/tfidf_vectorizer.pkl"

    class Config:
        env_file = ".env"

settings = Settings()