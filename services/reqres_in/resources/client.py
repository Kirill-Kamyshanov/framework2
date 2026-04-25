from requests import Response

from services.base_api import BaseAPI
from services.reqres_in.resources.models.resource import (
    ResourcesListResponse,
    SingleResourceResponse,
)


class ResourcesClient(BaseAPI):
    """Фасад над ресурсом /resource(s)."""

    def list(self, page: int = 1) -> tuple[Response, ResourcesListResponse]:
        """GET /resources — возвращает список ресурсов с пагинацией."""
        response = self.get("/resources", params={"page": page})
        return response, ResourcesListResponse.model_validate(response.json())

    def get_by_id(self, resource_id: int, validate: bool = True) -> tuple[Response, SingleResourceResponse | None]:
        """GET /resource/{resource_id}. При validate=False пропускает Pydantic-валидацию (для негативных кейсов)."""
        response = self.get(f"/resource/{resource_id}")
        validated = SingleResourceResponse.model_validate(response.json()) if validate else None
        return response, validated
