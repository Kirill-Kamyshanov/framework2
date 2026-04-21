from pydantic import BaseModel, Field, EmailStr, HttpUrl


class User(BaseModel):
    id: int = Field(gt=0)
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl