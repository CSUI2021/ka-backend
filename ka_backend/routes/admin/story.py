from math import ceil
from typing import List

from black import traceback
from fastapi import APIRouter, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse

from ka_backend.models import Story
from ka_backend.plugins import templates

router = APIRouter(prefix="/story")


@router.get("/", response_class=HTMLResponse, name="story_index")
async def index(
    request: Request,
    page: int = Query(
        1,
        ge=1,
        description="Page to look over",
    ),
):
    total_stories = await Story.objects.count()
    stories = await Story.objects.paginate(page, 10).all()

    total_pages = ceil(total_stories / 10)
    has_prev = page > 1
    has_next = page < total_pages

    return templates.TemplateResponse(
        "story/index.html",
        {
            "request": request,
            "page": page,
            "total_pages": total_pages,
            "has_prev": has_prev,
            "has_next": has_next,
            "stories": stories,
        },
    )


@router.get("/{story_id}/edit", response_class=HTMLResponse, name="edit_story")
async def edit_story(request: Request, story_id: int):
    story = await Story.objects.get_or_none(id=story_id)
    if not story:
        raise HTTPException(404, detail="Story not found.")

    return templates.TemplateResponse(
        "story/edit.html",
        {
            "request": request,
            "story": story,
        },
    )


@router.post("/{story_id}/edit", response_class=RedirectResponse)
async def do_story_edit(
    request: Request,
    story_id: int,
    title: str = Form(...),
    detail: str = Form(...),
    foto: List[UploadFile] = File(...),
):
    story = await Story.objects.get_or_none(id=story_id)
    if not story:
        raise HTTPException(404, detail="Story not found.")

    # TODO: upload photos
    await story.update(title=title, detail=detail)
    request.session["alert"] = ("success", "Successfully edited story.")
    return RedirectResponse(url=request.url_for("story_index"), status_code=302)


@router.get("/new", response_class=HTMLResponse, name="new_story")
async def new_story(request: Request):
    return templates.TemplateResponse(
        "story/edit.html", {"request": request, "story": None}
    )


@router.post("/new", response_class=RedirectResponse)
async def do_new_story(
    request: Request,
    title: str = Form(...),
    detail: str = Form(...),
    foto: List[UploadFile] = File(...),
):
    try:
        await Story.objects.create(title=title, detail=detail, foto=[])
        request.session["alert"] = ("success", "Story created.")
    except:  # noqa
        traceback.print_exc()
        request.session["alert"] = (
            "danger",
            "An error an occured or data is not valid.",
        )
    return RedirectResponse(url=request.url_for("story_index"), status_code=302)


@router.post("/{story_id}/delete", response_class=RedirectResponse, name="delete_story")
async def delete_story(
    request: Request,
    story_id: int,
):
    story = await Story.objects.get_or_none(id=story_id)
    if not story:
        raise HTTPException(404, detail="Story not found.")

    await story.delete()
    request.session["alert"] = ("success", "Story removed.")
    return RedirectResponse(url=request.url_for("story_index"), status_code=302)
