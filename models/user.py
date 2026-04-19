from typing import List
from pydantic import BaseModel, Field, EmailStr, HttpUrl


class User(BaseModel):
    id: int = Field(gt=0)
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl


class Support(BaseModel):
    url: HttpUrl
    text: str


class PaginationResponse(BaseModel):
    page: int = Field(gt=0)
    per_page: int = Field
    total: int = Field(ge=0)
    total_pages: int = Field(ge=0)
    data: List[User]
    support: Support