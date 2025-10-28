from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime

from app.db.database import Base


class TestResult(Base):
    """Test result model."""
    __tablename__ = 'test_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, ForeignKey('users.username'), index=True)
    wpm = Column(Float, nullable=False)
    raw_wpm = Column(Float, nullable=False)
    accuracy = Column(Float, nullable=False)
    burst_wpm = Column(Float, nullable=False)
    total_errors = Column(Integer, default=0)
    time_mode = Column(Integer, nullable=False)
    test_duration = Column(Integer, nullable=False)
    consistency = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
