from fastapi import Depends, FastAPI

from ka_backend import __version__, __description__
from ka_backend.helper.database import database
from ka_backend.models import Student
from ka_backend.plugins import manager
from ka_backend.responses import ErrorMessage, StudentSummary
from ka_backend.routes.auth import router as AuthRouter
from ka_backend.routes.competition import router as CompetitionRouter
from ka_backend.routes.sig import router as SigRouter
from ka_backend.routes.student import router as StudentRouter

tags_metadata = [
    {
        "name": "Users",
        "description": "Operations related to users and authentication.",
    },
    {"name": "SIG", "description": "SIG related operations."},
    {"name": "Students", "description": "Students related operations."},
]

app = FastAPI(
    openapi_tags=tags_metadata,
    title="Karya Angkatan",
    version=__version__,
    description=__description__,
)
app.include_router(AuthRouter)
app.include_router(SigRouter)
app.include_router(CompetitionRouter)
app.include_router(StudentRouter)


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Hello world!"}


@app.get(
    "/me",
    response_model=StudentSummary,
    summary="Get Current User",
    tags=["Users"],
    responses={
        401: {"model": ErrorMessage, "description": "User is unauthenticated."},
        200: {"description": "Authenticated user's info."},
    },
)
async def me(user: Student = Depends(manager)):
    """Gets currently authenticated user's data.

    If there is no authenticated user or session has expired, it will return a 401 response."""
    return await user.get_summary()


@app.on_event("startup")
async def on_startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def on_shutdown():
    if database.is_connected:
        await database.disconnect()
