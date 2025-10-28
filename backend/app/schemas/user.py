from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for user creation."""
    username: str
    password: str


class UserResponse(BaseModel):
    """Schema for user response."""
    username: str
    total_tests: int
    total_time_seconds: int
    best_wpm: float
    best_accuracy: float
    total_experience: int
    level: int
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for auth token response."""
    access_token: str
    token_type: str
    username: str
