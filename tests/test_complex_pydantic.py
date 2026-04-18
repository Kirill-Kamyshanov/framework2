from typing import Optional

from pydantic import BaseModel, Field, field_validator, ValidationError

from services.reqres_in.users.delete_user import DeleteUser
from services.reqres_in.users.get_user import GetUser
from services.reqres_in.users.patch_update import UpdateUser
from services.reqres_in.users.post_create import CreateUser
from faker import Faker
from datetime import datetime

fake = Faker()


class TestCrudOperations:

    def test_create_user_with_pydantic(self, env_config):
        class CreateUserRequest(BaseModel):
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

        # Генерация тестовых данных
        test_user = CreateUserRequest()

        # Создание юзера
        response = CreateUser(env_config).create_user(name=test_user.name, job=test_user.job)
        assert response.status_code == 201, f'Incorrect response code: {response.status_code}'

        # Валидация тела ответа
        response = CreateUserResponse(**response.json())
        assert response.name == test_user.name, f'Response name is {response.name}. Expected: {test_user.name}'
        assert response.job == test_user.job, f'Response job is {response.job}. Expected: {test_user.job}'

    def test_get_user_with_pydantic(self, env_config):
        class UserResponse(BaseModel):
            id: int = Field(gt=0)
            email: str
            first_name: str
            last_name: str
            avatar: str

        # тут юзера не стал генерить, т.к. в тестовом апи он не создаётся
        user_id = 2
        response = GetUser(env_config).get_user(2)
        assert response.status_code == 200, f'Incorrect response code: {response.status_code}'
        full_response_json = response.json()

        try:
            UserResponse(**full_response_json["data"])
            print(f'Validation user {user_id} succeeded.')
        except ValidationError as e:
            print(f'Validation user {user_id} failed.')

    def test_update_user_with_pydantic(self, env_config):
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

        # Создание тестового юзера (в тестовом апи это происходит понарошку,
        # Т.к. потом нельзя получить его данные через GET запрос). Но я сделал вид, что создал
        create_response = CreateUser(env_config).create_user(
            name=fake.name(),
            job=fake.job()
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

    def test_delete_user_with_pydantic(self, env_config):
        # Создание тестового юзера (типо)
        create_response = CreateUser(env_config).create_user(
            name=fake.name(),
            job=fake.job()
        )
        user_id = create_response.json()['id']

        # Удаление юзера
        response = DeleteUser(env_config).delete(user_id)
        assert response.status_code == 204, f'Incorrect response code: {response.status_code}'

        # Проверка, что юзер удалён
        response = GetUser(env_config).get_user(user_id)
        assert response.status_code == 404, f'Incorrect response code: {response.status_code}'
