import dotenv
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
dotenv.load_dotenv()

db_url = os.getenv("DATABASE_URL")
api_key = os.getenv("NEWS_API_KEY")  # Replace with your actual API key
engine = create_async_engine(db_url, echo=True)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


