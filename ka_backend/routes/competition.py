from typing import List

from fastapi import APIRouter, Query

from ka_backend.models import Competition

router = APIRouter(prefix="/competition", tags=["SIG"])


@router.get(
    "/list",
    response_model=List[Competition],
    summary="Get Competition List",
)
async def get_competition_list(
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
    competition_list = await Competition.objects.paginate(page, limit).all()
    return competition_list
