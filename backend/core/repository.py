"""Database repository pattern base"""

from typing import Generic, TypeVar, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Generic repository base class for database operations"""
    
    def __init__(self, db: AsyncSession, model_class: type[T]):
        self.db = db
        self.model_class = model_class
    
    async def create(self, obj: T) -> T:
        """Create a new object"""
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj
    
    async def get_by_id(self, id: int) -> Optional[T]:
        """Get object by ID"""
        return await self.db.get(self.model_class, id)
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all objects with pagination"""
        stmt = select(self.model_class).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def update(self, id: int, obj_data: dict) -> Optional[T]:
        """Update an object"""
        obj = await self.get_by_id(id)
        if not obj:
            return None
        
        for key, value in obj_data.items():
            setattr(obj, key, value)
        
        await self.db.commit()
        await self.db.refresh(obj)
        return obj
    
    async def delete(self, id: int) -> bool:
        """Delete an object"""
        obj = await self.get_by_id(id)
        if not obj:
            return False
        
        await self.db.delete(obj)
        await self.db.commit()
        return True
