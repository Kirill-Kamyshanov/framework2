from pydantic import BaseModel, Field, field_validator
from typing import Optional
from faker import Faker
from datetime import datetime

from services.reqres_in.users.patch_update import UpdateUser
from services.reqres_in.users.post_create import CreateUser

fake = Faker()


class UpdateUserRequest(BaseModel):
    name: Optional[str] = Field(default_factory=fake.name)
    job: Optional[str] = Field(default_factory=fake.job)

    @field_validator('name')
    @classmethod
    def name_validation(cls, v):
        if not 2 <= len(v) <= 25:
            raise ValueError(f'name must be between 2 and 25 characters long')
        return v


class UpdateUserResponse(BaseModel):
    name: str
    job: str
    updatedAt: datetime


def test_update_user(env_config):
    # Создание тестового юзера
    create_response = CreateUser(env_config).create_user(
        name="John Doe",
        job="QA Engineer"
    )
    user_id = create_response.json()['id']

    # Обновление тестового юзера
    new_data = UpdateUserRequest()
    # так можно сгенерить данные, если нужно обновить одно поле
    # new_data = UpdateUserRequest(name=fake.name()).model_dump(exclude_unset=True)
    update_response = UpdateUser(env_config).update(
        user_id=user_id,
        name=new_data.name,
        job=new_data.job
    )
    assert update_response.status_code == 200

    # Валидация тела ответа после обновления
    update_response = UpdateUserResponse(**update_response.json())
    assert update_response.name == new_data.name, f'{update_response.name} != {new_data.name}'
    assert update_response.job == new_data.job, f'{update_response.job} != {new_data.job}'
