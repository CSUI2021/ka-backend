from black import traceback
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from typing import cast
from ka_backend.helper.settings import settings
from ka_backend.models import Student
from ka_backend.plugins import manager
from ka_backend.sso.client import UIClient
from ka_backend.sso.types import KDAttributes

router = APIRouter(prefix="/auth")
client = UIClient(f"http://{settings.hostname}/auth/callback")


@router.get("/login")
def login():
    return RedirectResponse(client.login_url)


@router.get("/callback")
async def callback(ticket: str = Query(...)):
    try:
        sso_response = await client.authenticate(ticket)
    except Exception:
        traceback.print_exc()
        return {"err": "An error has occured."}

    kd = sso_response["attributes"]["kd_attributes"]
    kd = cast(KDAttributes, kd)
    if kd["faculty"] != "ILMU KOMPUTER":
        raise HTTPException(
            status_code=401,
            detail="This service is only available for Faculty of Computer Science students.",
        )

    user = await Student.objects.get_or_none(npm=sso_response["attributes"]["npm"])
    if not user:
        jurusan_name = "_".join(kd["study_program"].split()[:2])
        user = await Student.objects.create(
            npm=sso_response["attributes"]["npm"],
            nama=sso_response["attributes"]["nama"],
            jurusan=jurusan_name.lower(),
        )

    response = HTMLResponse(
        content="""<script>window.opener.postMessage("logged", "*")</script>"""
    )
    token = manager.create_access_token(
        data=dict(
            sub=dict(
                npm=user.npm,
            )
        )
    )
    manager.set_cookie(response, token)
    return response


@router.get("/logout")
async def logout(user: Student = Depends(manager)):
    response = JSONResponse(content={"message": "Logged out."})
    response.set_cookie("access-token")
    return response
