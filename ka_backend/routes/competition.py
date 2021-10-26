from typing import List

from fastapi import APIRouter, Query

from ka_backend.models import Competition

router = APIRouter(prefix="/competition")


@router.get("/list", response_model=List[Competition])
async def get_competition_list(
    page_num: int = Query(1, ge=1), page_size: int = Query(10, ge=1)
):
    competition_list = await Competition.objects.paginate(page_num, page_size).all()
    return competition_list
