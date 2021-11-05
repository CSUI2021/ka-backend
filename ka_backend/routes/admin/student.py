from math import ceil
from typing import List

from black import traceback
from fastapi import APIRouter, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse

from ka_backend.models import Story, Student, House
from ka_backend.plugins import templates

router = APIRouter(prefix="/student")


@router.get("/", response_class=HTMLResponse, name="student_index")
async def index(
    request: Request,
    page: int = Query(
        1,
        ge=1,
        description="Page to look over",
    ),
):
    total_students = await Student.objects.count()
    students = await Student.objects.paginate(page, 10).all()

    total_pages = ceil(total_students / 10)
    has_prev = page > 1
    has_next = page < total_pages

    return templates.TemplateResponse(
        "student/index.html",
        {
            "request": request,
            "page": page,
            "total_pages": total_pages,
            "has_prev": has_prev,
            "has_next": has_next,
            "students": students,
        },
    )


@router.get("/new", response_class=HTMLResponse, name="new_student")
async def new_story(request: Request):
    return templates.TemplateResponse(
        "student/edit.html", {"request": request, "student": None}
    )
