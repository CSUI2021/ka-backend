from typing import List, Literal, Optional

from fastapi import APIRouter, HTTPException, Query, status

from ka_backend.models import Student

router = APIRouter(prefix="/student", tags=["Students"])


@router.get(
    "/list",
    status_code=status.HTTP_200_OK,
    response_model=List[Student],
    response_model_include={"nama", "house", "jurusan", "foto_diri"},
    summary="Get Student List",
)
async def list(
    name: Optional[str] = None,
    major: Optional[Literal["ilmu_komputer", "sistem_informasi"]] = None,
    house: Optional[str] = None,
    sort: Optional[Literal["asc", "desc"]] = "asc",
    page: int = Query(1, ge=1),
):
    students = Student.objects.select_related("house")
    if name:
        students = students.filter(nama__icontains=name)
    if major:
        students = students.filter(jurusan__exact=major)
    if house:
        students = students.filter(house__nama__exact=house)

    if sort == "asc":
        students = students.order_by("nama")
    elif sort == "desc":
        students = students.order_by("-nama")

    result = await students.paginate(page=page, page_size=10).all()
    return result


@router.get(
    "/{npm}",
    status_code=status.HTTP_200_OK,
    response_model=Student,
    response_model_exclude={"npm"},
    summary="Get Student Detail",
)
async def show(npm: int):
    student = await Student.objects.select_related("house").get_or_none(npm=npm)
    if not student:
        raise HTTPException(status_code=404, detail="No such student found.")
    return student
