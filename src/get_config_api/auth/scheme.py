
from fastapi.security import OAuth2PasswordBearer, OAuth2


USER_AUTH_SCHEME = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    scheme_name="UserPasswordBearer",
)