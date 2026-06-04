# db/models.py
from sqlalchemy import Column, String, Float
from db.database import Base

class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    text = Column(String, nullable=False)
    status = Column(String)
    result = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)