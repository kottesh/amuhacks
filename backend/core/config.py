import os
from pydantic import AnyHttpUrl, field_validator 
from pydantic_settings import BaseSettings
from typing import List, Union
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "quid"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    DATABASE_URL: str

    OLLAMA_API_URL: AnyHttpUrl
    OLLAMA_MODEL: str = "granite3.2"

    CLIENT_ORIGIN: str | None = None
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode='before')
    def assemble_cors_origins(cls, v: Union[str, List[str]], values: dict) -> Union[List[str], str]:
        """Parse CORS origins from environment variable or CLIENT_ORIGIN"""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v

        client_origin = values.get("CLIENT_ORIGIN")
        if client_origin:
            return [client_origin]

        return []

    class Config:
        case_sensitive = True

        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
