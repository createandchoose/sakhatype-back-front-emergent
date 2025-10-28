from sqlalchemy.orm import Session
from sqlalchemy import desc, func, and_
from datetime import datetime, timedelta

from ..auth.models import User
from ..typing.models import TestResult

class LeaderboardService:
    @staticmethod
    def get_leaderboard_wpm(db: Session, limit: int = 100) -> list[User]:
        return db.query(User)\
            .filter(User.total_tests > 0)\
            .order_by(desc(User.best_wpm))\
            .limit(limit)\
            .all()

    @staticmethod
    def get_leaderboard_accuracy(db: Session, limit: int = 100) -> list[User]:
        return db.query(User)\
            .filter(User.total_tests > 0)\
            .order_by(desc(User.best_accuracy))\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_leaderboard_by_time_mode(db: Session, time_mode: int, limit: int = 100) -> list:
        """Get leaderboard for specific time mode (15 or 60 seconds) - all time"""
        # Subquery to get best result for each user for the specific time mode
        subquery = db.query(
            TestResult.username,
            func.max(TestResult.wpm).label('best_wpm'),
            func.max(TestResult.accuracy).label('best_accuracy')
        ).filter(TestResult.time_mode == time_mode)\
         .group_by(TestResult.username)\
         .subquery()
        
        # Get the actual test result with all details
        results = db.query(TestResult, User)\
            .join(User, TestResult.username == User.username)\
            .join(subquery, and_(
                TestResult.username == subquery.c.username,
                TestResult.wpm == subquery.c.best_wpm
            ))\
            .filter(TestResult.time_mode == time_mode)\
            .order_by(desc(TestResult.wpm))\
            .limit(limit)\
            .all()
        
        return [
            {
                'username': result.TestResult.username,
                'wpm': result.TestResult.wpm,
                'accuracy': result.TestResult.accuracy,
                'raw': result.TestResult.raw_wpm,
                'consistency': result.TestResult.consistency,
                'date': result.TestResult.created_at,
                'level': result.User.level
            }
            for result in results
        ]
    
    @staticmethod
    def get_daily_leaderboard_by_time_mode(db: Session, time_mode: int, limit: int = 100) -> list:
        """Get today's leaderboard for specific time mode"""
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        # Subquery to get best result for each user today for the specific time mode
        subquery = db.query(
            TestResult.username,
            func.max(TestResult.wpm).label('best_wpm')
        ).filter(
            and_(
                TestResult.time_mode == time_mode,
                TestResult.created_at >= today_start,
                TestResult.created_at < today_end
            )
        ).group_by(TestResult.username)\
         .subquery()
        
        # Get the actual test result with all details
        results = db.query(TestResult, User)\
            .join(User, TestResult.username == User.username)\
            .join(subquery, and_(
                TestResult.username == subquery.c.username,
                TestResult.wpm == subquery.c.best_wpm
            ))\
            .filter(
                and_(
                    TestResult.time_mode == time_mode,
                    TestResult.created_at >= today_start,
                    TestResult.created_at < today_end
                )
            )\
            .order_by(desc(TestResult.wpm))\
            .limit(limit)\
            .all()
        
        return [
            {
                'username': result.TestResult.username,
                'wpm': result.TestResult.wpm,
                'accuracy': result.TestResult.accuracy,
                'raw': result.TestResult.raw_wpm,
                'consistency': result.TestResult.consistency,
                'date': result.TestResult.created_at,
                'level': result.User.level
            }
            for result in results
        ]
    
    @staticmethod
    def get_weekly_xp_leaderboard(db: Session, limit: int = 100) -> list:
        """Get weekly XP leaderboard"""
        week_start = datetime.utcnow() - timedelta(days=7)
        
        # Calculate XP gained this week for each user
        results = db.query(
            TestResult.username,
            func.sum(TestResult.wpm + TestResult.accuracy).label('xp_gained'),
            func.sum(TestResult.test_duration).label('time_typed'),
            func.max(TestResult.created_at).label('last_activity'),
            User.level
        ).join(User, TestResult.username == User.username)\
         .filter(TestResult.created_at >= week_start)\
         .group_by(TestResult.username, User.level)\
         .order_by(desc(func.sum(TestResult.wpm + TestResult.accuracy)))\
         .limit(limit)\
         .all()
        
        return [
            {
                'username': result.username,
                'xp_gained': int(result.xp_gained),
                'time_typed': result.time_typed,
                'last_activity': result.last_activity,
                'level': result.level
            }
            for result in results
        ]
