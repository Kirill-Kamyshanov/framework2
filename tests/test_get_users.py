import allure
import pytest

from services.reqres_in.users.get_users import GetUsers, assert_users_data_is_correct


def test_get_users(env_config):
    with allure.step('Получение списка пользователей'):
        response, validated_data, page = GetUsers(env_config).get_users()
        print(validated_data)

    with allure.step('Валидация тела ответа'):
        assert_users_data_is_correct(response, validated_data, page)