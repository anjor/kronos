from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/kronos"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # OAuth - Google
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    google_redirect_uri: str = "http://localhost:8000/api/auth/callback/google"
    
    # OAuth - Microsoft
    microsoft_client_id: Optional[str] = None
    microsoft_client_secret: Optional[str] = None
    microsoft_tenant_id: Optional[str] = "common"
    microsoft_redirect_uri: str = "http://localhost:8000/api/auth/callback/microsoft"
    
    # Cal.com
    caldotcom_api_key: Optional[str] = None
    caldotcom_base_url: str = "https://api.cal.com/v1"
    
    # Frontend URL for CORS and redirects
    frontend_url: str = "http://localhost:3000"
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # Celery
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()