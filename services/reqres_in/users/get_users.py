from services.base_api import BaseAPI
from services.reqres_in.users.models.user import UsersListResponse
from utils.helper import helper

class GetUsers(BaseAPI):
    def __init__(self, env_config):
        """
        Args:
            env_config (EnvironmentConfig): Конфигурация окружения из фикстуры
        """
        super().__init__(base_url=env_config.reqres_url, api_key=env_config.reqres_api_key)


    def get_users(self, page=1):
        """Получение списка пользователей по номеру страницы

               Args:
                   page (int): номер страницы

               Returns:
                   requests.Response: Ответ от сервера
               """

        # Отправка запроса, получение ответа
        response = self.session.get(f"{self.base_url}/users?page={page}")

        # Прикрепляем ответ в JSON к отчёту
        helper.attach_response(response)

        # Валидация тела ответа
        validated = UsersListResponse.model_validate(response.json())


        return response, validated, page

def assert_users_data_is_correct(response, validated_data, page):
    assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}: {response.text}"
    assert validated_data.data is not None, f"В ответе отсутствует ключ data"
    assert validated_data.page == page, f"Ожидалось page={validated_data.page}, но пришло {page}"
    assert len(validated_data.data) == validated_data.per_page,\
        f"Несоответствие кол-ва объектов в data({len(validated_data.data)}) и per_page={len(validated_data.data)}"