from typing import Optional
from pydantic import BaseModel, Field, field_validator

# Список всех ролей из таблицы ролей Лабораторной работы №1
ALLOWED_ROLES = [
    "покупатель",
    "менеджер",
    "менеджер каталога",
    "кладовщик",
    "менеджер по ценообразованию",
    "модератор",
    "администратор"
]

class UserBase(BaseModel):
    email: str = Field(..., description="Электронная почта пользователя")
    username: Optional[str] = Field(None, description="Имя пользователя")
    role: str = Field(default="покупатель", description="Роль в системе")

    @field_validator("email")
    def validate_email_format(cls, value: str):
        value = value.strip()
        if "@" not in value:
            raise ValueError("Электронная почта указана неверно: отсутствует обязательный символ '@'")
        parts = value.split("@")
        if len(parts) != 2 or not parts[0] or "." not in parts[1]:
            raise ValueError("Некорректный формат почты: укажите адрес вида имя@домен.ru")
        return value

    @field_validator("role")
    def validate_role(cls, value: str):
        role_lower = value.strip().lower()
        if role_lower not in ALLOWED_ROLES:
            roles_str = ", ".join(ALLOWED_ROLES)
            raise ValueError(
                f"Недопустимая роль '{value}'. Доступные роли в системе: {roles_str}"
            )
        return role_lower

class User(UserBase):
    password: str

class NewUser(UserBase):
    password: str = Field(..., min_length=4, description="Пароль пользователя")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "manager@store.ru",
                "password": "managerPassword2026",
                "username": "Артур (Менеджер)",
                "role": "менеджер"
            }
        }

class UserSignIn(BaseModel):
    email: str = Field(..., description="Электронная почта")
    password: str = Field(..., description="Пароль")

    @field_validator("email")
    def validate_email_format(cls, value: str):
        if "@" not in value:
            raise ValueError("Электронная почта указана неверно: отсутствует символ '@'")
        return value.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "email": "manager@store.ru",
                "password": "managerPassword2026"
            }
        }
