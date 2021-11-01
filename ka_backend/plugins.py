from datetime import timedelta

from fastapi.templating import Jinja2Templates
from fastapi_login import LoginManager
from starlette.background import BackgroundTask
from starlette.templating import _TemplateResponse

from ka_backend.helper.settings import settings
from ka_backend.models import Student


class Templator(Jinja2Templates):
    def TemplateResponse(
        self,
        name: str,
        context: dict,
        status_code: int = 200,
        headers: dict = None,
        media_type: str = None,
        background: BackgroundTask = None,
    ) -> _TemplateResponse:
        result = super().TemplateResponse(
            name, context, status_code, headers, media_type, background
        )
        # Remove alert from session
        context["request"].session["alert"] = None
        return result


templates = Templator(directory="ka_backend/templates")
manager = LoginManager(
    settings.secret,
    "/auth/login",
    use_cookie=True,
    use_header=False,
    default_expiry=timedelta(hours=24),
)


@manager.user_loader()  # type: ignore
async def get_user(identifier):
    return await Student.objects.select_all().get_or_none(**identifier)
