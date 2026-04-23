from services.base_api import BaseAPI
from services.reqres_in.users.models.user import CreateUserResponse
from utils.helper import helper


class CreateUser(BaseAPI):

    def __init__(self, env_config):
        super().__init__(base_url=env_config.reqres_url, api_key=env_config.reqres_api_key)

    def create_user(self, name: str, job: str, validate: bool = True):
        """Создание нового пользователя.

        Args:
            name (str): Имя пользователя
            job (str): Должность пользователя
        """
        data = {"name": name, "job": job}
        response = self.session.post(f"{self.base_url}/users", json=data)

        # Прикрепляем ответ в JSON к отчёту
        helper.attach_response(response)

        validated = None
        if validate:
            validated = CreateUserResponse.model_validate(response.json())
        return response, validated

def assert_user_created_correctly(response, validated_data, expected_name, expected_job):
    assert response.status_code == 201, f"Ожидался статус 201, но получен {response.status_code}: {response.text}"
    assert validated_data.name == expected_name, f"Ожидалось имя '{expected_name}', но получено '{validated_data.name}'"
    assert validated_data.job == expected_job, f"Ожидалась должность '{expected_job}', но получено '{validated_data.job}'"
    assert validated_data.id is not None, "Поле 'id' отсутствует или пустое"
    assert validated_data.createdAt is not None, "Поле 'createdAt' отсутствует или пустое"