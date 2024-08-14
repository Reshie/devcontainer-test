from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine

from app import models, routers

app = FastAPI()
app.mount("/static", StaticFiles(directory="./app/static"), name="static")

app.include_router(routers.router)
