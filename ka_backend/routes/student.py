import math
from typing import List, Literal, Optional

import ujson
from fastapi import APIRouter, HTTPException, Query, status

from ka_backend.models import Student
from ka_backend.plugins import redis
from ka_backend.responses import ErrorMessage, PagedData
from ka_backend.responses import Student as StudentFull
from ka_backend.responses import StudentSummary

router = APIRouter(prefix="/student", tags=["Students"])


@router.get(
    "/list",
    status_code=status.HTTP_200_OK,
    response_model=PagedData[StudentSummary],
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
    house: Optional[List[str]] = Query(
        None,
        description="Filters by major name.",
    ),
    sort: Literal["asc", "desc"] = Query(
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
    redis_key = f"student--list--{page}--{limit}"

    students = Student.objects.select_related("house").filter(npm__gte=2100000000)
    if name:
        students = students.filter(nama__icontains=name)
        redis_key += "--" + name.lower()
    if major:
        students = students.filter(jurusan__exact=major)
        redis_key += "--" + major
    if house:
        # Make all houses lowercase for case incensitive result
        house = [h.lower() for h in house]
        students = students.filter(house__codename__in=house)
        redis_key += "--" + "--".join(house)

    if sort == "asc":
        students = students.order_by("nama")
    elif sort == "desc":
        students = students.order_by("-nama")

    redis_key += "--" + sort
    if redis:
        result_cached = await redis.get(redis_key)
        if result_cached:
            return ujson.loads(result_cached)

    result = [
        await user.get_summary()
        for user in await students.paginate(page=page, page_size=limit).all()
    ]

    max_page = math.ceil((await students.count()) / limit)
    paged_result = {
        "data": result,
        "max_page": max_page,
        "has_next": page < max_page,
        "has_prev": page > 1,
    }

    if redis:
        await redis.set(redis_key, ujson.dumps(paged_result))
    return paged_result


@router.get(
    "/{username}",
    status_code=status.HTTP_200_OK,
    response_model=StudentFull,
    summary="Get Student Detail",
    responses={
        404: {"model": ErrorMessage, "description": "User is not found."},
        200: {"description": "Requested user's info."},
    },
)
async def show(username: str):
    redis_key = "student--detail--" + username
    if redis:
        result_cached = await redis.get(redis_key)
        if result_cached:
            return ujson.loads(result_cached)

    student = await Student.objects.select_related("house").get_or_none(
        username=username
    )
    if not student:
        raise HTTPException(status_code=404, detail="No such student found.")

    if redis:
        await redis.set(redis_key, ujson.dumps(student.dict()))
    return student
