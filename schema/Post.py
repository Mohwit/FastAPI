from pydantic import BaseModel

from typing import Optional


class Post(BaseModel):
    title: str
    content: str
    # id: int
    published: bool = True
    rating: Optional[int] = None
