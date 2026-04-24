from typing import List
from pydantic import BaseModel, Field, HttpUrl



class ResourceData(BaseModel):
    """данные ресурса с полями id, name, year, color, pantone_value"""
    id: int = Field(gt=0)
    name: str = Field(min_length=2, max_length=30)
    year: int = Field(gt=0)
    color: str = Field(pattern=r'^#[0-9a-fA-F]{3,8}$')
    pantone_value: str = Field(pattern=r'^\d{2}-\d{4}$')


class Support(BaseModel):
    """Вспомогательный класс для валидации объекта support"""
    url: HttpUrl
    text: str



class SingleResourceResponse(BaseModel):
    """Ответ при получении одного ресурса"""
    data: ResourceData
    support: Support



class ResourcesListResponse(BaseModel):
    """Ответ при получении списка ресурсов"""
    data: List[ResourceData]
    support: Support
    page: int = Field(gt=0)
    per_page: int = Field(gt=0)
    total: int = Field(gt=0)
    total_pages: int = Field(gt=0)