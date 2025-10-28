from pydantic_settings import BaseSettings
import secrets


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = 'sqlite:///./sakhatype.db'
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: list = ['*']
    
    # App
    APP_NAME: str = 'Sakhatype API'
    VERSION: str = '1.0.0'
    DEBUG: bool = True
    
    class Config:
        case_sensitive = True


settings = Settings()
