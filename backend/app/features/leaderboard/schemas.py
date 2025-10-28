from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LeaderboardEntry(BaseModel):
    username: str
    wpm: Optional[float] = None
    accuracy: Optional[float] = None
    total_tests: int
    best_wpm: float
    best_accuracy: float
    level: int

    class Config:
        from_attributes = True

class TimeModeLeaderboardEntry(BaseModel):
    username: str
    wpm: float
    accuracy: float
    raw: float
    consistency: float
    date: datetime
    level: int

class WeeklyXPLeaderboardEntry(BaseModel):
    username: str
    xp_gained: int
    time_typed: int
    last_activity: datetime
    level: int
