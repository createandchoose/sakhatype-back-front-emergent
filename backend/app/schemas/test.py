from pydantic import BaseModel
from datetime import datetime


class TestResultCreate(BaseModel):
    """Schema for creating test result."""
    wpm: float
    raw_wpm: float
    accuracy: float
    burst_wpm: float
    total_errors: int
    time_mode: int
    test_duration: int
    consistency: float = 0.0


class TestResultResponse(BaseModel):
    """Schema for test result response."""
    id: int
    username: str
    wpm: float
    raw_wpm: float
    accuracy: float
    burst_wpm: float
    total_errors: int
    time_mode: int
    test_duration: int
    consistency: float
    created_at: datetime

    class Config:
        from_attributes = True


class LeaderboardEntry(BaseModel):
    """Schema for leaderboard entry."""
    username: str
    best_wpm: float
    best_accuracy: float
    total_tests: int
    level: int

    class Config:
        from_attributes = True
