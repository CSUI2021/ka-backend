from fastapi import APIRouter

from ka_backend.routes.admin.competition import router as CompetitionRouter
from ka_backend.routes.admin.sig import router as SIGRouter
from ka_backend.routes.admin.story import router as StoryRouter

router = APIRouter(prefix="/admin", tags=["SIG"])
router.include_router(StoryRouter)
router.include_router(SIGRouter)
router.include_router(CompetitionRouter)