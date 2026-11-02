from typing import Optional
from beanie import Document
from pydantic import BaseModel, Field, EmailStr

class User(Document):
    email: EmailStr = Field(..., description="Электронная почта")
    username: Optional[str] = Field(None, description="Имя пользователя")
    role: str = Field(default="покупатель", description="Роль пользователя в системе")
    password: str = Field(..., min_length=4, description="Пароль пользователя")

    class Settings:
        name = "users"

    class Config:
        json_schema_extra = {
            "example": {
                "email": "manager@store.ru",
                "username": "Анастасия (Менеджер)",
                "role": "менеджер",
                "password": "managerPassword2026"
            }
        }

class UserSignIn(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., description="Пароль")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "manager@store.ru",
                "password": "managerPassword2026"
            }
        }
