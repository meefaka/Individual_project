from typing import Dict, Optional
from pydantic import BaseModel, Field

class Product(BaseModel):
    id: int = Field(..., gt=0, description="Уникальный номер (ID) товара")
    sku: str = Field(..., min_length=3, description="Артикул производителя (заводской код товара / SKU)")
    name: str = Field(..., min_length=2, description="Название модели")
    brand: str = Field(..., min_length=2, description="Бренд производителя")
    category: str = Field(..., min_length=2, description="Категория техники")
    price: float = Field(..., gt=0, description="Цена в рублях (должна быть больше 0)")
    description: str = Field(..., min_length=5, description="Подробное описание товара")
    specifications: Dict[str, str] = Field(..., description="Технические характеристики (ОЗУ, процессор, дисплей)")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "sku": "SAM-S24U-512 (Артикул завода-изготовителя)",
                "name": "Samsung Galaxy S24 Ultra",
                "brand": "Samsung",
                "category": "Смартфоны",
                "price": 139990.0,
                "description": "Флагманский смартфон с титановым корпусом и искусственным интеллектом",
                "specifications": {
                    "Оперативная память": "12 ГБ",
                    "Процессор": "Snapdragon 8 Gen 3",
                    "Экран": "6.8 дюйма AMOLED 120 Гц",
                    "Встроенная память": "512 ГБ"
                }
            }
        }

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Название модели")
    brand: Optional[str] = Field(None, description="Бренд")
    category: Optional[str] = Field(None, description="Категория")
    price: Optional[float] = Field(None, gt=0, description="Новая цена в рублях")
    description: Optional[str] = Field(None, description="Новое описание")
    specifications: Optional[Dict[str, str]] = Field(None, description="Характеристики")
