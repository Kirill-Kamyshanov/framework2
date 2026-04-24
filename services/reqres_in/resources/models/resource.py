from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, HttpUrl, field_validator
from faker import Faker



class ResourceData(BaseModel):
    """данные ресурса с полями id, name, year, color, pantone_value"""
    id: int = Field(gt=0)
    name: str
    year: int = Field(gt=0)
    color: str = Field(pattern=r'^#[0-9a-fA-F]{6}$')
    pantone_value: str

#     "pantone_value": "15-4020"





class SingleResourceResponse(BaseModel):
    """Ответ при получении одного ресурса"""



class ResourcesListResponse(BaseModel):
    """Ответ при получении списка ресурсов"""