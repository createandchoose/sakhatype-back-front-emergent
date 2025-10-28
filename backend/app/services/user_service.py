from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password


class UserService:
    """Service for user operations."""
    
    @staticmethod
    def get_by_username(db: Session, username: str) -> User | None:
        """Get user by username."""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create new user."""
        # Check if user exists
        existing_user = UserService.get_by_username(db, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'User with username {user_data.username} already exists'
            )
        
        # Create user
        db_user = User(
            username=user_data.username,
            password=get_password_hash(user_data.password),
            created_at=datetime.utcnow()
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def authenticate(db: Session, username: str, password: str) -> User | None:
        """Authenticate user."""
        user = UserService.get_by_username(db, username)
        if not user or not verify_password(password, user.password):
            return None
        return user
