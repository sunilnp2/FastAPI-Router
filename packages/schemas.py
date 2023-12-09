from pydantic import BaseModel


class BlogBase(BaseModel):
    title : str
    description : str
   


class BlogCreate(BlogBase):
    is_active : bool


class BlogUpdate(BlogBase):
    pass


class Blog(BlogBase):
    id : int
    class Config:
        orm_mode = True

# pydantic model for User 

class UserBase(BaseModel):
    email : str

class UserCreate(UserBase):
    password : str 


class UserLogin(UserBase):
    password : str 

class User(UserBase):
    id: int
    password : str
    is_active : bool

