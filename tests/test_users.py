import allure
import pytest

from services.base_api import check_status_code
from services.reqres_in.users.delete_user import DeleteUser
from services.reqres_in.users.get_user import GetUser, assert_user_data_is_correct
from services.reqres_in.users.get_users import GetUsers, assert_users_data_is_correct
from services.reqres_in.users.patch_update import assert_user_updated_correctly, UpdateUserPatch
from services.reqres_in.users.post_create import CreateUser, assert_user_created_correctly
from services.reqres_in.users.put_update import UpdateUserPut, assert_user_updated_put_correctly
from services.reqres_in.users.models.user import CreateUserRequest, UpdateUserRequest




@allure.feature('Users')
class TestUsers:

    @pytest.mark.regression
    @allure.title('Проверка корректности пагинации')
    @allure.testcase("https://jira.example.com/TC-2", "TC-2")
    def test_users_pagination(self, env_config):
        with allure.step('Отправка GET-запроса с пагинацией'):
            page = 2
            response, validated_data, page = GetUsers(env_config).get_users(page)

        with allure.step('Валидация тела ответа'):
            assert_users_data_is_correct(response, validated_data, page)


    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.title('Получение данных о пользователе')
    @allure.testcase("https://jira.example.com/TC-3", "TC-3")
    def test_get_user(self, env_config):
        with allure.step('Получение данных о пользователе'):
            user_id = 2
            response, validated_data = GetUser(env_config).get_user(user_id)

        with allure.step('Проверка корректности ответа'):
            assert_user_data_is_correct(response, validated_data, user_id)


    @pytest.mark.regression
    @allure.title('Получение данных о несуществующем пользователе')
    @allure.testcase("https://jira.example.com/TC-4", "TC-4")
    def test_get_user_negative(self, env_config):
        with allure.step('Попытка получить данные о несуществующем пользователе'):
            invalid_id = 23
            response, validated_data = GetUser(env_config).get_user(invalid_id, validate=False)

        with allure.step('Проверка статус-кода от сервера'):
            check_status_code(response, 404)


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


    @pytest.mark.regression
    @allure.title('Обновление данных методом PUT')
    @allure.testcase("https://jira.example.com/TC-5", "TC-5")
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


    @pytest.mark.regression
    @allure.title('Обновление пользователя методом PATCH')
    @allure.testcase("https://jira.example.com/TC-2", "TC-2")
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


    @pytest.mark.regression
    @allure.title('Удаление пользователя')
    @allure.testcase("https://jira.example.com/TC-7", "TC-7")
    def test_delete_user(self, env_config):
        with allure.step('Удаление пользователя'):
            user_id = 2
            DeleteUser(env_config).delete(user_id)