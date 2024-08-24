from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    description: str
    user_id: int


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    is_blocked: bool

    class ConfigDict:
        from_attributes = True
