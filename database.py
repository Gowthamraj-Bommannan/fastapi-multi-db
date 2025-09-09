from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession
    )
from sqlalchemy.pool import NullPool
import os

DATABASE_URL_A = os.getenv("DATABASE_URL_A", "postgresql+asyncpg://gowthamraj:root@company_a-service:5433/company_a")
DATABASE_URL_B = os.getenv("DATABASE_URL_B", "postgresql+asyncpg://gowthamraj:root@company_b-service:5432/company")

engine_a = create_async_engine(DATABASE_URL_A, echo=False, future=True)
engine_b = create_async_engine(DATABASE_URL_B, echo=False, future=True)

AsyncSessionLocal_A = async_sessionmaker(
    engine_a,
    class_=AsyncSession,
    expire_on_commit=False,
)
AsyncSessionLocal_B = async_sessionmaker(
    engine_b,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db(company: str):
    if company == "company_a":
        db = AsyncSessionLocal_A()
    elif company == "company_b":
        db = AsyncSessionLocal_B()
    else:
        raise ValueError("Invalid company")
    
    try:
        yield db
    finally:
        await db.close()