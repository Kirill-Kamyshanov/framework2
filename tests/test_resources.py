import allure
import pytest

from services.base_api import check_status_code
from services.reqres_in.resources.get_resource import GetResource, assert_resource_data_is_correct
from services.reqres_in.resources.get_resources import GetResources, assert_resources_data_is_correct


class TestResources:
    def test_get_resources_list(self, env_config):
        """Получение списка ресурсов"""
        with allure.step('Отправка запроса и валидация структуры ответа'):
            page = 2
            response, validated_data = GetResources(env_config).get_resources(page)

        with allure.step('Проверка корректности полученных данных'):
            assert_resources_data_is_correct(response, validated_data, 2)



    def test_get_resource(self, env_config):
        """Получение одного ресурса"""
        with allure.step('Отправка запроса и валидация структуры ответа'):
            resource_id = 2
            response, validated_data = GetResource(env_config).get_resource(resource_id)

        with allure.step('Проверка корректности полученных данных'):
            assert_resource_data_is_correct(response, validated_data, resource_id)





    def test_get_unexisted_resource(self, env_config):
        """Получение несуществующего ресурса"""
        with allure.step('Отправка запроса на получение несуществующего юзера'):
            unexisted_resource = 23
            response, _ = GetResource(env_config).get_resource(
                unexisted_resource,
                validate=False
            )

        with allure.step('Проверка статус-кода'):
            check_status_code(response, 404)