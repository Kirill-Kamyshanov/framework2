from enum import StrEnum

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    """Перечень поддерживаемых окружений запуска тестов."""

    DEV = "dev"
    STAGE = "stage"

    def __str__(self) -> str:
        """Человекочитаемое представление для логов и Allure."""
        return self.value.capitalize()


class EnvironmentConfig(BaseSettings):
    """Конфиг окружения. URL фиксированы в коде, секреты подтягиваются из .env / переменных окружения."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="",
        extra="ignore",
        case_sensitive=False,
    )

    reqres_url: str
    reqres_api_key: str = Field(default="")

    def __str__(self) -> str:
        """Краткое представление конфига для логов."""
        return f"- Reqres API: {self.reqres_url}"


_URLS: dict[Environment, str] = {
    Environment.DEV: "https://reqres.in/api",
    Environment.STAGE: "https://reqres.in/api",
}


def load_environment(env: Environment | str) -> EnvironmentConfig:
    """Возвращает конфиг для запрошенного окружения.

    URL берётся из статической таблицы _URLS, секреты — из .env / env vars.
    """
    env = env if isinstance(env, Environment) else Environment(env.lower())
    return EnvironmentConfig(reqres_url=_URLS[env])
