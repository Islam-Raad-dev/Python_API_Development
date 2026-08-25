# 1:09:30

from typing import Optional

from fastapi import FastAPI
from fastapi.params import Body  # noqa: F401
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None  # noqa: UP045

@app.get("/")
async def root():           
    return {"message" : " Islam Raad API "}   


@app.get("/posts")
async def get_posts():
    return {"Data": " This is Your Post API "}


@app.post("/posts")
async def create_posts(post: Post):
    print(post.published)
    return {"Data" : post}

