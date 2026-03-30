from services.reqres_in.users.post_create import CreateUser


def test_create_user(env_config):
    response = CreateUser(env_config).create_user(
        name="John Doe",
        job="QA Engineer"
    )

    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["name"] == "John Doe"
    assert response.json()["job"] == "QA Engineer"