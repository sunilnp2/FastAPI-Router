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

