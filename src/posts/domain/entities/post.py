from typing import Literal, Sequence

from pydantic import BaseModel, Field
from pydantic.types import Decimal


class Post(BaseModel):
    alias: str
    text: str
    id: str

    class Config:
        orm_mode = False
