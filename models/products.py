from typing import Dict, Optional
from beanie import Document
from pydantic import BaseModel, Field

class Product(Document):
    sku: str = Field(..., min_length=3, description="Артикул производителя (SKU)")
    name: str = Field(..., min_length=2, description="Название модели")
    brand: str = Field(..., min_length=2, description="Бренд производителя")
    category: str = Field(..., min_length=2, description="Категория техники")
    price: float = Field(..., gt=0, description="Цена в рублях")
    description: str = Field(..., min_length=5, description="Подробное описание товара")
    specifications: Dict[str, str] = Field(..., description="Технические характеристики")

    class Settings:
        name = "products"

    class Config:
        json_schema_extra = {
            "example": {
                "sku": "SAM-S24U-512",
                "name": "Samsung Galaxy S24 Ultra",
                "brand": "Samsung",
                "category": "Смартфоны",
                "price": 139990.0,
                "description": "Флагманский смартфон с титановым корпусом",
                "specifications": {
                    "Оперативная память": "12 ГБ",
                    "Процессор": "Snapdragon 8 Gen 3",
                    "Экран": "6.8 дюйма AMOLED 120 Гц",
                    "Встроенная память": "512 ГБ"
                }
            }
        }

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None
    specifications: Optional[Dict[str, str]] = None
