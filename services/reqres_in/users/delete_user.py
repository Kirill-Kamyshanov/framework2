from services.base_api import BaseAPI

class DeleteUser(BaseAPI):
    def __init__(self, env_config):
        """
        Args:
            env_config (EnvironmentConfig): Конфигурация окружения из фикстуры
        """
        super().__init__(base_url=env_config.reqres_url, api_key=env_config.reqres_api_key)

    def delete(self, user_id):
        """Удаление пользователя
        Args:
            user_id (int): ID пользователя

        Returns:
            requests.Response: Ответ от сервера
        """
        response = self.session.delete(f'{self.base_url}/{user_id}')
        return response