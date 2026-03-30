from services.reqres_in.users.get_users import GetUsers

def test_get_users(env_config):
    response = GetUsers(env_config).get_users()
    assert 'data' in response.json()