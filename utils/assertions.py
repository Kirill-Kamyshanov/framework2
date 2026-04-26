import allure


@allure.step("Проверка статус-кода: ожидается {expected_code}")
def assert_status_code(response, expected_code: int) -> None:
    """Проверяет, что HTTP-статус ответа совпадает с ожидаемым; иначе падает с понятным сообщением."""
    assert response.status_code == expected_code, (
        f"Ожидался статус-код {expected_code}, но получен {response.status_code}: {response.text}"
    )
