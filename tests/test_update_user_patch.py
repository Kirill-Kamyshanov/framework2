import allure
import pytest

from services.reqres_in.users.delete_user import DeleteUser
from services.reqres_in.users.models.user import UpdateUserRequest, UpdateUserResponse
from services.reqres_in.users.patch_update import UpdateUserPatch, assert_user_updated_correctly
from services.reqres_in.users.post_create import CreateUser


@pytest.fixture
def created_user_ids():
    """Список ID созданных пользователей для cleanup."""
    return []


@pytest.fixture
def cleanup_users(env_config, created_user_ids):
    """Фикстура для удаления тестовых пользователей после теста."""
    yield

    # Cleanup после теста
    for user_id in created_user_ids:
        try:
            DeleteUser(env_config).delete(user_id)
        except Exception as e:
            print(f"Ошибка при удалении {user_id}: {e}")





def test_update_user(env_config, created_user_ids, cleanup_users):
    with allure.step('Создание тестового юзера'):
        create_response = CreateUser(env_config).create_user(
            name="John Doe",
            job="QA Engineer"
        )[1]
        user_id = create_response.id

    with allure.step('Обновление тестового юзера'):
        new_data = UpdateUserRequest()
        response, validated_data = UpdateUserPatch(env_config).update(
            user_id=user_id, **new_data.model_dump(exclude_none=True)
        )

    with allure.step('Проверка корректности обновления данных'):
        assert_user_updated_correctly(response, validated_data, **new_data.model_dump(exclude_none=True))

    created_user_ids.append(user_id)



