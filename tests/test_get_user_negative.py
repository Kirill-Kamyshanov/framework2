from services.reqres_in.users.get_user import GetUser

def test_get_user_negative(env_config):
    invalid_id = 999999
    response = GetUser(env_config).get_user(invalid_id)

    assert response.status_code == 404