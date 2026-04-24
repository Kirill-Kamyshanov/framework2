from services.base_api import BaseAPI
from services.reqres_in.resources.models.resource import ResourcesListResponse
from utils.helper import helper


class GetResources(BaseAPI):
    def __init__(self, env_config):
        """
        Args:
            env_config (EnvironmentConfig): Конфигурация окружения из фикстуры
        """
        super().__init__(base_url=env_config.reqres_url, api_key=env_config.reqres_api_key)


    def get_resources(self, page: int =1):
        """Получение списка ресурсов с пагинацией"""
        # Отправка запроса
        response = self.session.get(f"{self.base_url}/resources?page={page}")

        # Прикрепление JSON ответа к отчёту
        helper.attach_response(response)

        validated = ResourcesListResponse.model_validate(response.json())

        return response, validated


def assert_resources_data_is_correct(response, validated_data, page):
    assert response.status_code == 200, f"Ожидался статус-код 200, но получен {response.status_code}: {response.text}"
    assert validated_data.page == page, f"Ожидался page=={page}, но получен {validated_data.page}"

    total, per_page, total_pages = validated_data.total, validated_data.per_page, validated_data.total_pages
    if total % per_page == 0:
        assert total_pages == total / per_page, \
            f"Ожидалось total_pages=={total / per_page},но пришло {total_pages}"
    else:
        assert total_pages == (total / per_page) + 1, \
            f"Ожидалось total_pages=={(total / per_page) + 1},но пришло {total_pages}"