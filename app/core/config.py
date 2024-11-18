from functools import lru_cache
from typing import List
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl

# Get base directory
BASE_DIR = Path(__file__).parent.parent.parent

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Trade GPT"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "AI-Powered Trading Bot with News Analysis"
    
    # CORS Configuration
    CORS_ORIGINS: List[AnyHttpUrl] = []
    
    # Tavily API Configuration
    TAVILY_API_KEY: str = ""  # Set default empty string
    TAVILY_API_BASE_URL: str = "https://api.tavily.com/v1"
    TAVILY_SEARCH_MAX_RESULTS: int = 10
    
    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "allow"  # Allow extra fields in env file

@lru_cache()
def get_settings() -> Settings:
    """
    Create cached instance of settings to avoid reading .env file multiple times
    """
    return Settings()

settings = get_settings()