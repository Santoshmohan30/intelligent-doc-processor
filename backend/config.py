"""
Application configuration management
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""

    # Application
    app_name: str = "Intelligent Document Processor"
    version: str = "0.1.0"
    debug: bool = True

    # API
    api_prefix: str = "/api/v1"

    # Database
    database_url: str = "sqlite:///./doc_processor.db"

    # ML Models
    model_path: str = "./ml-pipeline/models"

    # OCR
    tesseract_path: str = "/usr/bin/tesseract"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
