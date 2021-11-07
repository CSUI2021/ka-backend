from fastapi import APIRouter, Depends, HTTPException

from ka_backend.models import Student
from ka_backend.plugins import manager
from ka_backend.routes.admin.competition import router as CompetitionRouter
from ka_backend.routes.admin.sig import router as SIGRouter
from ka_backend.routes.admin.story import router as StoryRouter
from ka_backend.routes.admin.student import router as StudentRouter


async def ensure_admin(user: Student = Depends(manager)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized.")
    return True


router = APIRouter(
    prefix="/admin",
    include_in_schema=False,
    dependencies=[Depends(ensure_admin)],
)
router.include_router(StoryRouter)
router.include_router(SIGRouter)
router.include_router(CompetitionRouter)
router.include_router(StudentRouter)
