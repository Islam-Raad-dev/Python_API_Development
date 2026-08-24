from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():           
    return {"message" : " Islam Raad API "}   


@app.get("/posts")
async def get_posts():
    return {"Data": " This is Your Post API "}
