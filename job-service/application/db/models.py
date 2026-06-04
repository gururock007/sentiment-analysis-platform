# db/models.py
from sqlalchemy import Column, String, Float
from db.database import Base

class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    text = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, processing, done, failed
    result = Column(String, nullable=True)      # Stores: Positive / Negative
    confidence = Column(Float, nullable=True)   # Stores: 0.0 - 1.0 confidence score