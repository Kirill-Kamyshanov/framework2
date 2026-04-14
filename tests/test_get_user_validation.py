from services.reqres_in.users.get_user import GetUser
from pydantic import BaseModel, Field, ValidationError


def test_user_validation(env_config):
    class User(BaseModel):
        id: int = Field(gt=0)
        email: str
        first_name: str
        last_name: str
        avatar: str

    user_id = 1
    full_response_json = GetUser(env_config).get_user(user_id).json()

    try:
        User(**full_response_json["data"])
        print(f'Validation user {user_id} succeeded.')
    except ValidationError as e:
        print(f'Validation user {user_id} failed.')
