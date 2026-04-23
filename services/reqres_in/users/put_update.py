from services.base_api import BaseAPI
from services.reqres_in.users.models.user import UpdateUserResponse
from utils.helper import helper


class UpdateUserPut(BaseAPI):
    def __init__(self, env_config):
        """
        Args:
            env_config (EnvironmentConfig): Конфигурация окружения из фикстуры
        """
        super().__init__(base_url=env_config.reqres_url, api_key=env_config.reqres_api_key)

    def update(self, user_id: int, name: str, job: str):
        """Обновление данных пользователя.

        Args:
            user_id (int): ID пользователя
            name (str): Новое имя
            job (str): Новая должность

        Returns:
            requests.Response: Ответ от сервера
        """
        data = {"name": name, "job": job}
        response = self.session.put(f"{self.base_url}/users/{user_id}", json=data)

        # Прикрепляем ответ в JSON к отчёту
        helper.attach_response(response)

        validated = UpdateUserResponse.model_validate(response.json())

        return response, validated

def assert_user_updated_put_correctly(response, validated_data, name, job):
    assert response.status_code == 200, f"Ожидался статус 201, но получен {response.status_code}: {response.text}"
    assert validated_data.name == name, f'Ожидалось name = {name}, но получено {validated_data.name}'
    assert validated_data.job == job, f'Ожидалось job = {job}, но получено {validated_data.job}'