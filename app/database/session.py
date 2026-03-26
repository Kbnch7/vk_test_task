from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    echo=True, # для разработки, убрать потом
    pool_size=5,
)

AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    """Генератор асинхронных сессий для dependency injection"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            pass