from fastapi import APIRouter, HTTPException, status
from database.connection import Database
from models.users import User, UserSignIn

user_router = APIRouter(tags=["User"])
user_database = Database(User)

@user_router.post("/signup", status_code=status.HTTP_201_CREATED, summary="Регистрация нового пользователя")
async def sign_new_user(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с такой почтой уже зарегистрирован"
        )
    await user_database.save(user)
    return {"message": "Пользователь успешно зарегистрирован в MongoDB!"}

@user_router.post("/signin", summary="Вход пользователя в систему")
async def sign_user_in(user: UserSignIn) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь с таким email не найден"
        )
    if user_exist.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный пароль"
        )
    return {"message": "Вход выполнен успешно!"}
