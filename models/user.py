from typing import List
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, HttpUrl, field_validator
from faker import Faker

fake = Faker()

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


class CreateUserRequest(BaseModel):
    name: str = Field(default_factory=fake.name, min_length=2, max_length=25)
    job: str = Field(default_factory=fake.job)

    @field_validator('name')
    @classmethod
    def name_validator(cls, v):
        if not v.istitle():
            raise ValueError(f'{v} does not start with a capital letter')


class CreateUserResponse(BaseModel):
    name: str
    job: str
    id: str
    createdAt: datetime

    @field_validator('id')
    @classmethod
    def id_validator(cls, v):
        if int(v) < 1:
            raise ValueError(f'Error:id < 1 ({v})')
        return v


class UpdateUserRequest(BaseModel):
    name: Optional[str] = Field(default_factory=fake.name, min_length=2, max_length=25)
    job: Optional[str] = Field(default_factory=fake.job)



class UpdateUserResponse(BaseModel):
    name: str
    job: str
    updatedAt: datetime