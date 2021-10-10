from fastapi import Depends, FastAPI

from ka_backend.helper.database import database
from ka_backend.models import Student
from ka_backend.plugins import manager
from ka_backend.routes.auth import router as AuthRouter
from ka_backend.routes.sig import router as SigRouter
from ka_backend.routes.competition import router as CompetitionRouter


app = FastAPI()
app.include_router(AuthRouter)
app.include_router(SigRouter)
app.include_router(CompetitionRouter)


@app.get("/")
async def root():
    return {"message": "Hello world!"}


@app.get("/me", response_model=Student)
async def me(user: Student = Depends(manager)):
    return user


@app.on_event("startup")
async def on_startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def on_shutdown():
    if database.is_connected:
        await database.disconnect()
