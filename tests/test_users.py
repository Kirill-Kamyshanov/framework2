import allure
import pytest

from services.reqres_in.users.delete_user import DeleteUser
from services.reqres_in.users.get_user import GetUser, assert_user_data_is_correct
from services.reqres_in.users.get_users import GetUsers, assert_users_data_is_correct
from services.reqres_in.users.patch_update import assert_user_updated_correctly, UpdateUserPatch
from services.reqres_in.users.post_create import CreateUser, assert_user_created_correctly
from services.reqres_in.users.put_update import UpdateUserPut, assert_user_updated_put_correctly
from services.reqres_in.users.models.user import CreateUserRequest, UpdateUserRequest


# @pytest.fixture
# def created_user_ids():
#     """Список ID созданных пользователей для cleanup."""
#     return []
#
#
# @pytest.fixture
# def cleanup_users(env_config, created_user_ids):
#     """Фикстура для удаления тестовых пользователей после теста."""
#     yield
#
#     for user_id in created_user_ids:
#         try:
#             DeleteUser(env_config).delete(user_id)
#         except Exception as e:
#             print(f"Ошибка при удалении {user_id}: {e}")



@allure.feature('Users')
class TestUsers:
    def test_users_pagination(self, env_config):
        with allure.step('Отправка GET-запроса с пагинацией'):
            page = 2
            response, validated_data, page = GetUsers(env_config).get_users(page)

        with allure.step('Валидация тела ответа'):
            assert_users_data_is_correct(response, validated_data, page)


    def test_get_user(self, env_config):
        with allure.step('Получение данных о пользователе'):
            user_id = 2
            response, validated_data = GetUser(env_config).get_user(user_id)

        with allure.step('Проверка корректности ответа'):
            assert_user_data_is_correct(response, validated_data, user_id)


    def test_get_user_negative(self, env_config):
        with allure.step('Попытка получить данные о несуществующем пользователе'):
            invalid_id = 23
            response, validated_data = GetUser(env_config).get_user(invalid_id, validate=False)

        with allure.step('Проверка статус-кода от сервера'):
            assert response.status_code == 404


    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.title('Создание нового пользователя')
    @allure.testcase("https://jira.example.com/TC-1", "TC-1")
    def test_create_user(self, env_config, user_data, delete_user):
        with allure.step('Создаём нового пользователя'):
            # генерация случайных тестовых данных для создания юзера
            test_data = CreateUserRequest()
            #  создание юзера
            response, validated_data = CreateUser(env_config).create_user(
                **test_data.model_dump()
            )

        with allure.step('Проверка корректности создания'):
            assert_user_created_correctly(
                response, validated_data, test_data.name, test_data.job
            )

        # добавление данных юзера в контейнер для удаления
        user_data.update(validated_data.model_dump())


    def test_update_user_put(self, env_config):
        with allure.step('Получение исходных данных о пользователе'):
            user_id = 2
            response, _ = GetUser(env_config).get_user(user_id)


        with allure.step('Обновление тестового юзера'):
            new_data = UpdateUserRequest()
            response, validated_data = UpdateUserPut(env_config).update(
                user_id=user_id, **new_data.model_dump(exclude_none=True)
            )

        with allure.step('Проверка корректности обновления данных'):
            assert_user_updated_put_correctly(response, validated_data, **new_data.model_dump(exclude_none=True))




    def test_update_user_patch(self, env_config):
        with allure.step('Получение исходных данных о пользователе'):
            user_id = 2
            response, _ = GetUser(env_config).get_user(user_id)


        with allure.step('Обновление тестового юзера'):
            new_data = UpdateUserRequest()
            response, validated_data = UpdateUserPatch(env_config).update(
                user_id=user_id, **new_data.model_dump(exclude_none=True)
            )

        with allure.step('Проверка корректности обновления данных'):
            assert_user_updated_correctly(response, validated_data, **new_data.model_dump(exclude_none=True))



    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.title('Удаление пользователя')
    @allure.testcase("https://jira.example.com/TC-1", "TC-2")
    def test_delete_user(self, env_config):
        with allure.step('Удаление пользователя'):
            user_id = 2
            DeleteUser(env_config).delete(user_id)