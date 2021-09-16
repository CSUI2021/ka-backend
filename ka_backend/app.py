from fastapi import FastAPI
from ka_backend.helper.database import database

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello world!"}


@app.on_event("startup")
async def on_startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def on_shutdown():
    if database.is_connected:
        await database.disconnect()
