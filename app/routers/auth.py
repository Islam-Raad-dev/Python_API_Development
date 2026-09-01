from fastapi import (  # noqa: F401
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)
from sqlalchemy.orm import Session

from .. import database, models, schemas, utils

# -------------------------------------------------------------------------

models.Base.metadata.create_all(bind=database.engine)

# -------------------------------------------------------------------------

router = APIRouter(tags=["Authentication"])

# -------------------------------------------------------------------------


@router.post("/login", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)

async def login_user(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):  # noqa: B008

    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials",
        )

    return user