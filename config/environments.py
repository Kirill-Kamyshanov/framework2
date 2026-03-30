import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные из .env файла (ищем в корне проекта)
_env_path = Path(__file__).parent.parent / ".env"
load_dotenv(_env_path)

class Environment(str, Enum):
    DEV = "dev"
    STAGE = "stage"

    def __str__(self):
        return {
            self.DEV: "Dev",
            self.STAGE: "Stage"
        }[self]


@dataclass
class EnvironmentConfig:
    reqres_url: str
    reqres_api_key: str

    def __str__(self):
        return f"- Reqres API: {self.reqres_url}"

# API ключ читается из переменной окружения REQRES_API_KEY
_api_key = os.environ.get("REQRES_API_KEY", "")

environments = {
    Environment.DEV: EnvironmentConfig(
        reqres_url="https://reqres.in/api",
        reqres_api_key=_api_key
    ),
    Environment.STAGE: EnvironmentConfig(
        reqres_url="https://reqres.in/api",
        reqres_api_key=_api_key
    )
}