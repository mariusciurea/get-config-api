from datetime import timedelta

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status

from src.get_config_api.auth.auth import authenticate_user, create_access_token
from src.get_config_api.settings import get_settings


settings = get_settings()

auth_router = APIRouter(
    prefix="/auth",
)

@auth_router.post("/token", tags=["auth"])
def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    print(username, password)
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(
        data={"sub": username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": access_token, "token_type": "bearer"}