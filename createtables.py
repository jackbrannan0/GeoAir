import asyncio
from backend.db.session import AsyncSessionLocal, engine
from backend.db.models import GeoPoliticalEvent, Base

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())