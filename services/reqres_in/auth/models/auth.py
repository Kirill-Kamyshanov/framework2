from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Запрос на регистрацию"""
    email: EmailStr
    password: str = Field(min_length=8)



class RegisterResponse(BaseModel):
    """Успешный ответ при регистрации"""
    id: int = Field(gt=0)
    token: str = Field(min_length=10)



class LoginRequest(BaseModel):
    """Запрос на вход"""
    email: EmailStr
    password: str = Field(min_length=8)


class LoginResponse(BaseModel):
    """Успешный ответ при авторизации"""
    token: str = Field(min_length=10)


class ErrorResponse(BaseModel):
    """Ответ с ошибкой при регистрации/авторизации"""
    message: Literal["Куда собрался-то? Не пущу никуда сказал."]
