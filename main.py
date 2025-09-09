# from fastapi import FastAPI
# from routers.routers import routers
# from database import engine_a, engine_b, Base
# import models, asyncio
# from exceptions.exception_handler import handle_exception
# from contextlib import asynccontextmanager

# async def create_tables():
#     async with engine_a.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     async with engine_b.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await create_tables()
#     yield

#     await engine_a.dispose()
#     await engine_b.dispose()

# app = FastAPI(
#     lifespan=lifespan,
#     title="User Management API",
#     description="API for user management",
#     version="1.0.0",
#     )

# @app.get("/health")
# async def health_check():
#     return {"status": "healthy", "message": "User Management API is running"}

# app.include_router(routers)
# handle_exception(app)


from fastapi import FastAPI
from routers.routers import routers
from database import engine_a, engine_b, Base
import models, asyncio
from exceptions.exception_handler import handle_exception
from contextlib import asynccontextmanager
import time
import logging
from sqlalchemy import text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def wait_for_database(engine, db_name, max_retries=30, delay=2):
    """Wait for database to be ready with retry logic"""
    for attempt in range(max_retries):
        try:
            async with engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            logger.info(f"Database {db_name} is ready!")
            return True
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1}/{max_retries} - Database {db_name} not ready: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(delay)
            else:
                logger.error(f"Failed to connect to {db_name} after {max_retries} attempts")
                raise e

async def create_tables():
    """Create tables with database readiness check"""
    logger.info("Waiting for databases to be ready...")
    
    # Wait for both databases to be ready
    await wait_for_database(engine_a, "company_a")
    await wait_for_database(engine_b, "company_b")
    
    logger.info("Creating tables...")
    async with engine_a.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with engine_b.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Tables created successfully!")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

    await engine_a.dispose()
    await engine_b.dispose()

app = FastAPI(
    lifespan=lifespan,
    title="User Management API",
    description="API for user management",
    version="1.0.0",
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "User Management API is running"}

app.include_router(routers)
handle_exception(app)