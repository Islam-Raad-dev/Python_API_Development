# 1:09:30

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel  # noqa: F401

app = FastAPI()

@app.get("/")
async def root():           
    return {"message" : " Islam Raad API "}   


@app.get("/posts")
async def get_posts():
    return {"Data": " This is Your Post API "}


@app.post("/createpost")
async def create_posts(payload: dict = Body):
    print(payload)
    return {"new_post" : f"title {payload['title']} content: {payload['content']}"}

