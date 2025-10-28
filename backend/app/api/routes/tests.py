from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.test import TestResultCreate, TestResultResponse
from app.services.test_service import TestService
from app.core.security import get_current_username


router = APIRouter(prefix='/api', tags=['Tests'])


@router.post('/results', response_model=TestResultResponse)
def save_test_result(
    result_data: TestResultCreate,
    username: str = Depends(get_current_username),
    db: Session = Depends(get_db)
):
    """Save test result."""
    return TestService.create_result(db, username, result_data)


@router.get('/results/user/{username}', response_model=List[TestResultResponse])
def get_user_results(username: str, limit: int = 50, db: Session = Depends(get_db)):
    """Get user's test results."""
    return TestService.get_user_results(db, username, limit)
