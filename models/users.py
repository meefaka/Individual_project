from typing import Optional
from beanie import Document
from pydantic import BaseModel, Field

class UserBase(BaseModel):
    email: str = Field(..., description="Электронная почта")
    username: Optional[str] = Field(None, description="Имя пользователя")
    role: str = Field(default="покупатель", description="Роль пользователя в системе")

class User(Document):
    email: str = Field(..., description="Электронная почта")
    username: Optional[str] = Field(None, description="Имя пользователя")
    role: str = Field(default="покупатель", description="Роль пользователя в системе")
    password: str = Field(..., min_length=4, description="Пароль пользователя")

    class Settings:
        name = "users"

class NewUser(BaseModel):
    email: str = Field(..., description="Электронная почта")
    username: Optional[str] = Field(None, description="Имя пользователя")
    role: str = Field(default="покупатель", description="Роль в системе")
    password: str = Field(..., min_length=4, description="Пароль пользователя")

class UserSignIn(BaseModel):
    email: str = Field(..., description="Электронная почта")
    password: str = Field(..., description="Пароль")
