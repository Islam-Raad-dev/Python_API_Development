# 5:04:00


from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.params import Body  # noqa: F401
from psycopg2.extras import RealDictCursor  # noqa: F401
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db

# -------------------------------------------------------------------------

models.Base.metadata.create_all(bind=engine)

# -------------------------------------------------------------------------

load_dotenv()

# -------------------------------------------------------------------------

app = FastAPI()

# -------------------------------------------------------------------------

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# -------------------------------------------------------------------------

@app.get("/")
async def root():           
    return {"message" : " Islam Raad API "}   

# -------------------------------------------------------------------------

@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):  # noqa: B008
    post = db.query(models.Post).all()
    return {"data": post}

# -------------------------------------------------------------------------

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post, db: Session = Depends(get_db)):  # noqa: B008

    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}

#-------------------------------------------------------------------------

@app.get("/posts/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):  # noqa: B008

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    
    return {"data" : post}

# -------------------------------------------------------------------------

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):  # noqa: B008

    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() is None:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post at id {id} is not found")
    
    deleted_post.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# -------------------------------------------------------------------------

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
async def update_post(id: int, post: Post, db: Session = Depends(get_db)):  # noqa: B008


    post_query = db.query(models.Post).filter(models.Post.id == id)

    update_post = post_query.first()

    if update_post is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    post_query.update(post.dict() ,synchronize_session=False)

    db.commit()

    return {"data": post_query.first()}