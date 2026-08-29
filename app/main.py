# 4:41:00

import os
import time
from typing import Optional

import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body  # noqa: F401
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

from . import models  # noqa: F401
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# -------------------------------------------------------------------------

load_dotenv()

# -------------------------------------------------------------------------

app = FastAPI()

# -------------------------------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------------------------------------------------


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None  # noqa: UP045

# -------------------------------------------------------------------------

while True:
    try:

        connect = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
            cursor_factory=RealDictCursor
            )

        cursor = connect.cursor()
        print("Connect to Database was successful")
        break


    except Exception as error:  # noqa: BLE001
        print("Connect to Database was Failed")
        print(f"The Error Was {error}")
        time.sleep(3)



# -------------------------------------------------------------------------


@app.get("/")
async def root():           
    return {"message" : " Islam Raad API "}   


# -------------------------------------------------------------------------


@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    return {"data": cursor.fetchall()}


# -------------------------------------------------------------------------


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):

    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))

    new_post = cursor.fetchone()
    connect.commit()

    return {"data": new_post}

#-------------------------------------------------------------------------


@app.get("/posts/{id}")
async def get_post(id: int):

    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (id,))

    post = cursor.fetchone()

    if not post:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    
    return {"data" : post}

# -------------------------------------------------------------------------


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):

    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (id,))
    
    deleted_post = cursor.fetchone()
    connect.commit()

    if deleted_post is None:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post at id {id} is not found")


    return Response(status_code=status.HTTP_204_NO_CONTENT)

# -------------------------------------------------------------------------


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
async def update_post(id: int, post: Post):

    cursor.execute(
                    """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""",
                    (post.title, post.content, post.published, id))

    updated_post = cursor.fetchone()
    connect.commit()

    if updated_post is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )

    return {"data": updated_post}