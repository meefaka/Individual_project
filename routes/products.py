from typing import List, Optional
from fastapi import APIRouter, Body, HTTPException, Path, Query, status
from models.products import Product, ProductUpdate

product_router = APIRouter(tags=["Products"])

products: List[Product] = []

@product_router.get("/", response_model=List[Product])
async def retrieve_all_products(
    brand: Optional[str] = Query(None, description="Фильтр по бренду"),
    category: Optional[str] = Query(None, description="Фильтр по категории")
) -> List[Product]:
    res = products
    if brand:
        res = [p for p in res if p.brand.lower() == brand.lower()]
    if category:
        res = [p for p in res if p.category.lower() == category.lower()]
    return res

@product_router.get("/{id}", response_model=Product)
async def retrieve_product(id: int = Path(..., gt=0)) -> Product:
    for product in products:
        if product.id == id:
            return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Товар с ID={id} не найден"
    )

@product_router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_product(body: Product = Body(...)) -> dict:
    for product in products:
        if product.id == body.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Товар с ID={body.id} уже существует! Используйте другой идентификатор."
            )
        if product.sku == body.sku:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Товар с артикулом {body.sku} уже существует."
            )
    products.append(body)
    return {
        "message": "Товар успешно добавлен в каталог",
        "product_id": body.id
    }

@product_router.put("/{id}")
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
            return {"message": f"Товар с ID={id} успешно обновлен"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Невозможно обновить: товар с ID={id} отсутствует"
    )

@product_router.delete("/{id}")
async def delete_product(id: int = Path(..., gt=0)) -> dict:
    for product in products:
        if product.id == id:
            products.remove(product)
            return {"message": f"Товар с ID={id} успешно удален"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Товар с ID={id} не найден для удаления"
    )

@product_router.delete("/")
async def delete_all_products() -> dict:
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Каталог уже пуст, нечего удалять"
        )
    products.clear()
    return {"message": "Все товары успешно удалены из каталога"}
