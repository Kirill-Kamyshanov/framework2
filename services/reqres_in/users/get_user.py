from services.base_api import BaseAPI
from services.reqres_in.users.models.user import SingleUserResponse
from utils.helper import helper

class GetUser(BaseAPI):
    def __init__(self, env_config):
        """
        Args:
            env_config (EnvironmentConfig): Конфигурация окружения из фикстуры
        """
        super().__init__(base_url=env_config.reqres_url, api_key=env_config.reqres_api_key)


    def get_user(self, user_id: int):
        """Получение пользователя по ID.

               Args:
                   user_id (int): ID пользователя

               Returns:
                   requests.Response: Ответ от сервера
               """
        response = self.session.get(f"{self.base_url}/users/{user_id}")

        # Прикрепляем ответ в JSON к отчёту
        helper.attach_response(response)

        # Валидация ответа по схеме
        validated = SingleUserResponse.model_validate(response.json())

        return response, validated


def assert_user_data_is_correct(response, validated_data, user_id):
    assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}: {response.text}"
    assert validated_data.data.id == user_id, f"Ожидался Id '{user_id}', но получен '{validated_data.data.id}'"