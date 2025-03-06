# models.py

from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    keywords = Column(String, nullable=False)
    time = Column(String, nullable=False)
    status = Column(String, nullable=False)
    url = Column(String, nullable=False)