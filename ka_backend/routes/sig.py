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
    page_num: int = Query(1, ge=1), page_size: int = Query(10, ge=1)
):
    sig_list = await SIG.objects.paginate(page_num, page_size).all()
    return sig_list
