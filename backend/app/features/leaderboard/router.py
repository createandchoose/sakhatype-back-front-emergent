from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from .schemas import LeaderboardEntry, TimeModeLeaderboardEntry, WeeklyXPLeaderboardEntry
from .service import LeaderboardService
from ...shared.dependencies import get_db

router = APIRouter(prefix='/api/leaderboard', tags=['Leaderboard'])

@router.get('/wpm', response_model=List[LeaderboardEntry])
def get_leaderboard_wpm(limit: int = 100, db: Session = Depends(get_db)):
    return LeaderboardService.get_leaderboard_wpm(db, limit)

@router.get('/accuracy', response_model=List[LeaderboardEntry])
def get_leaderboard_accuracy(limit: int = 100, db: Session = Depends(get_db)):
    return LeaderboardService.get_leaderboard_accuracy(db, limit)

@router.get('/time-mode/{time_mode}', response_model=List[TimeModeLeaderboardEntry])
def get_leaderboard_by_time_mode(
    time_mode: int = Query(..., description="Time mode: 15 or 60 seconds"),
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all-time leaderboard for specific time mode"""
    return LeaderboardService.get_leaderboard_by_time_mode(db, time_mode, limit)

@router.get('/daily/time-mode/{time_mode}', response_model=List[TimeModeLeaderboardEntry])
def get_daily_leaderboard_by_time_mode(
    time_mode: int = Query(..., description="Time mode: 15 or 60 seconds"),
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get today's leaderboard for specific time mode"""
    return LeaderboardService.get_daily_leaderboard_by_time_mode(db, time_mode, limit)

@router.get('/weekly-xp', response_model=List[WeeklyXPLeaderboardEntry])
def get_weekly_xp_leaderboard(limit: int = 100, db: Session = Depends(get_db)):
    """Get weekly XP leaderboard"""
    return LeaderboardService.get_weekly_xp_leaderboard(db, limit)
