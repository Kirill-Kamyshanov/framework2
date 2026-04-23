import allure
import pytest

from services.reqres_in.users.get_user import GetUser, assert_user_data_is_correct


def test_user_validation(env_config):
    with allure.step('Получение данных о пользователе'):
        user_id = 1
        response, full_response_json = GetUser(env_config).get_user(user_id)

    with allure.step('Проверка корректности ответа'):
        assert_user_data_is_correct(response, full_response_json, user_id)
        print(f'Validation user {user_id} succeeded.')

    # Проверка та же, что и в test_get_user.py. Предлагаю этот файл тупо удалить

