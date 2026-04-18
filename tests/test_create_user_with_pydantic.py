from pydantic import BaseModel, Field, field_validator
from services.reqres_in.users.post_create import CreateUser
from faker import Faker
from datetime import datetime

fake = Faker()


class UserRequest(BaseModel):
    name: str = Field(default_factory=fake.name)
    job: str = Field(default_factory=fake.job)

    @field_validator('name')
    @classmethod
    def name_validator(cls, v):
        if not v.istitle():
            raise ValueError(f'{v} does not start with a capital letter')
        if not (1 < len(v) < 26):
            raise ValueError(f'{v} must be between 2 and 25 characters long')
        return v


class UserResponse(BaseModel):
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


class TestCreateUser:
    def test_create_user_with_pydantic(self, env_config):
        # Генерация тестовых данных
        test_user = UserRequest()
        # Создание юзера
        response = CreateUser(env_config).create_user(name=test_user.name, job=test_user.job)
        assert response.status_code == 201, f'Incorrect response code: {response.status_code}'

        # Валидация тела ответа
        response = UserResponse(**response.json())
        assert response.name == test_user.name, f'Response name is {response.name}. Expected: {test_user.name}'
        assert response.job == test_user.job, f'Response job is {response.job}. Expected: {test_user.job}'
