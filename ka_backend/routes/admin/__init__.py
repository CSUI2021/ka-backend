from fastapi import APIRouter

from ka_backend.routes.admin.competition import router as CompetitionRouter
from ka_backend.routes.admin.sig import router as SIGRouter
from ka_backend.routes.admin.story import router as StoryRouter
from ka_backend.routes.admin.student import router as StudentRouter

router = APIRouter(prefix="/admin", include_in_schema=False)
router.include_router(StoryRouter)
router.include_router(SIGRouter)
router.include_router(CompetitionRouter)
router.include_router(StudentRouter)
