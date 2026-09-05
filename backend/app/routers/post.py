from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, oauth2, schemas
from ..database import engine, get_db

# -------------------------------------------------------------------------

models.Base.metadata.create_all(bind=engine)


# -------------------------------------------------------------------------

router = APIRouter(prefix="/posts", tags=["Posts"])

# -------------------------------------------------------------------------
@router.get("/", response_model=list[schemas.PostOut])
async def get_posts(
    db: Session = Depends(get_db),  # noqa: B008
    limit: int = 10,
    skip: int = 0,
    search: str | None = None,
):
    query = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
    )

    if search:
        query = query.filter(models.Post.title.contains(search))

    return query.offset(skip).limit(limit).all()


# -------------------------------------------------------------------------


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate,
                       db: Session = Depends(get_db),  # noqa: B008
                       current_user: int = Depends(oauth2.get_current_user)
                        ):

    post_data = post.model_dump()
    new_post = models.Post(user_id=current_user.id, **post_data)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# -------------------------------------------------------------------------


@router.get("/{id}", response_model=schemas.Post)
async def get_post(id: int,
                   db: Session = Depends(get_db),  # noqa: B008
                   current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    return post


# -------------------------------------------------------------------------


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int,
    db: Session = Depends(get_db),  # noqa: B008
    current_user: models.User = Depends(oauth2.get_current_user),  # noqa: B008
):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post at id {id} is not found",
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform request action",
        )

    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# -------------------------------------------------------------------------


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
async def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),  # noqa: B008
    current_user: models.User = Depends(oauth2.get_current_user),  # noqa: B008
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform request action",
        )

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
