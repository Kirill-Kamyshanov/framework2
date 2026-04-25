from services.base_api import BaseAPI
from services.reqres_in.auth.models.auth import LoginResponse, ErrorResponse
from utils.helper import helper


class LoginUser(BaseAPI):
    def __init__(self, env_config):
        """
        Args:
            env_config (EnvironmentConfig): Конфигурация окружения из фикстуры
        """
        super().__init__(base_url=env_config.reqres_url, api_key=env_config.reqres_api_key)


    def login(self, request_body, positive=True):

        response = self.session.post(f'{self.base_url}/login',json=request_body)


        helper.attach_response(response)

        if positive:
            validated = LoginResponse.model_validate(response.json())
        else:
            validated = ErrorResponse.model_validate(response.json())

        return response, validated


def assert_login_is_successful(response, validated_data, expected_response_body):
    assert response.status_code == 200, f"Ожидался статус-код 200, но получен {response.status_code}: {response.text}"
    assert validated_data.token == expected_response_body['token'], f"Ожидался token={expected_response_body['token']}, но получен {validated_data.token}"


def assert_login_is_failed(response, validated_data, expected_response_body):
    assert response.status_code == 400, f"Ожидался статус-код 400, но получен {response.status_code}: {response.text}"
    assert validated_data.message == expected_response_body['message'], f"Ожидался message={expected_response_body['message']}, но получен {validated_data.message}"

