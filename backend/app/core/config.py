from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Breeze-RP"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    IS_PROD: bool = False
    
    # LLM Settings (Defaults for Ollama)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/breeze.db"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache()
def get_settings() -> Settings:
    return Settings()
