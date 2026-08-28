# 1:52:00

from typing import Optional

from fastapi import FastAPI, HTTPException, Response, status  # noqa: F401
from fastapi.params import Body  # noqa: F401
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None  # noqa: UP045


my_post = [
    {"title": "Nigga", "content": "Ass Hole", "id": 1},
    {"title": "White", "content": "Great Man", "id": 2},
    {"title": "Arab", "content": "Gay Man", "id": 3}
]


@app.get("/")
async def root():           
    return {"message" : " Islam Raad API "}   


@app.get("/posts")
async def get_posts():
    print(my_post)
    return {"Data": my_post}


def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p

@app.post("/posts")
async def create_posts(post: Post):
    my_post.append(post.dict())
    print(my_post)
    return {"Data": post}


@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message' : f"post with id: {id} was not found"}
    return {"Data" : post}





