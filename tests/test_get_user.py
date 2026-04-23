import allure
import pytest

from services.reqres_in.users.get_user import GetUser, assert_user_data_is_correct


def test_get_user(env_config):
    with allure.step('Получение данных о пользователе'):
        user_id = 2
        response, validated_data = GetUser(env_config).get_user(user_id)

    with allure.step('Проверка корректности ответа'):
        assert_user_data_is_correct(response, validated_data, user_id)
