from services.reqres_in.users.post_create import CreateUser
from services.reqres_in.users.models.user import CreateUserRequest, CreateUserResponse


class TestCreateUser:
    def test_create_user_with_pydantic(self, env_config):
        # Генерация тестовых данных
        test_user = CreateUserRequest()
        # Создание юзера
        response = CreateUser(env_config).create_user(**test_user.model_dump())
        assert response.status_code == 201, f'Incorrect response code: {response.status_code}'

        # Валидация тела ответа
        validated_response = CreateUserResponse(**response.json())
        assert validated_response.name == test_user.name, f'Response name is {validated_response.name}. Expected: {test_user.name}'
        assert validated_response.job == test_user.job, f'Response job is {validated_response.job}. Expected: {test_user.job}'
