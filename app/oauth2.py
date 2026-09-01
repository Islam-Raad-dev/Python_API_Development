import os
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt  # noqa: F401

#SECRET_KEY
#ALGORITHM
#EXPIRATION TIME

SECRET_KEY = os.getenv("SECRET_KEY_FRO_JWT", "fallback_secret_key_for_dev_only")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt