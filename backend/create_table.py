import asyncio

from infrastructure.db.database import engine, Base
from infrastructure.db.orm.factory_data import FactoryDataEntity
from infrastructure.db.orm.predict_data import PredictDataEntity


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_tables())