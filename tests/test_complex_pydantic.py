import allure
import pytest

from services.reqres_in.users.delete_user import DeleteUser
from services.reqres_in.users.get_user import GetUser, assert_user_data_is_correct
from services.reqres_in.users.patch_update import UpdateUserPatch, assert_user_updated_correctly
from services.reqres_in.users.post_create import CreateUser, assert_user_created_correctly
from services.reqres_in.users.models.user import CreateUserRequest, CreateUserResponse, UserData, UpdateUserRequest, UpdateUserResponse
from faker import Faker

fake = Faker()


@pytest.fixture
def created_user_ids():
    """Список ID созданных пользователей для cleanup."""
    return []


@pytest.fixture
def cleanup_users(env_config, created_user_ids):
    """Фикстура для удаления тестовых пользователей после теста."""
    yield  # Тест выполняется здесь

    # Cleanup после теста
    for user_id in created_user_ids:
        try:
            DeleteUser(env_config).delete(user_id)
        except Exception as e:
            print(f"Ошибка при удалении {user_id}: {e}")





class TestCrudOperations:
    def test_create_user_with_pydantic(self, env_config, created_user_ids, cleanup_users):
        with allure.step('Создаём нового пользователя'):
            # генерация случайных тестовых данных для создания юзера
            test_data = CreateUserRequest()
            #  создание юзера
            response, validated_data = CreateUser(env_config).create_user(
                **test_data.model_dump()
            )

        with allure.step('Проверяем корректность создания'):
            assert_user_created_correctly(
                response, validated_data, test_data.name, test_data.job
            )

        created_user_ids.append(validated_data.id)


    def test_get_user_with_pydantic(self, env_config):
        with allure.step('Получение данных о пользователе'):
            user_id = 2
            response, validated_data = GetUser(env_config).get_user(user_id)

        with allure.step('Проверка корректности ответа'):
            assert_user_data_is_correct(response, validated_data, user_id)


    def test_update_user_with_pydantic(self, env_config, created_user_ids, cleanup_users):
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


    def test_delete_user_with_pydantic(self, env_config):
        with allure.step('Создание нового пользователя'):
            create_response = CreateUser(env_config).create_user(
                name="To Delete",
                job="Temporary"
            )[1]

        with allure.step('Удаление пользователя'):
            user_id = create_response.id
            DeleteUser(env_config).delete(user_id)
