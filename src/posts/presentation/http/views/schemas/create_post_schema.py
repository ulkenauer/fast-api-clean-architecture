from pydantic import BaseModel


class CreatePostSchema(BaseModel):
    alias: str
    text: str
    user_id: str
