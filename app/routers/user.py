from fastapi import (  # noqa: F401
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import engine, get_db

# -------------------------------------------------------------------------

models.Base.metadata.create_all(bind=engine)

# -------------------------------------------------------------------------

router = APIRouter(prefix="/users", tags=["Users"])

# -------------------------------------------------------------------------


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):  # noqa: B008

    user_data = user.model_dump()
    user_data["password"] = utils.hash_password(user.password)

    new_user = models.User(**user_data)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# -------------------------------------------------------------------------


@router.get("/{id}", response_model=schemas.UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):  # noqa: B008

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} was not found",
        )

    return user
