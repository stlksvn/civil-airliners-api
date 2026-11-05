import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ALLOWED_ENVIRONMENTS = ("dev", "test", "prod")
DEFAULT_ENVIRONMENT = "dev"

BASE_DIR = Path(__file__).resolve().parent.parent
ENVIRONMENT = os.getenv("ENVIRONMENT", DEFAULT_ENVIRONMENT).strip().lower()
if ENVIRONMENT not in ALLOWED_ENVIRONMENTS:
    ENVIRONMENT = DEFAULT_ENVIRONMENT

ENV_FILE = BASE_DIR / f".env.{ENVIRONMENT}"


class Settings(BaseSettings):
    app_env: str = DEFAULT_ENVIRONMENT
    feature_flag: bool = False

    db_user: str = "avia"
    db_password: str = "avia_password"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "avia_metrics"

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
