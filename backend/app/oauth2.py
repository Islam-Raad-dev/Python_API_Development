import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from . import schemas

oauth2_schemas = OAuth2PasswordBearer(tokenUrl="login")

# -------------------------------------------------------------------------

SECRET_KEY = os.getenv("SECRET_KEY_FRO_JWT","fallback_secret_key_for_dev_only")

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# -------------------------------------------------------------------------


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp" : expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=[ALGORITHM])

# -------------------------------------------------------------------------

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data
# -------------------------------------------------------------------------

def get_current_user(token: str = Depends(oauth2_schemas)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate crecredentials ", headers={"WWW-Authenticate" : "Bearer"}
    )

    return verify_access_token(token=token, credentials_exception=credentials_exception)