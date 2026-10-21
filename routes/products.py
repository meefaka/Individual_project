from typing import List, Optional
from fastapi import APIRouter, Body, HTTPException, Path, Query, status
from models.products import Product, ProductUpdate

product_router = APIRouter(tags=["Товары каталога"])

products: List[Product] = []

@product_router.get("/", response_model=List[Product], summary="Получить все товары (с фильтрацией)")
async def retrieve_all_products(
    brand: Optional[str] = Query(None, description="Фильтр по бренду (например, Samsung, Apple)"),
    category: Optional[str] = Query(None, description="Фильтр по категории (например, Смартфоны, Ноутбуки)")
) -> List[Product]:
    res = products
    if brand:
        res = [p for p in res if p.brand.lower() == brand.lower()]
    if category:
        res = [p for p in res if p.category.lower() == category.lower()]
    return res

@product_router.get("/{id}", response_model=Product, summary="Просмотр товара по ID")
async def retrieve_product(id: int = Path(..., gt=0, description="ID товара")) -> Product:
    for product in products:
        if product.id == id:
            return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Ошибка: Товар с идентификатором ID={id} не найден в каталоге"
    )

@product_router.post("/new", status_code=status.HTTP_201_CREATED, summary="Сценарий 1: Заведение товара в каталог")
async def create_product(body: Product = Body(...)) -> dict:
    for product in products:
        if product.id == body.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ошибка: Товар с ID={body.id} уже существует в базе! Пожалуйста, укажите другой ID."
            )
        if product.sku == body.sku:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ошибка: Товар с артикулом (SKU) '{body.sku}' уже добавлен в систему!"
            )
    products.append(body)
    return {
        "message": "Товар успешно добавлен в каталог интернет-магазина",
        "product_id": body.id
    }

@product_router.put("/{id}", summary="Обновление данных товара")
async def update_product(data: ProductUpdate, id: int = Path(..., gt=0)) -> dict:
    for product in products:
        if product.id == id:
            if data.name is not None:
                product.name = data.name
            if data.brand is not None:
                product.brand = data.brand
            if data.category is not None:
                product.category = data.category
            if data.price is not None:
                product.price = data.price
            if data.description is not None:
                product.description = data.description
            if data.specifications is not None:
                product.specifications = data.specifications
            return {"message": f"Данные товара с ID={id} успешно обновлены"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Невозможно обновить: товар с ID={id} отсутствует в каталоге"
    )

@product_router.delete("/{id}", summary="Удаление товара по ID")
async def delete_product(id: int = Path(..., gt=0)) -> dict:
    for product in products:
        if product.id == id:
            products.remove(product)
            return {"message": f"Товар с ID={id} успешно удален из каталога"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Товар с ID={id} не найден для удаления"
    )

@product_router.delete("/", summary="Очистить весь каталог")
async def delete_all_products() -> dict:
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Каталог уже пуст, нечего удалять"
        )
    products.clear()
    return {"message": "Все товары успешно удалены из каталога"}
