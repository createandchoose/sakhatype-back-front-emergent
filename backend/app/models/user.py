from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.db.database import Base


class User(Base):
    """User model."""
    __tablename__ = 'users'

    username = Column(String, primary_key=True, index=True)
    password = Column(String, nullable=False)
    total_tests = Column(Integer, default=0)
    total_time_seconds = Column(Integer, default=0)
    best_wpm = Column(Float, default=0.0)
    best_accuracy = Column(Float, default=0.0)
    total_experience = Column(Integer, default=0)
    level = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
