from math import ceil
from typing import List

from fastapi import APIRouter, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse

from ka_backend.models import Student, House
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
    students = await Student.objects.select_related("house").paginate(page, 10).all()

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
async def new_student(request: Request):
    houses = await House.objects.all()
    return templates.TemplateResponse(
        "student/edit.html", {"request": request, "student": None, "houses": houses}
    )


@router.post("/new", response_class=RedirectResponse)
async def do_new_student(
    request: Request,
    npm: int = Form(...),
    username: str = Form(...),
    nama: str = Form(...),
    jurusan: str = Form(...),
    house: str = Form(...),
    ketua_house: str = Form(...),
    ttl: str = Form(...),
    hobi: str = Form(...),
    interests: List[str] = Form(...),
    twitter: str = Form(...),
    line: str = Form(...),
    instagram: str = Form(...),
    foto_diri: UploadFile = File(...),
    video_diri: str = Form(...),
    message: str = Form(...),
    about: str = Form(...),
):
    try:
        house = await House.objects.get(nama=house)
        if ketua_house == "ya":
            await Student.objects.create(
                npm=npm,
                username=username,
                nama=nama,
                jurusan=jurusan,
                house=house,
                house_led=house,
                ttl=ttl,
                hobi=hobi,
                interests=interests,
                twitter=twitter,
                line=line,
                instagram=instagram,
                video_diri=video_diri,
                message=message,
                about=about,
            )
        else:
            await Student.objects.create(
                npm=npm,
                username=username,
                nama=nama,
                jurusan=jurusan,
                house=house,
                ttl=ttl,
                hobi=hobi,
                interests=interests,
                twitter=twitter,
                line=line,
                instagram=instagram,
                video_diri=video_diri,
                message=message,
                about=about,
            )
        request.session["alert"] = ("success", "Student created.")
    except:
        request.session["alert"] = (
            "danger",
            "An error an occured or data is not valid.",
        )
    return RedirectResponse(url=request.url_for("student_index"), status_code=302)


@router.get("/{npm}/edit", response_class=HTMLResponse, name="edit_student")
async def edit_student(request: Request, npm: int):
    student = await Student.objects.select_related("house").get_or_none(npm=npm)
    if not student:
        raise HTTPException(404, detail="student not found.")

    houses = await House.objects.all()

    return templates.TemplateResponse(
        "student/edit.html",
        {"request": request, "student": student, "houses": houses},
    )


@router.post("/{npm}/edit", response_class=RedirectResponse)
async def do_edit_student(
    request: Request,
    npm: int,
    nama: str = Form(...),
    jurusan: str = Form(...),
    house: str = Form(...),
    ketua_house: str = Form(...),
    ttl: str = Form(...),
    hobi: str = Form(...),
    interests: List[str] = Form(...),
    twitter: str = Form(...),
    line: str = Form(...),
    instagram: str = Form(...),
    foto_diri: UploadFile = File(...),
    video_diri: str = Form(...),
    message: str = Form(...),
    about: str = Form(...),
):
    student = await Student.objects.select_related("house").get_or_none(npm=npm)
    if not student:
        raise HTTPException(404, detail="student not found.")

    try:
        house = await House.objects.get(nama=house)
        if ketua_house == "ya":
            await student.update(
                nama=nama,
                jurusan=jurusan,
                house=house,
                house_led=house,
                ttl=ttl,
                hobi=hobi,
                interests=interests,
                twitter=twitter,
                line=line,
                instagram=instagram,
                video_diri=video_diri,
                message=message,
                about=about,
            )
        else:
            await student.update(
                nama=nama,
                jurusan=jurusan,
                house=house,
                house_led=None,
                ttl=ttl,
                hobi=hobi,
                interests=interests,
                twitter=twitter,
                line=line,
                instagram=instagram,
                video_diri=video_diri,
                message=message,
                about=about,
            )
        request.session["alert"] = ("success", "Student edited.")
    except:
        request.session["alert"] = (
            "danger",
            "An error an occured or data is not valid.",
        )
    return RedirectResponse(url=request.url_for("student_index"), status_code=302)


@router.post("/{npm}/delete", response_class=RedirectResponse, name="delete_student")
async def delete_student(
    request: Request,
    npm: int,
):
    student = await Student.objects.get_or_none(npm=npm)
    if not student:
        raise HTTPException(404, detail="student not found.")

    await student.delete()
    request.session["alert"] = ("success", "student removed.")
    return RedirectResponse(url=request.url_for("student_index"), status_code=302)
