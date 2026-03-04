from ctypes import HRESULT

from pydantic_settings import BaseSettings
from pathlib import Path
from argon2 import PasswordHasher


ph = PasswordHasher()

class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent
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


def get_settings() -> Settings:
    """Return settings object"""

    return Settings()


if __name__ == "__main__":
    import requests

    token = requests.post("localhost:3333/auth/token", data={"username": "admin", "password": "admin"})

    config_data = requests.get("localhost:3333/config", headers={"Authorization": f"Bearer {token.json()['access_token']}"})

    print(config_data.json())
