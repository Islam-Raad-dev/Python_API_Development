# 1:09:30

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel  # noqa: F401

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str

@app.get("/")
async def root():           
    return {"message" : " Islam Raad API "}   


@app.get("/posts")
async def get_posts():
    return {"Data": " This is Your Post API "}


@app.post("/createpost")
async def create_posts(nwe_post: Post):
    print(nwe_post.title)
    return {"Data" : "New Post"}

