from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parents[2] / ".env")

    mongo_db: str
    mongo_name: str
    weather_api_key: str
    grpc_api_key: str


settings = Settings()
