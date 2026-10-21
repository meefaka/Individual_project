import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routes.users import user_router
from routes.products import product_router

app = FastAPI(
    title="Каталог интернет-магазина электроники (Catalog Service)",
    description="Лабораторная работа №2. Проектирование структуры на основе микросервисов."
)

# Перехватчик ошибок валидации для вывода аккуратного русского текста
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        msg = error.get("msg", "")
        # Если ошибка сформирована нашим валидатором (ValueError), убираем префикс "Value error, "
        if msg.startswith("Value error, "):
            msg = msg.replace("Value error, ", "")
        errors.append(msg)
    
    error_message = errors[0] if len(errors) == 1 else "; ".join(errors)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": error_message}
    )

app.include_router(user_router, prefix="/user")
app.include_router(product_router, prefix="/product")

@app.get("/", tags=["Главная"])
async def home():
    return {"message": "Добро пожаловать в сервис каталога интернет-магазина техники!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
