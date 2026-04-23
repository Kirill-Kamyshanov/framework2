import allure
import pytest

from services.reqres_in.users.post_create import CreateUser
from services.reqres_in.users.delete_user import DeleteUser

@pytest.mark.smoke
@pytest.mark.regression
@allure.title('Удаление пользователя')
@allure.testcase("https://jira.example.com/TC-1", "TC-2")
def test_delete_user(env_config):
    with allure.step('Создание нового пользователя'):
            create_response  = CreateUser(env_config).create_user(
            name="To Delete",
            job="Temporary"
        )[1]

    with allure.step('Удаление пользователя'):
        user_id = create_response.id
        DeleteUser(env_config).delete(user_id)