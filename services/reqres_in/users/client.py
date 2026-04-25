from requests import Response

from services.base_api import BaseAPI
from services.reqres_in.users.models.user import (
    CreateUserResponse,
    SingleUserResponse,
    UpdateUserResponse,
    UsersListResponse,
)


class UsersClient(BaseAPI):
    """Фасад над ресурсом /users — единый клиент на все операции с пользователями."""

    resource = "/users"

    def list(self, page: int = 1) -> tuple[Response, UsersListResponse]:
        """GET /users — возвращает список пользователей и валидированный ответ."""
        response = self.get(self.resource, params={"page": page})
        return response, UsersListResponse.model_validate(response.json())

    def get_by_id(self, user_id: int, validate: bool = True) -> tuple[Response, SingleUserResponse | None]:
        """GET /users/{user_id}. При validate=False пропускает Pydantic-валидацию (для негативных кейсов)."""
        response = self.get(f"{self.resource}/{user_id}")
        validated = SingleUserResponse.model_validate(response.json()) if validate else None
        return response, validated

    def create(self, name: str, job: str) -> tuple[Response, CreateUserResponse]:
        """POST /users — создаёт пользователя и возвращает валидированный ответ."""
        response = self.post(self.resource, json={"name": name, "job": job})
        return response, CreateUserResponse.model_validate(response.json())

    def update_put(self, user_id: int, name: str, job: str) -> tuple[Response, UpdateUserResponse]:
        """PUT /users/{user_id} — полное обновление данных пользователя."""
        response = self.put(f"{self.resource}/{user_id}", json={"name": name, "job": job})
        return response, UpdateUserResponse.model_validate(response.json())

    def update_patch(self, user_id: int, name: str, job: str) -> tuple[Response, UpdateUserResponse]:
        """PATCH /users/{user_id} — частичное обновление данных пользователя."""
        response = self.patch(f"{self.resource}/{user_id}", json={"name": name, "job": job})
        return response, UpdateUserResponse.model_validate(response.json())

    def remove(self, user_id: int) -> Response:
        """DELETE /users/{user_id} — возвращает сырой Response (тело пустое, проверяется только статус)."""
        return self.delete(f"{self.resource}/{user_id}")
