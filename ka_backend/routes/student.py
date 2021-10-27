from typing import List, Literal, Optional

from fastapi import APIRouter, HTTPException, Query, status

from ka_backend.models import Student
from ka_backend.responses import StudentSummary

router = APIRouter(prefix="/student", tags=["Students"])


@router.get(
    "/list",
    status_code=status.HTTP_200_OK,
    response_model=List[StudentSummary],
    summary="Get Student List",
)
async def list(
    name: Optional[str] = Query(
        None,
        description="Name of student to search.",
    ),
    major: Optional[Literal["ilmu_komputer", "sistem_informasi"]] = Query(
        None,
        description="Filters by major name.",
    ),
    house: Optional[str] = Query(
        None,
        description="Filters by major name.",
    ),
    sort: Optional[Literal["asc", "desc"]] = Query(
        "asc",
        description="Name sorting order.",
    ),
    page: int = Query(
        1,
        ge=1,
        description="Page to look over",
    ),
    limit: int = Query(
        20,
        ge=1,
        description="Number of results to return per page.",
    ),
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

    result = [
        await user.get_summary()
        for user in await students.paginate(page=page, page_size=limit).all()
    ]
    return result


@router.get(
    "/{username}",
    status_code=status.HTTP_200_OK,
    response_model=Student,
    response_model_exclude={"npm"},
    summary="Get Student Detail",
)
async def show(username: str):
    student = await Student.objects.select_related("house").get_or_none(
        username=username
    )
    if not student:
        raise HTTPException(status_code=404, detail="No such student found.")
    return student
