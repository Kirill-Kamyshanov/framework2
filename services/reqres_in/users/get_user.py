from services.base_api import BaseAPI

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
        return response
