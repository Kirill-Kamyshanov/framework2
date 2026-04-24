from services.base_api import BaseAPI
from utils.helper import helper


class GetResources(BaseAPI):
    def __init__(self, env_config):
        """
        Args:
            env_config (EnvironmentConfig): Конфигурация окружения из фикстуры
        """
        super().__init__(base_url=env_config.reqres_url, api_key=env_config.reqres_api_key)


    def get_resources(self):
        """Получение списка ресурсов с пагинацией"""