from typing import cast

from black import traceback
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from ka_backend.helper.settings import settings
from ka_backend.models import Student
from ka_backend.plugins import manager
from ka_backend.sso.client import AuthError, UIClient
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
    except AuthError:
        return {"err": "Authentication failure. Please try again."}
    except Exception:
        traceback.print_exc()
        return {"err": "An error has occured."}

    kd = sso_response["attributes"]["kd_attributes"]
    if kd and kd["faculty"] != "ILMU KOMPUTER":
        raise HTTPException(
            status_code=401,
            detail="This service is only available for Faculty of Computer Science students.",
        )

    kd = cast(KDAttributes, kd)
    user = await Student.objects.get_or_create(npm=sso_response["attributes"]["npm"])
    jurusan_name = "_".join(kd["study_program"].split()[:2])
    await user.update(
        nama=sso_response["attributes"]["nama"],
        jurusan=jurusan_name.lower(),
    )

    response = HTMLResponse(
        content="""<script>window.opener.postMessage("logged", "*")</script>"""
    )
    token = manager.create_access_token(data=dict(sub=dict(npm=user.npm)))
    manager.set_cookie(response, token)
    return response


@router.get("/logout")
async def logout(user: Student = Depends(manager)):
    response = JSONResponse(content={"message": "Logged out."})
    response.set_cookie("access-token")
    return response
