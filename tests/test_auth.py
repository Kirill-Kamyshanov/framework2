import allure
import pook
import pytest
import requests

from conftest import env_config
from services.reqres_in.auth.login_user import assert_login_is_successful, LoginUser
from services.reqres_in.auth.models.auth import LoginRequest


class TestAuth:
    base_url = "https://reqres.in/api"
    valid_request_body = {"email": "example@example.com", "password": "password123"}
    invalid_request_body = {"email": "example@example.com"}

    success_auth_response_body = {"token": "yalubluykabachki"}

    success_register_response_body = {"message": "success"}
    failure_register_response_body = {"message": "access denied"}


# нет
    @pook.on
    def test_register_successful(self):
        """Успешная регистрация с валидными данными"""
        with allure.step('Настройка тестового мока:'):
            pook.post(f'{self.base_url}/register',
                      json=self.valid_request_body,
                      status=200,
                      response_json=self.success_response_body
                      )

        with allure.step('Отправка запроса и валидация ответа:'):
            response = requests.post(f'{self.base_url}/register',json= self.valid_request_body)

            assert response.status_code == 200
            assert response.json() == self.success_response_body


    # нет
    @pook.on
    def test_register_negative(self):
        """Неуспешная регистрация без пароля"""
        with allure.step('Подготовка тестовых данных:'):
            pook.post(f'{self.base_url}/register',
                      json=self.invalid_request_body,
                      status=400,
                      response_json=self.failure_response_body
                      )

        with allure.step('Отправка запроса и валидация ответа:'):
            response = requests.post(f'{self.base_url}/register', json=self.invalid_request_body)

            assert response.status_code == 400
            assert response.json() == self.failure_response_body



# ЕС
    @pook.on
    def test_auth_successful(self, env_config):
        """Успешная авторизация"""
        with allure.step('Подготовка тестовых данных:'):
            pook.post(f'{self.base_url}/login',
                      json=self.valid_request_body,
                      status=200,
                      response_json=self.success_auth_response_body
                      )

        with allure.step('Отправка запроса:'):
            req_body = LoginRequest.model_validate(self.valid_request_body).model_dump()
            print(req_body)

            response, validated_data = LoginUser(env_config).login(
                req_body
            )

        with allure.step('Валидация ответа:'):
            assert_login_is_successful(response, validated_data, self.success_auth_response_body)



    # нет
    @pook.on
    def test_auth_negative(self):
        """Неуспешная авторизация без пароля"""
        with allure.step('Подготовка тестовых данных:'):
            pook.post(f'{self.base_url}/login',
                      json=self.invalid_request_body,
                      status=400,
                      response_json=self.failure_response_body
                      )

        with allure.step('Отправка запроса и валидация ответа:'):
            response = requests.post(f'{self.base_url}/login',json= self.invalid_request_body)

            assert response.status_code == 400
            assert response.json() == self.failure_response_body






