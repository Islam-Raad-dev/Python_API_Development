from fastapi import (  # noqa: F401
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas, utils
from ..database import engine, get_db

# -------------------------------------------------------------------------

models.Base.metadata.create_all(bind=engine)

# -------------------------------------------------------------------------

router = APIRouter(prefix="/votes", tags=["Votes"])

# -------------------------------------------------------------------------


@router.post("/", status_code=status.HTTP_200_OK)
async def like_post():
    pass