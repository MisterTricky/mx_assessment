import enum
from pathlib import Path
from tempfile import gettempdir
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL
import os

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = os.getenv("BACKEND_HOST", "127.0.0.1")
    port: int = int(os.getenv("BACKEND_PORT", "8000"))
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO
    # Variables for the database
    db_host: str = os.getenv("BACKEND_DB_HOST", "localhost")
    db_port: int = int(os.getenv("BACKEND_DB_PORT", "5432"))
    db_user: str = os.getenv("BACKEND_DB_USER", "backend")
    db_pass: str = os.getenv("BACKEND_DB_PASS", "backend")
    db_base: str = os.getenv("BACKEND_DB_BASE", "admin")
    db_echo: bool = False

    calendarific_api_key: str = os.environ.get("BACKEND_CALENDARIFIC_API_KEY")

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="BACKEND_",
        env_file_encoding="utf-8",
    )


settings = Settings()
