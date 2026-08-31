# 6:33:00


from fastapi import FastAPI

from . import models
from .database import engine
from .routers import post, user

# -------------------------------------------------------------------------

models.Base.metadata.create_all(bind=engine)

# -------------------------------------------------------------------------

app = FastAPI()

# -------------------------------------------------------------------------

app.include_router(user.router)
app.include_router(post.router)

# -------------------------------------------------------------------------


@app.get("/")
async def root():           
    return {"message" : " Islam Raad API "}   

