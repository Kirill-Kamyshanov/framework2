from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Запрос на регистрацию"""

    email: EmailStr
    password: str


class RegisterResponse(BaseModel):
    """Успешный ответ при регистрации"""

    id: int = Field(gt=0)
    token: str


class LoginRequest(BaseModel):
    """Запрос на вход"""

    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Успешный ответ при авторизации"""

    token: str


class ErrorResponse(BaseModel):
    """Ответ с ошибкой при регистрации/авторизации"""

    error: str
