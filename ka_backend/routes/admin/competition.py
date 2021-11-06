from math import ceil
from typing import Optional

from black import traceback
from fastapi import APIRouter, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse

from ka_backend.models import Competition
from ka_backend.plugins import templates

ROWS_PER_PAGE = 10

router = APIRouter(prefix="/competition")


@router.get("/", response_class=HTMLResponse, name="competition_index")
async def view_index(
    request: Request,
    page: int = Query(
        1,
        ge=1,
        description="Page to look over",
    ),
):
    total_competition = await Competition.objects.count()
    competitions = await Competition.objects.paginate(page, ROWS_PER_PAGE).all()

    total_pages = ceil(total_competition / ROWS_PER_PAGE)
    has_prev = page > 1
    has_next = page < total_pages

    return templates.TemplateResponse(
        "competition/index.html",
        {
            "request": request,
            "page": page,
            "total_pages": total_pages,
            "has_prev": has_prev,
            "has_next": has_next,
            "competitions": competitions,
        },
    )


@router.get("/{competition_id}/edit", response_class=HTMLResponse, name="edit_competition")
async def view_edit_competition(request: Request, competition_id: int):
    competition = await Competition.objects.get_or_none(id=competition_id)
    if not competition:
        raise HTTPException(404, detail="Competition not found.")

    return templates.TemplateResponse(
        "competition/edit.html",
        {
            "request": request,
            "competition": competition,
        },
    )


@router.post("/{competition_id}/edit", response_class=RedirectResponse)
async def edit_competition(
    request: Request,
    competition_id: int,
    nama: str = Form(...),
    foto: UploadFile = File(...),
    link: str = Form(...),
):
    competition = await Competition.objects.get_or_none(id=competition_id)
    if not competition:
        raise HTTPException(404, detail="Competition not found.")
    # TODO: store foto
    await competition.update(nama=nama, link=link)
    request.session["alert"] = ("success", "Successfully edited competition.")
    return RedirectResponse(url=request.url_for("competition_index"), status_code=302)


@router.get("/new", response_class=HTMLResponse, name="new_competition")
async def view_new_competition(request: Request):
    return templates.TemplateResponse(
        "competition/edit.html", {"request": request, "competition": None}
    )


@router.post("/new", response_class=RedirectResponse)
async def new_competition(
    request: Request,
    nama: str = Form(...),
    foto: UploadFile = File(...),
    link: str = Form(...),
):
    try:
        await Competition.objects.create(nama=nama, link=link)
        request.session["alert"] = ("success", "Competition created.")
    except:  # noqa
        traceback.print_exc()
        request.session["alert"] = (
            "danger",
            "An error an occured or data is not valid.",
        )
    return RedirectResponse(url=request.url_for("competition_index"), status_code=302)


@router.post("/{competition_id}/delete", response_class=RedirectResponse, name="delete_competition")
async def delete_competition(
    request: Request,
    competition_id: int,
):
    competition = await Competition.objects.get_or_none(id=competition_id)
    if not competition:
        raise HTTPException(404, detail="Competition not found.")

    await competition.delete()
    request.session["alert"] = ("success", "Competition removed.")
    return RedirectResponse(url=request.url_for("competition_index"), status_code=302)
