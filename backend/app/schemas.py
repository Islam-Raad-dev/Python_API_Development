from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, conint

# -------------------------------------------------------------------------


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# -------------------------------------------------------------------------

class PostCreate(PostBase):
    pass

# -------------------------------------------------------------------------

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

# -------------------------------------------------------------------------

class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserOut
    
    class Config:
        model_config = ConfigDict(from_attributes=True)

# -------------------------------------------------------------------------

class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)



    class Config:
        model_config = ConfigDict(from_attributes=True)

# -------------------------------------------------------------------------

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

# -------------------------------------------------------------------------

class Token(BaseModel):
    access_token: str
    token_type: str

# -------------------------------------------------------------------------

class TokenData(BaseModel):
    id: int | str | None = None

# -------------------------------------------------------------------------

class Vote(BaseModel):
    post_id: int
    user_id: int
    dir: conint(ge=0, le=1) # type: ignore