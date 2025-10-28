from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.word import Word


class WordService:
    """Service for word operations."""
    
    @staticmethod
    def get_random_words(db: Session, limit: int = 100) -> list[str]:
        """Get random words for typing test."""
        words = db.query(Word.word)\
            .order_by(func.random())\
            .limit(limit)\
            .all()
        return [word[0] for word in words]
