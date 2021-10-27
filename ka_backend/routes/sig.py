from typing import List

from fastapi import APIRouter, Query

from ka_backend.models import SIG

router = APIRouter(prefix="/sig", tags=["SIG"])


@router.get(
    "/list",
    response_model=List[SIG],
    summary="Get SIG List",
)
async def get_sig_list(
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
    sig_list = await SIG.objects.paginate(page, limit).all()
    return sig_list
