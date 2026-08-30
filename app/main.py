# 6:04:00


from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db

# -------------------------------------------------------------------------

models.Base.metadata.create_all(bind=engine)

# -------------------------------------------------------------------------

load_dotenv()

# -------------------------------------------------------------------------

app = FastAPI()

# -------------------------------------------------------------------------

@app.get("/")
async def root():           
    return {"message" : " Islam Raad API "}   

# -------------------------------------------------------------------------

@app.get("/posts",
          response_model=list[schemas.Post])

async def get_posts(db: Session = Depends(get_db)):  # noqa: B008
    post = db.query(models.Post).all()
    return post

# -------------------------------------------------------------------------

@app.post("/posts",
            status_code=status.HTTP_201_CREATED,
            response_model=schemas.Post)

async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):  # noqa: B008


    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

#-------------------------------------------------------------------------

@app.get("/posts/{id}",
          response_model=schemas.Post)

async def get_post(id: int, db: Session = Depends(get_db)):  # noqa: B008

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    
    return post

# -------------------------------------------------------------------------

@app.delete("/posts/{id}",
             status_code=status.HTTP_204_NO_CONTENT)

async def delete_post(id: int, db: Session = Depends(get_db)):  # noqa: B008

    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() is None:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post at id {id} is not found")
    
    deleted_post.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# -------------------------------------------------------------------------

@app.put("/posts/{id}",
          status_code=status.HTTP_200_OK,
          response_model=schemas.Post)

async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):  # noqa: B008


    post_query = db.query(models.Post).filter(models.Post.id == id)

    update_post = post_query.first()

    if update_post is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    post_query.update(post.dict() ,synchronize_session=False)

    db.commit()

    return post_query.first()

# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------

@app.post("/users",
            status_code=status.HTTP_201_CREATED,
            response_model=schemas.User)
async def create_user():
    pass
