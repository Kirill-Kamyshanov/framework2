from services.reqres_in.users.post_create import CreateUser
from services.reqres_in.users.delete_user import DeleteUser

def test_delete_user(env_config):
    create_response  = CreateUser(env_config).create_user(
        name="To Delete",
        job="Temporary"
    )
    # print(create_response[0].status_code)
    # print(create_response[1])
    user_id = create_response.json()['id']
    print(user_id)
    response = DeleteUser(env_config).delete(user_id)
    assert response.status_code == 204
