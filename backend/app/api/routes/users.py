from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserResponse
from app.services.user_service import UserService
from app.core.security import get_current_username


router = APIRouter(prefix='/api', tags=['Users'])


@router.get('/users/me', response_model=UserResponse)
def get_current_user(username: str = Depends(get_current_username), db: Session = Depends(get_db)):
    """Get current user info."""
    user = UserService.get_by_username(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user


@router.get('/profile/{username}', response_model=UserResponse)
def get_user_profile(username: str, db: Session = Depends(get_db)):
    """Get user profile."""
    user = UserService.get_by_username(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user
