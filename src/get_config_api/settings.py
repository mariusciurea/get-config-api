from ctypes import HRESULT

from pydantic_settings import BaseSettings
from pathlib import Path
from argon2 import PasswordHasher
from dotenv import load_dotenv




ph = PasswordHasher()

class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent
    PROJECT_DIR: Path = BASE_DIR.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    USER: dict = {
        "admin": {
            "username": "admin",
            "password": ph.hash("admin"),
        }
    }
    SECRET_KEY: str = "123423rsdfsd3w45345"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


class DBSettings(BaseSettings):
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME:str = "devgetconfig"


def get_settings() -> Settings:
    """Return settings object"""

    return Settings()


def get_db_settings() -> DBSettings:
    """Return db settings object"""

    return DBSettings()


load_dotenv(get_settings().PROJECT_DIR / ".env")


if __name__ == "__main__":
    import requests

    token = requests.post("localhost:3333/auth/token", data={"username": "admin", "password": "admin"})

    config_data = requests.get("localhost:3333/config", headers={"Authorization": f"Bearer {token.json()['access_token']}"})

    print(config_data.json())
