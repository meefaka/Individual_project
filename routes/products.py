from typing import List, Optional
from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Path, Query, status
from database.connection import Database
from models.products import Product, ProductUpdate

product_router = APIRouter(tags=["Товары каталога"])
product_database = Database(Product)

@product_router.get("/", response_model=List[Product], summary="Получение всех товаров с фильтрацией")
async def retrieve_all_products(
    brand: Optional[str] = Query(None, description="Фильтр по бренду (например, Apple, Samsung)"),
    category: Optional[str] = Query(None, description="Фильтр по категории (например, Смартфоны, Ноутбуки)")
) -> List[Product]:
    query = {}
    if brand:
        query["brand"] = {"$regex": f"^{brand}$", "$options": "i"}
    if category:
        query["category"] = {"$regex": f"^{category}$", "$options": "i"}

    products = await Product.find(query).to_list()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товары по заданным критериям не найдены"
        )
    return products

@product_router.get("/{id}", response_model=Product, summary="Получение товара по ID")
async def retrieve_product(id: PydanticObjectId = Path(..., description="ID товара в MongoDB")) -> Product:
    product = await product_database.get(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Товар с ID={id} не найден в каталоге"
        )
    return product

@product_router.post("/new", status_code=status.HTTP_201_CREATED, summary="Заведение товара в каталог")
async def create_product(body: Product) -> dict:
    existing_sku = await Product.find_one(Product.sku == body.sku)
    if existing_sku:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Товар с артикулом '{body.sku}' уже существует в базе"
        )
    await product_database.save(body)
    return {
        "message": "Товар успешно добавлен в MongoDB",
        "product_id": str(body.id)
    }

@product_router.put("/{id}", response_model=Product, summary="Обновление данных товара")
async def update_product(id: PydanticObjectId, body: ProductUpdate) -> Product:
    updated = await product_database.update(id, body)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Невозможно обновить: товар с ID={id} отсутствует в базе"
        )
    return updated

@product_router.delete("/{id}", summary="Удаление товара по ID")
async def delete_product(id: PydanticObjectId = Path(..., description="ID товара")) -> dict:
    deleted = await product_database.delete(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Товар с ID={id} не найден для удаления"
        )
    return {"message": f"Товар с ID={id} успешно удален из базы данных"}
