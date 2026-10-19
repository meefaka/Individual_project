import uvicorn
from fastapi import FastAPI
from routes.users import user_router
from routes.products import product_router

app = FastAPI(title="Electronics Store - Catalog Service")

app.include_router(user_router, prefix="/user")
app.include_router(product_router, prefix="/product")

@app.get("/")
async def home():
    return {"message": "Добро пожаловать в сервис каталога интернет-магазина техники!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
