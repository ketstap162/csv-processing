import os
from pathlib import Path
from typing import List

import ujson
from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings
from datetime import timezone, datetime

# Loading variables from the .env file
load_dotenv()


class Settings(BaseSettings):        
    # API
    API_HOST: str = os.getenv("API_HOST", "127.0.0.1")
    API_PORT: int = os.getenv("API_PORT", 8000)
    API_URL: str = os.getenv("API_URL", "http://127.0.0.1:8000")

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    BACKEND_CORS_ORIGINS: str | List[str] = []

    @field_validator("BACKEND_CORS_ORIGINS")
    def parse_cors_origins(cls, value: str | list) -> List[str]:
        if isinstance(value, str):
            return ujson.loads(value)
        elif isinstance(value, list):
            return value

    # DB
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "default_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "default_password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "default_dbname")
    POSTGRES_PORT: int = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", 'localhost')
    
    class Config:
        env_file = "env/.env.dev"
        extra = "ignore"
        
        
settings = Settings()
