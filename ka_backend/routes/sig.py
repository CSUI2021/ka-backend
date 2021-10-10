from typing import List
from fastapi import APIRouter
from ka_backend.models import SIG

router = APIRouter(prefix="/sig")


@router.get("/list", response_model=List[SIG])
async def get_sig_list():
    sig_list = await SIG.objects.all()
    return sig_list
