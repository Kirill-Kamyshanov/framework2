import allure
import pook
import pytest

from services.reqres_in.auth.login_user import assert_login_is_successful, LoginUser, assert_login_is_failed
from services.reqres_in.auth.models.auth import LoginRequest, RegisterRequest
from services.reqres_in.auth.register_user import RegisterUser, assert_register_is_successful, assert_register_is_failed



class TestAuth:
    base_url = "https://reqres.in/api"
    valid_request_body = {"email": "example@example.com", "password": "password123"}
    invalid_request_body = {"email": "example@example.com"}

    success_auth_response_body = {"token": "yalubluykabachki"}

    success_register_response_body = {"id": 12, "token" : "yalubluykabachki"}
    failure_response_body = {"message": "access denied"}


    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.title('Успешная регистрация')
    @allure.testcase("https://jira.example.com/TC-11", "TC-11")
    @allure.feature('Registration')
    @pook.on
    def test_register_successful(self, env_config):
        """Успешная регистрация с валидными данными"""
        with allure.step('Настройка тестового мока:'):
            pook.post(f'{self.base_url}/register',
                      json=self.valid_request_body,
                      status=200,
                      response_json=self.success_register_response_body
                      )

        with allure.step('Отправка запроса и валидация ответа:'):
            validated_request_body = RegisterRequest(**self.valid_request_body)

            response, validated_data = RegisterUser(env_config).register(validated_request_body.model_dump())
            assert_register_is_successful(response, validated_data, self.success_register_response_body)


    @pytest.mark.regression
    @allure.title('Регистрация с невалидными входными данными')
    @allure.testcase("https://jira.example.com/TC-12", "TC-12")
    @allure.feature('Registration')
    @pook.on
    def test_register_negative(self, env_config):
        """Неуспешная регистрация без пароля"""
        with allure.step('Подготовка тестовых данных:'):
            pook.post(f'{self.base_url}/register',
                      json=self.invalid_request_body,
                      status=400,
                      response_json=self.failure_response_body
                      )

        with allure.step('Отправка запроса и валидация ответа:'):
            response, validated_data = RegisterUser(env_config).register(self.invalid_request_body, positive=False)
            assert_register_is_failed(response, validated_data, self.failure_response_body)


    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.title('Успешная авторизация')
    @allure.testcase("https://jira.example.com/TC-13", "TC-13")
    @allure.feature('Authorization')
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

            response, validated_data = LoginUser(env_config).login(
                req_body
            )

        with allure.step('Валидация ответа:'):
            assert_login_is_successful(response, validated_data, self.success_auth_response_body)


    @pytest.mark.regression
    @allure.title('Авторизация с невалидными входными данными')
    @allure.testcase("https://jira.example.com/TC-14", "TC-14")
    @allure.feature('Authorization')
    @pook.on
    def test_auth_negative(self, env_config):
        """Неуспешная авторизация без пароля"""
        with allure.step('Подготовка тестовых данных:'):
            pook.post(f'{self.base_url}/login',
                      json=self.invalid_request_body,
                      status=400,
                      response_json=self.failure_response_body
                      )

        with allure.step('Отправка запроса:'):
            response, validated_data = LoginUser(env_config).login(
                self.invalid_request_body,
                positive=False
            )

        with allure.step('Валидация ответа:'):
            assert_login_is_failed(response, validated_data, self.failure_response_body)
