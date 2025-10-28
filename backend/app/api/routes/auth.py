from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, TokenResponse
from app.services.user_service import UserService
from app.core.security import create_access_token


router = APIRouter(prefix='/api/auth', tags=['Authentication'])


@router.post('/register', response_model=TokenResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register new user."""
    user = UserService.create_user(db, user_data)
    access_token = create_access_token(user.username)
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'username': user.username
    }


@router.post('/login', response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login user."""
    user = UserService.authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    access_token = create_access_token(user.username)
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'username': user.username
    }
