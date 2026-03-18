"""Helper functions for authentication"""
from charset_normalizer import from_path
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from jose import jwt
from starlette import status

from src.get_config_api.settings import get_settings, ph

from src.get_config_api.auth.scheme import USER_AUTH_SCHEME
from .jwt_utils import decode_token, get_token_sub

from src.get_config_api.databse.db_models import User
from src.get_config_api.databse.db import get_db, SessionLocal


settings = get_settings()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if the password matches the hashed password"""

    return ph.verify(hashed_password, plain_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create an access token"""

    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def authenticate_user(username: str, password: str, db: Session) -> bool:
    """Authenticate a user"""

    try:
        # user = settings.USER[username]
        user = db.query(User).filter(User.username == username).first()
    except KeyError:
        return False

    if not user:
        return False

    try:
        # verify_password(password, user["password"])
        verify_password(password, user.hashed_password)
    except VerifyMismatchError:
        return False

    return user


def get_user_from_token(db:Session = Depends(get_db), token: str = Depends(USER_AUTH_SCHEME)) -> User:
    payload = decode_token(token)
    sub = get_token_sub(payload)

    # user = settings.USER[sub]
    user = db.query(User).filter(User.username == sub).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
