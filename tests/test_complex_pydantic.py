import allure
import pytest

from services.reqres_in.users.delete_user import DeleteUser
from services.reqres_in.users.get_user import GetUser
from services.reqres_in.users.patch_update import UpdateUserPatch
from services.reqres_in.users.post_create import CreateUser
from services.reqres_in.users.models.user import CreateUserRequest, CreateUserResponse, UserData, UpdateUserRequest, UpdateUserResponse
from faker import Faker

fake = Faker()

class TestCrudOperations:

    def test_create_user_with_pydantic(self, env_config):
        # Генерация тестовых данных
        test_user = CreateUserRequest()

        # Создание юзера
        response = CreateUser(env_config).create_user(**test_user.model_dump())
        assert response.status_code == 201, f'Incorrect response code: {response.status_code}'

        # Валидация тела ответа
        validated_response = CreateUserResponse(**response.json())
        assert validated_response.name == test_user.name, \
            f'Response name is {validated_response.name}. Expected: {test_user.name}'
        assert validated_response.job == test_user.job, \
            f'Response job is {validated_response.job}. Expected: {test_user.job}'


    def test_get_user_with_pydantic(self, env_config):
        user_id = 2
        response = GetUser(env_config).get_user(user_id)
        assert response.status_code == 200, f'Incorrect response code: {response.status_code}'
        full_response_json = response.json()
        UserData(**full_response_json["data"])
        print(f'Validation user {user_id} succeeded.')


    def test_update_user_with_pydantic(self, env_config):
        create_response = CreateUser(env_config).create_user(**CreateUserRequest().model_dump())
        user_id = create_response.json()['id']

        # Обновление тестового юзера
        new_data = UpdateUserRequest()
        update_response = UpdateUserPatch(env_config).update(
            user_id=user_id, **new_data.model_dump()
        )
        assert update_response.status_code == 200

        # Валидация тела ответа после обновления
        validated_update_response = UpdateUserResponse(**update_response.json(exclude_none=True))
        assert validated_update_response.name == new_data.name,f'{validated_update_response.name} != {new_data.name}'
        assert validated_update_response.job == new_data.job, f'{validated_update_response.job} != {new_data.job}'


    def test_delete_user_with_pydantic(self, env_config):
        # Создание тестового юзера
        create_response = CreateUser(env_config).create_user(**CreateUserRequest().model_dump())
        user_id = create_response.json()['id']

        # Удаление юзера
        response = DeleteUser(env_config).delete(user_id)
        assert response.status_code == 204, f'Incorrect response code: {response.status_code}'

        # Проверка, что юзер удалён
        response = GetUser(env_config).get_user(user_id)
        assert response.status_code == 404, f'Incorrect response code: {response.status_code}'
