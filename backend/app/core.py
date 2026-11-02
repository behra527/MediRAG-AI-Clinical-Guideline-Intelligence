import os
from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE = Path(__file__).resolve().parents[2]
class Settings(BaseSettings):
    openrouter_api_key: str = ""
    openrouter_model: str = "openai/gpt-4o-mini"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    cors_origins: str = "http://localhost:5173"
    max_upload_mb: int = 15
    model_config = SettingsConfigDict(env_file=str(BASE / '.env'), extra='ignore')

@lru_cache
def settings(): return Settings()

STORAGE = BASE / 'backend' / 'storage'
STORAGE.mkdir(parents=True, exist_ok=True)
