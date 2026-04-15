from services.base_api import BaseAPI

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

        response = self.session.get(f"{self.base_url}/users?page={page}")
        return response
