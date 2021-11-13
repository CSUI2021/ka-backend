from math import ceil
from typing import List, Optional

from fastapi import APIRouter, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from ka_backend.helper.files import save_file

from ka_backend.models import House, Student
from ka_backend.plugins import templates

router = APIRouter(prefix="/student")
VALID_INTERESTS = [
    "Data Science",
    "Networking & Security",
    "Competitive Programming",
    "App Development",
    "Web Development",
    "UI/UX Design",
    "Game Development",
    "Artifical Intelligence",
    "Cloud Computing",
    "Product Manager",
    "Quality Assurance",
    "Business Intelligence",
    "Internet of Things",
]


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
    students = await Student.objects.select_related("house").paginate(page, 25).all()

    total_pages = ceil(total_students / 25)
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
        "student/edit.html",
        {
            "request": request,
            "student": None,
            "houses": houses,
            "interests": VALID_INTERESTS,
        },
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
        house_object = await House.objects.get(nama=house)

        house_led: Optional[House]
        if ketua_house == "ya":
            house_led = house_object
        else:
            house_led = None

        foto_path = await save_file("Student", foto_diri)
        await Student.objects.create(
            npm=npm,
            username=username,
            nama=nama,
            jurusan=jurusan,
            house=house_object,
            house_led=house_led,
            ttl=ttl,
            hobi=hobi,
            interests=interests,
            twitter=twitter,
            line=line,
            instagram=instagram,
            foto_diri=foto_path,
            video_diri=video_diri,
            message=message,
            about=about,
        )
        request.session["alert"] = ("success", "Student created.")
    except:
        request.session["alert"] = (
            "danger",
            "An error has occured or data is not valid.",
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
        {
            "request": request,
            "student": student,
            "houses": houses,
            "interests": VALID_INTERESTS,
        },
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
    foto_diri: Optional[UploadFile] = File(...),
    video_diri: str = Form(...),
    message: str = Form(...),
    about: str = Form(...),
):
    student = await Student.objects.select_all().get_or_none(npm=npm)
    if not student:
        raise HTTPException(404, detail="student not found.")

    try:
        house_object = await House.objects.get(nama=house)

        house_led: Optional[House]
        if ketua_house == "ya":
            house_led = house_object
        else:
            house_led = None

            if student.house_led:
                # Explicitly reload house_led as we dont want to have
                # reference of it on student while working on it.
                ex_house_led = await student.house_led.load()
                await ex_house_led.ketua.remove(student)

        is_valid_photo = bool(await foto_diri.read(8))

        if is_valid_photo:
            await foto_diri.seek(0)
            foto_path = await save_file("Student", foto_diri)
        else:
            foto_path = student.foto_diri

        await student.update(
            nama=nama,
            jurusan=jurusan,
            house=house_object,
            house_led=house_led,
            ttl=ttl,
            hobi=hobi,
            interests=interests,
            twitter=twitter,
            line=line,
            instagram=instagram,
            foto_diri=foto_path,
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
