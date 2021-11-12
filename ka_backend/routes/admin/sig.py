from math import ceil
from typing import Optional

from black import traceback
from fastapi import APIRouter, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from ka_backend.helper.files import save_file

from ka_backend.models import SIG
from ka_backend.plugins import templates

ROWS_PER_PAGE = 10

router = APIRouter(prefix="/sig")


@router.get("/", response_class=HTMLResponse, name="sig_index")
async def view_index(
    request: Request,
    page: int = Query(
        1,
        ge=1,
        description="Page to look over",
    ),
):
    total_sig = await SIG.objects.count()
    sig_list = await SIG.objects.paginate(page, ROWS_PER_PAGE).all()

    total_pages = ceil(total_sig / ROWS_PER_PAGE)
    has_prev = page > 1
    has_next = page < total_pages

    return templates.TemplateResponse(
        "sig/index.html",
        {
            "request": request,
            "page": page,
            "total_pages": total_pages,
            "has_prev": has_prev,
            "has_next": has_next,
            "sig_list": sig_list,
        },
    )


@router.get("/{sig_id}/edit", response_class=HTMLResponse, name="edit_sig")
async def view_edit_sig(request: Request, sig_id: int):
    sig = await SIG.objects.get_or_none(id=sig_id)
    if not sig:
        raise HTTPException(404, detail="SIG not found.")

    return templates.TemplateResponse(
        "sig/edit.html",
        {
            "request": request,
            "sig": sig,
        },
    )


@router.post("/{sig_id}/edit", response_class=RedirectResponse)
async def edit_sig(
    request: Request,
    sig_id: int,
    nama: str = Form(...),
    detail: str = Form(...),
    is_it_interest: Optional[bool] = Form(False),
):
    sig = await SIG.objects.get_or_none(id=sig_id)
    if not sig:
        raise HTTPException(404, detail="SIG not found.")

    await sig.update(
        nama=nama,
        detail=detail,
        is_it_interest=is_it_interest,
    )
    request.session["alert"] = ("success", "Successfully edited sig.")
    return RedirectResponse(url=request.url_for("sig_index"), status_code=302)


@router.get("/new", response_class=HTMLResponse, name="new_sig")
async def view_new_sig(request: Request):
    return templates.TemplateResponse(
        "sig/edit.html", {"request": request, "sig": None}
    )


@router.post("/new", response_class=RedirectResponse)
async def new_sig(
    request: Request,
    nama: str = Form(...),
    detail: str = Form(...),
    is_it_interest: Optional[bool] = Form(False),
):
    try:
        await SIG.objects.create(
            nama=nama,
            detail=detail,
            is_it_interest=is_it_interest,
        )
        request.session["alert"] = ("success", "SIG created.")
    except:  # noqa
        traceback.print_exc()
        request.session["alert"] = (
            "danger",
            "An error an occured or data is not valid.",
        )
    return RedirectResponse(url=request.url_for("sig_index"), status_code=302)


@router.post("/{sig_id}/delete", response_class=RedirectResponse, name="delete_sig")
async def delete_sig(
    request: Request,
    sig_id: int,
):
    sig = await SIG.objects.get_or_none(id=sig_id)
    if not sig:
        raise HTTPException(404, detail="SIG not found.")

    await sig.delete()
    request.session["alert"] = ("success", "SIG removed.")
    return RedirectResponse(url=request.url_for("sig_index"), status_code=302)
