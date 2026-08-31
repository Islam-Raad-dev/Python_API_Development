from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import engine, get_db

# -------------------------------------------------------------------------

models.Base.metadata.create_all(bind=engine)


# -------------------------------------------------------------------------

router = APIRouter()

# -------------------------------------------------------------------------


@router.get("/posts", response_model=list[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):  # noqa: B008
    post = db.query(models.Post).all()
    return post


# -------------------------------------------------------------------------


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):  # noqa: B008

    post_data = post.model_dump()
    new_post = models.Post(**post_data)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# -------------------------------------------------------------------------


@router.get("/posts/{id}", response_model=schemas.Post)
async def get_post(id: int, db: Session = Depends(get_db)):  # noqa: B008

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    return post


# -------------------------------------------------------------------------


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):  # noqa: B008

    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post at id {id} is not found",
        )

    deleted_post.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# -------------------------------------------------------------------------


@router.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):  # noqa: B008

    post_query = db.query(models.Post).filter(models.Post.id == id)

    update_post = post_query.first()

    if update_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    post_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()
