import allure
import pytest

from services.reqres_in.users.get_users import GetUsers
from services.reqres_in.users.models.user import UsersListResponse


def test_users_pagination(env_config):
    page = 1
    response, validated_data = GetUsers(env_config).get_users(page)
    print(validated_data)
    assert validated_data.page == page
    assert len(validated_data.data) == validated_data.per_page

