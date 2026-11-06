from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from database.connection import Settings
from routes.products import product_router
from routes.users import user_router
from routes.web import web_router

settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Автоматическое подключение к MongoDB при старте
    await settings.initialize_database()
    yield

app = FastAPI(
    title="Каталог интернет-магазина электроники (Catalog Service + MongoDB)",
    description="Каталог электроники на базе FastAPI, MongoDB и шаблонизатора Jinja2.",
    lifespan=lifespan
)

# Перехватчик ошибок валидации данных
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        msg = error.get("msg", "")
        if msg.startswith("Value error, "):
            msg = msg.replace("Value error, ", "")
        errors.append(msg)
    error_message = errors[0] if len(errors) == 1 else "; ".join(errors)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": error_message}
    )

# Подключение маршрутизаторов
app.include_router(web_router)
app.include_router(user_router, prefix="/user")
app.include_router(product_router, prefix="/product")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
