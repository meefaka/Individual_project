from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from database.connection import Settings
from routes.products import product_router
from routes.users import user_router

settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Автоматическое подключение к MongoDB при старте
    await settings.initialize_database()
    yield

app = FastAPI(
    title="Каталог интернет-магазина электроники (Catalog Service + MongoDB)",
    description="Лабораторная работа №3. Интеграция базы данных MongoDB с помощью Beanie.",
    lifespan=lifespan
)

app.include_router(user_router, prefix="/user")
app.include_router(product_router, prefix="/product")

@app.get("/", tags=["Главная"])
async def home():
    return {"message": "Сервис каталога электроники успешно подключен к MongoDB!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
