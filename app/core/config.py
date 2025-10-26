import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path, override=False)

class Config:
    SERVER_HOST = os.getenv("SERVER_HOST")
    SERVER_PORT = int(os.getenv("SERVER_PORT"))
    
    IMAP_HOST = os.getenv("IMAP_HOST")
    USERNAME = os.getenv("USERNAME")
    APP_PASSWORD = os.getenv("APP_PASSWORD")

    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    ENV = os.getenv("ENV", "development")

    CREDENTIALS_PATH = BASE_DIR / "credentials.json"
    TOKEN_PATH = BASE_DIR / "token.json"
    SCOPES = ["https://mail.google.com/"]

    REQUIRED_VARS = ["SERVER_HOST", "SERVER_PORT", "IMAP_HOST", "USERNAME", "APP_PASSWORD"]

    @classmethod
    def validate(cls):
        # Checks if all variables are set
        missing = [var for var in cls.REQUIRED_VARS if getattr(cls, var) is None]
        if missing:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing)}"
                )

Config.validate()