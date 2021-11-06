from fastapi import APIRouter

from ka_backend.routes.admin.story import router as StoryRouter
from ka_backend.routes.admin.sig import router as SIGRouter

router = APIRouter(prefix="/admin", tags=["SIG"])
router.include_router(StoryRouter)
router.include_router(SIGRouter)
