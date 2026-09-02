from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, models, oauth2, utils

# -------------------------------------------------------------------------

models.Base.metadata.create_all(bind=database.engine)

# -------------------------------------------------------------------------

router = APIRouter(tags=["Authentication"])

# -------------------------------------------------------------------------


@router.post("/login", status_code=status.HTTP_200_OK)

async def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):  # noqa: B008

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    
    if not utils.verify_password(user.password, user_credentials.password):

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token" : access_token, "token_type" : "bearer"}