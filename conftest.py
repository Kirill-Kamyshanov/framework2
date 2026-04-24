import pytest
from config.environments import Environment, environments, EnvironmentConfig
from services.reqres_in.users.delete_user import DeleteUser


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="stage",
        help="Окружение для запуска тестов (dev/stage)"
    )


@pytest.fixture(scope="session")
def env(request) -> Environment:
    """Фикстура для получения текущего окружения"""
    env_name = request.config.getoption("--env")
    try:
        return Environment(env_name.lower())
    except ValueError:
        raise ValueError(
            f"Некорректное окружение: {env_name}. "
            f"Используйте одно из: dev/stage"
        )


@pytest.fixture(scope="session")
def env_config(env) -> EnvironmentConfig:
    """Фикстура для получения конфигурации текущего окружения"""
    print(f"\nОкружение: {env}")
    print(f"{environments[env]}\n")
    return environments[env]






@pytest.fixture
def user_data() -> dict:
    """Контейнер для хранения данных созданного пользователя"""
    return {}



# Использую только в test_create_user, т.к. я больше нигде юзера не создаю
@pytest.fixture
def delete_user(env_config, user_data):
    """Автоматическая очистка созданного пользователя после теста"""
    yield

    user_id = user_data["id"]
    try:
        DeleteUser(env_config).delete(user_id)
        print(f"Пользователь {user_id} успешно удалён")
    except Exception as e:
        print(f"Ошибка при удалении {user_id}: {e}")
