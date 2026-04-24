import allure
import pytest

from services.reqres_in.resources.get_resource import GetResource, assert_resource_data_is_correct


class TestResources:
    def test_get_resources_list(self, env_config):
        """Получение списка ресурсов"""



    def test_get_resource_11(self, env_config):
        """Получение одного ресурса"""
        with allure.step('Отправка запроса и валидация ответа'):
            resource_id = 2
            response, validated_data = GetResource(env_config).get_resource(resource_id)
            print(validated_data)

        with allure.step('Проверка корректности полученных данных'):
            assert_resource_data_is_correct(response, validated_data, resource_id)





    def test_get_unexisted_resource(self, env_config):
        """Получение несуществующего ресурса"""
        unexisted_resource = 23
        # ждём 404