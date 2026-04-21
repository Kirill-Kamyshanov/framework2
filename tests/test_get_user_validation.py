from services.reqres_in.users.get_user import GetUser
from models.user import User

def test_user_validation(env_config):
    user_id = 1
    full_response_json = GetUser(env_config).get_user(user_id).json()

    validate = User(**full_response_json["data"])
    assert validate.id == user_id, f'invalid user_id: {user_id}'
    print(f'Validation user {user_id} succeeded.')

