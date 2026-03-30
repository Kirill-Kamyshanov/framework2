from services.reqres_in.users.get_user import GetUser


def test_get_user(env_config):
    user_id = 2
    response = GetUser(env_config).get_user(user_id)
    assert response.status_code == 200
    assert "data" in response.json()
    assert  response.json()['data']['id'] == user_id