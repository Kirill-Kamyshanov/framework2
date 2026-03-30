from services.base_api import BaseAPI


class CreateUser(BaseAPI):

    def __init__(self, env_config):
        """
        Args:
            env_config (EnvironmentConfig): Конфигурация окружения из фикстуры
        """
        super().__init__(base_url=env_config.reqres_url, api_key=env_config.reqres_api_key)

    def create_user(self, name: str, job: str):
        """Создание нового пользователя.

        Args:
            name (str): Имя пользователя
            job (str): Должность пользователя

        Returns:
            requests.Response: Ответ от сервера
        """
        data = {"name": name, "job": job}
        response = self.session.post(f"{self.base_url}/users", json=data)
        return response