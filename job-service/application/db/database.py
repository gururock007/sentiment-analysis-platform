# db/database.py
from sqlalchemy import  create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from core.config import settings

# for local development use docker 
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
# connect_args={"check_same_thread": False}
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to provide isolation for database sessions inside endpoint lifecycles
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()