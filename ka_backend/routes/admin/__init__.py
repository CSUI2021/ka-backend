from fastapi import APIRouter

from ka_backend.routes.admin.story import router as StoryRouter
from ka_backend.routes.admin.student import router as StudentRouter

router = APIRouter(prefix="/admin", tags=["SIG"])
router.include_router(StoryRouter)
router.include_router(StudentRouter)
