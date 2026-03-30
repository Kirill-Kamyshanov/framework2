from services.reqres_in.users.post_create import CreateUser
from services.reqres_in.users.patch_update import UpdateUser

def test_update_user(env_config):
    create_response = CreateUser(env_config).create_user(
        name="John Doe",
        job="QA Engineer"
    )
    user_id = create_response.json()['id']

    response = UpdateUser(env_config).update(
        user_id=user_id,
        name="Bob Smith",
        job="Senior QA"
    )
    assert response.status_code == 200
    assert response.json()['name'] == 'Bob Smith'
    assert response.json()['job'] == 'Senior QA'
    assert 'updatedAt' in response.json()


