from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from infrastructure.db.configuration import DATABASE_URL


engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(bind=engine,class_=AsyncSession, expire_on_commit=False)

Base=declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
