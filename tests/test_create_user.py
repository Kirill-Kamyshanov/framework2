import allure
import pytest
from services.reqres_in.users.post_create import CreateUser, assert_user_created_correctly
from services.reqres_in.users.delete_user import DeleteUser


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


@allure.feature('Users')
class TestUser:


    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.title('Создание нового пользователя')
    @allure.testcase("https://jira.example.com/TC-1", "TC-1")
    def test_create_user(self, env_config, cleanup_users, created_user_ids):
        with allure.step('Создаём нового пользователя'):
            response, validated_data = CreateUser(env_config).create_user(
                name="John Doe",
                job="QA Engineer"
            )

        with allure.step('Проверяем корректность создания'):
            assert_user_created_correctly(
                response, validated_data, "John Doe", "QA Engineer"
            )

        created_user_ids.append(validated_data.id)