from requests import Response

from services.base_api import BaseAPI
from services.reqres_in.auth.models.auth import ErrorResponse, LoginResponse, RegisterResponse


class AuthClient(BaseAPI):
    """Фасад над ресурсами /login и /register."""

    def login(self, body: dict) -> tuple[Response, LoginResponse]:
        """POST /login — успешная авторизация, валидирует ответ как LoginResponse."""
        response = self.post("/login", json=body)
        return response, LoginResponse.model_validate(response.json())

    def login_expect_error(self, body: dict) -> tuple[Response, ErrorResponse]:
        """POST /login для негативных кейсов — валидирует ответ как ErrorResponse."""
        response = self.post("/login", json=body)
        return response, ErrorResponse.model_validate(response.json())

    def register(self, body: dict) -> tuple[Response, RegisterResponse]:
        """POST /register — успешная регистрация, валидирует ответ как RegisterResponse."""
        response = self.post("/register", json=body)
        return response, RegisterResponse.model_validate(response.json())

    def register_expect_error(self, body: dict) -> tuple[Response, ErrorResponse]:
        """POST /register для негативных кейсов — валидирует ответ как ErrorResponse."""
        response = self.post("/register", json=body)
        return response, ErrorResponse.model_validate(response.json())
