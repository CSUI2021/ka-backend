from fastapi import APIRouter

from ka_backend.routes.admin.story import router as StoryRouter

router = APIRouter(prefix="/admin", tags=["SIG"])
router.include_router(StoryRouter)
