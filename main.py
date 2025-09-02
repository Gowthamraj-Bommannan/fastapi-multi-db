from fastapi import FastAPI
from routers.routers import routers
from database import engine_a, engine_b, Base
import models


Base.metadata.create_all(bind=engine_a)
Base.metadata.create_all(bind=engine_b)

app = FastAPI()
app.include_router(routers)