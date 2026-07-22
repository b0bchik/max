from pydantic import BaseModel, EmailStr


class PublicUser(BaseModel):
    username: str
    email: EmailStr
    password: str

    model_config = {"from_attributes": True}


class PublicPost(BaseModel):
    title: str
    content: str

    model_config = {"from_attributes": True}

class PublicVote(BaseModel):
    post_id: int
    dir: int