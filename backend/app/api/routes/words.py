from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.services.word_service import WordService


router = APIRouter(prefix='/api', tags=['Words'])


@router.get('/words', response_model=List[str])
def get_words(limit: int = 100, db: Session = Depends(get_db)):
    """Get random words for typing test."""
    return WordService.get_random_words(db, limit)
