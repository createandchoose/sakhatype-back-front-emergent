from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.test import LeaderboardEntry
from app.services.test_service import TestService


router = APIRouter(prefix='/api/leaderboard', tags=['Leaderboard'])


@router.get('/wpm', response_model=List[LeaderboardEntry])
def get_wpm_leaderboard(limit: int = 100, db: Session = Depends(get_db)):
    """Get WPM leaderboard."""
    return TestService.get_leaderboard_wpm(db, limit)


@router.get('/accuracy', response_model=List[LeaderboardEntry])
def get_accuracy_leaderboard(limit: int = 100, db: Session = Depends(get_db)):
    """Get accuracy leaderboard."""
    return TestService.get_leaderboard_accuracy(db, limit)
