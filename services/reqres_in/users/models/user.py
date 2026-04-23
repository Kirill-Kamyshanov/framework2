from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, HttpUrl, field_validator
from faker import Faker


fake = Faker()



class Support(BaseModel):
    """вспомогательная структура с полями url и text"""
    url: HttpUrl
    text: str



class UserData(BaseModel):
    """данные пользователя с полями id, email, first_name, last_name, avatar"""
    id: int = Field(gt=0)
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl


class SingleUserResponse(BaseModel):
    """ответ при получении одного пользователя"""
    data: UserData
    support: Support


class UsersListResponse(BaseModel):
    """ответ при получении списка пользователей"""
    page: int = Field(gt=0)
    per_page: int = Field
    total: int = Field(ge=0)
    total_pages: int = Field(ge=0)
    data: List[UserData]
    support: Support


class CreateUserRequest(BaseModel):
    """запрос на создание пользователя"""

    class CreateUserRequest(BaseModel):
        name: str = Field(default_factory=fake.name, min_length=2, max_length=25)
        job: str = Field(default_factory=fake.job)

        @field_validator('name')
        @classmethod
        def name_validator(cls, v):
            if not v.istitle():
                raise ValueError(f'{v} does not start with a capital letter')



class CreateUserResponse(BaseModel):
    """ответ при создании пользователя"""
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
    """запрос на обновление пользователя (с Optional полями)"""
    # name: Optional[str] = None
    # job: Optional[str] = None
    name: Optional[str] = Field(default_factory=fake.name, min_length=2, max_length=25)
    job: Optional[str] = Field(default_factory=fake.job)




class UpdateUserResponse(BaseModel):
    """ответ при обновлении пользователя"""
    name: Optional[str]
    job: Optional[str]
    updatedAt: datetime

