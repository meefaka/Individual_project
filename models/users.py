from typing import Optional
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None
    role: Optional[str] = "customer"

class NewUser(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None
    role: Optional[str] = "customer"

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "manager@store.ru",
                "password": "strongPassword123"
            }
        }
