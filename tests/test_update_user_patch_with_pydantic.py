import allure
import pytest

from services.reqres_in.users.models.user import UpdateUserRequest, UpdateUserResponse
from services.reqres_in.users.patch_update import UpdateUserPatch
from services.reqres_in.users.post_create import CreateUser


def test_update_user(env_config):
    # Создание тестового юзера
    create_response = CreateUser(env_config).create_user(
        name="John Doe",
        job="QA Engineer"
    )
    user_id = create_response.json()['id']

    # Обновление тестового юзера
    new_data = UpdateUserRequest()
    update_response = UpdateUserPatch(env_config).update(
        user_id=user_id, **new_data.model_dump(exclude_none=True)
    )
    assert update_response.status_code == 200

    # Валидация тела ответа после обновления
    validated_update_response = UpdateUserResponse(**update_response.json())
    assert validated_update_response.name == new_data.name, f'{validated_update_response.name} != {new_data.name}'
    assert validated_update_response.job == new_data.job, f'{validated_update_response.job} != {new_data.job}'
