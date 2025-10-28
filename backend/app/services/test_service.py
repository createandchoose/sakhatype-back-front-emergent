from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime

from app.models.test_result import TestResult
from app.models.user import User
from app.schemas.test import TestResultCreate


class TestService:
    """Service for test operations."""
    
    @staticmethod
    def create_result(db: Session, username: str, result_data: TestResultCreate) -> TestResult:
        """Create test result and update user stats."""
        # Create test result
        db_result = TestResult(
            username=username,
            wpm=result_data.wpm,
            raw_wpm=result_data.raw_wpm,
            accuracy=result_data.accuracy,
            burst_wpm=result_data.burst_wpm,
            total_errors=result_data.total_errors,
            time_mode=result_data.time_mode,
            test_duration=result_data.test_duration,
            consistency=result_data.consistency,
            created_at=datetime.utcnow()
        )
        db.add(db_result)
        
        # Update user statistics
        user = db.query(User).filter(User.username == username).first()
        if user:
            user.total_tests += 1
            user.total_time_seconds += result_data.test_duration
            
            # Update best scores
            if result_data.wpm > user.best_wpm:
                user.best_wpm = result_data.wpm
            if result_data.accuracy > user.best_accuracy:
                user.best_accuracy = result_data.accuracy
            
            # Add experience and calculate level
            experience_gained = int(result_data.wpm + result_data.accuracy)
            user.total_experience += experience_gained
            user.level = 1 + (user.total_experience // 1000)
        
        db.commit()
        db.refresh(db_result)
        return db_result
    
    @staticmethod
    def get_user_results(db: Session, username: str, limit: int = 50) -> list[TestResult]:
        """Get user's test results."""
        return db.query(TestResult)\
            .filter(TestResult.username == username)\
            .order_by(desc(TestResult.created_at))\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_leaderboard_wpm(db: Session, limit: int = 100) -> list[User]:
        """Get WPM leaderboard."""
        return db.query(User)\
            .filter(User.total_tests > 0)\
            .order_by(desc(User.best_wpm))\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_leaderboard_accuracy(db: Session, limit: int = 100) -> list[User]:
        """Get accuracy leaderboard."""
        return db.query(User)\
            .filter(User.total_tests > 0)\
            .order_by(desc(User.best_accuracy))\
            .limit(limit)\
            .all()
