from os import stat
from fastapi import APIRouter, status, Query
from typing import Optional, List
from ..models import House, Student

router = APIRouter(prefix="/student")


@router.get(
    "/list",
    status_code=status.HTTP_200_OK,
    response_model=List[Student],
    response_model_include={"nama", "house", "jurusan", "foto_diri"},
)
async def list(search_name: Optional[str] = None, page: int = Query(1)):
    if search_name:
        students = (
            await Student.objects.select_related("house")
            .filter(nama__icontains=search_name)
            .order_by("nama")
            .paginate(page=page, page_size=10)
            .all()
        )
    else:
        students = (
            await Student.objects.select_related("house")
            .order_by("nama")
            .paginate(page=page, page_size=10)
            .all()
        )
    return students


@router.get(
    "/{npm}",
    status_code=status.HTTP_200_OK,
    response_model=Student,
    response_model_exclude={"npm"},
)
async def show(npm: int):
    student = await Student.objects.select_related("house").get(npm=npm)
    return student
