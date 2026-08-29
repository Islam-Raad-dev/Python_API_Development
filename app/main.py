# 3:55:00

import os
import time
from typing import Optional

import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body  # noqa: F401
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None  # noqa: UP045


while True:
    try:
        load_dotenv()

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

my_post = [
    {"title": "Nigga", "content": "Ass Hole", "id": 1},
    {"title": "White", "content": "Great Man", "id": 2},
    {"title": "Arab", "content": "Gay Man", "id": 3}
]

# -------------------------------------------------------------------------


@app.get("/")
async def root():           
    return {"message" : " Islam Raad API "}   

# -------------------------------------------------------------------------


@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


# -------------------------------------------------------------------------


def find_index_post(id):
    for i, p in enumerate(my_post):
        if p["id"] == id:
            return i
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
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, str((id),))
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
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,
                    str((id),))
    index = cursor.fetchone()
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post at id {id} is not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# -------------------------------------------------------------------------


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
async def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post at id {id} is not found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_post[index] = post_dict
    return {"data" : post_dict}
