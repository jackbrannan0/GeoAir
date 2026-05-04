import asyncio
from backend.db.session import AsyncSessionLocal, engine
from backend.db.models import GeoPoliticalEvent, Base

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def reset_tables():
    # WARNING: This wipes the entire database schema for a fresh start
    async with engine.begin() as conn:
        # Logic: Completely erase the old table structure
        await conn.run_sync(Base.metadata.drop_all)
        print("Dropped all existing tables.")
        
        # Logic: Recreate everything from scratch with the 'url' column
        await conn.run_sync(Base.metadata.create_all)
        print("Created all tables successfully.")

if __name__ == "__main__":
    asyncio.run(reset_tables())