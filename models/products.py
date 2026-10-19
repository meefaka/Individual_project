from typing import Dict, Optional
from pydantic import BaseModel, Field

class Product(BaseModel):
    id: int = Field(..., gt=0, description="ID товара должен быть больше 0")
    sku: str = Field(..., min_length=3, description="Уникальный артикул (SKU)")
    name: str = Field(..., min_length=2, description="Название не должно быть пустым")
    brand: str = Field(..., min_length=2, description="Бренд производителя")
    category: str = Field(..., min_length=2, description="Категория техники")
    price: float = Field(..., gt=0, description="Цена должна быть больше 0")
    description: str = Field(..., min_length=5, description="Описание минимум 5 символов")
    specifications: Dict[str, str] = Field(..., description="Характеристики устройства")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "sku": "SM-S928B",
                "name": "Samsung Galaxy S24 Ultra",
                "brand": "Samsung",
                "category": "Смартфоны",
                "price": 119990.0,
                "description": "Флагманский смартфон с титановым корпусом и AI",
                "specifications": {
                    "RAM": "12 ГБ",
                    "CPU": "Snapdragon 8 Gen 3",
                    "Display": "6.8 AMOLED 120Hz"
                }
            }
        }

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    specifications: Optional[Dict[str, str]] = None
