from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    APP_NAME: str = "NEXUS AI Operating System"
    VERSION: str = "0.1.0"

    DEBUG: bool = True

    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    LOG_DIR: Path = BASE_DIR / "logs"
    DOCS_DIR: Path = BASE_DIR / "docs"


settings = Settings()