from fastapi import FastAPI
from routers.routers import routers
from database import engine_a, engine_b, Base
import models, asyncio
from exceptions.exception_handler import handle_exception
from contextlib import asynccontextmanager

async def create_tables():
    async with engine_a.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with engine_b.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

    await engine_a.dispose()
    await engine_b.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(routers)
handle_exception(app)