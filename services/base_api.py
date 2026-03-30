import requests


class BaseAPI:
    """Базовый класс для работы с API."""

    def __init__(self, base_url, api_key: str = ""):
        self.base_url = base_url
        self.session = requests.Session()
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        # если ключ передан, он добавляется в хедеры
        if api_key:
            headers["x-api-key"] = api_key
        # применяем заголовки к сессии
        self.session.headers.update(headers)