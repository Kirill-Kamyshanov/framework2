import allure
import pytest

from services.reqres_in.users.get_user import GetUser
from services.reqres_in.users.models.user import UserData

def test_user_validation(env_config):
    user_id = 1
    full_response_json = GetUser(env_config).get_user(user_id).json()

    validate = UserData(**full_response_json["data"])
    assert validate.id == user_id, f'invalid user_id: {user_id}'
    print(f'Validation user {user_id} succeeded.')

