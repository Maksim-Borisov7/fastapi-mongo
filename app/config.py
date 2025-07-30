from typing import ClassVar
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    MONGO_HOST: str = Field(env='MONGO_HOST')
    MONGO_PORT: int = Field(env='MONGO_PORT')
    MONGO_DB: str = Field(env='MONGO_DB')
    ADMIN_PASSWORD: str = Field(env='ADMIN_PASSWORD')
    BASE_DIR: ClassVar[Path] = Path(__file__).parent

    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 15
    DEBUG: bool = Field(True)
    QUEUE_ORDERS: str = Field(env='QUEUE_ORDERS')
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True)


settings = AppConfig()
