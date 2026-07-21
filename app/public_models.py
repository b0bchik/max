from pydantic import BaseModel, EmailStr


class PublicUser(BaseModel):
    username: str
    email: EmailStr
    password: str

    model_config = {"from_attributes": True}


class PublicPost(BaseModel):
    id: int | None = None
    title: str
    content: str
    owner: PublicUser | None = None

    model_config = {"from_attributes": True}

class PublicVote(BaseModel):
    post_id: int
    dir: int