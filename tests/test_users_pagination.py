from services.reqres_in.users.get_users import GetUsers
from pydantic import BaseModel, Field, EmailStr, HttpUrl, model_validator
from typing import List, Literal


class User(BaseModel):
    id: int = Field(gt=0)
    email: EmailStr
    first_name: str
    last_name: str
    avatar: str


class Support(BaseModel):
    url: HttpUrl
    text: str


class PaginationResponse(BaseModel):
    page: int = Field(gt=0)
    per_page: Literal[6]
    total: int = Field(ge=0)
    total_pages: int = Field(ge=0)
    data: List[User]
    support: Support

    @model_validator(mode='after')
    def validate_pagination(self):
        """Валидация полей пагинации"""

        if len(self.data) != self.per_page:
            raise ValueError(f'Count of users ({len(self.data)}) does not match per_page ({self.per_page})')

        if self.total != self.per_page * self.total_pages:
            raise ValueError(f'Error. total:({self.total}), total_pages:({self.total_pages}), '
                             f'per_page:{self.per_page}')

        return self


def test_users_pagination(env_config):
    page = 1
    full_response_body = GetUsers(env_config).get_users(page).json()
    validated = PaginationResponse(**full_response_body).model_dump()

    assert validated['page'] == page, f'{validated['page']} != {page}'
