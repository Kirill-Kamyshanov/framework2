import allure
import pytest

from services.reqres_in.users.get_user import GetUser

def test_get_user_negative(env_config):
    with allure.step('Попытка получить данные о несуществующем пользователе'):
        invalid_id = 999999
        response, validated_data = GetUser(env_config).get_user(invalid_id, validate=False)

    with allure.step('Проверка статус-кода от сервера'):
        assert response.status_code == 404