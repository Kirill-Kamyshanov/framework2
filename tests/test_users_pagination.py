from services.reqres_in.users.get_users import GetUsers
from services.reqres_in.users.models.user import UsersListResponse


def test_users_pagination(env_config):
    page = 1
    response = GetUsers(env_config).get_users(page)
    assert response.status_code == 200, f'Incorrect response code: {response.status_code}'
    validated = UsersListResponse(**response.json())
    assert validated.page == page, f'{validated.page} != {page}'
    assert len(validated.data) == validated.per_page, f'{len(validated.data)} != {validated.per_page}'

