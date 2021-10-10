from typing import List
from fastapi import APIRouter
from ka_backend.models import Competition

router = APIRouter(prefix="/competition")


@router.get("/list", response_model=List[Competition])
async def get_competition_list():
    competition_list = await Competition.objects.all()
    return competition_list
