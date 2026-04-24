from services.base_api import BaseAPI
from services.reqres_in.resources.models.resource import SingleResourceResponse, ResourceData, Support
from utils.helper import helper


class GetResource(BaseAPI):
    def __init__(self, env_config):
        """
        Args:
            env_config (EnvironmentConfig): Конфигурация окружения из фикстуры
        """
        super().__init__(base_url=env_config.reqres_url, api_key=env_config.reqres_api_key)


    def get_resource(self, resource_id):
        """получение одного ресурса по ID"""
        # отправка запроса
        response = self.session.get(f"{self.base_url}/resource/{resource_id}")

        # прикрепление JSON к allure-отчёту
        helper.attach_response(response)

        # валидация отчёта
        validated = SingleResourceResponse.model_validate(response.json())
        return response, validated


def assert_resource_data_is_correct(response, validated_data, resource_id):
    ...

