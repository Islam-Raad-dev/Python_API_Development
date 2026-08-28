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
    return {"data": my_post}


def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p
def find_index_post(id):
    for i, p in enumerate(my_post):
        if p["id"] == id:
            return i


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
   
    my_post.append(post.dict())
    return {"data": post}


@app.get("/posts/{id}")
async def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return {"data" : post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post at id {id} is not found")
    
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

