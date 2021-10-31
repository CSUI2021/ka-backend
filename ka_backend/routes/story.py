from typing import List

from fastapi import APIRouter, Query

from ka_backend.models import Story

router = APIRouter(prefix="/story", tags=["Story"])


@router.get(
    "/list",
    response_model=List[Story],
    summary="Get Our Stories List",
)
async def get_story_list(
    page: int = Query(
        1,
        ge=1,
        description="Page to look over",
    ),
    limit: int = Query(
        10,
        ge=1,
        description="Number of results to return per page.",
    ),
):
    results = await Story.objects.paginate(page, limit).all()
    return results
