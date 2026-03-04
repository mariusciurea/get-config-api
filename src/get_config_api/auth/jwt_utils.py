from charset_normalizer import from_path
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from src.get_config_api.settings import get_settings


settings = get_settings()


def decode_token(token: str) -> dict:
    """Decode JWT Token"""
    try:
        return jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    except JWTError:
        raise  HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

def get_token_sub(payload: dict) -> dict:
    """Get JWT Token subject claim"""

    subject = payload.get("sub")
    if not subject:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    return subject



