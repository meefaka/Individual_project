from typing import Any, List, Optional
from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = "mongodb://localhost:27017/electronics_catalog"

    async def initialize_database(self):
        from models.products import Product
        from models.users import User
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(
            database=client.get_default_database(),
            document_models=[Product, User]
        )

    class Config:
        env_file = ".env"

class Database:
    def __init__(self, model):
        self.model = model

    async def save(self, document) -> None:
        await document.create()
        return

    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        doc = await self.get(id)
        if not doc:
            return False
        des_body = body.model_dump(exclude_unset=True) if hasattr(body, "model_dump") else body.dict(exclude_unset=True)
        update_query = {"$set": {k: v for k, v in des_body.items() if v is not None}}
        await doc.update(update_query)
        return await self.get(id)

    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True
