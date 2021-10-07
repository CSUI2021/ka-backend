from datetime import timedelta

from fastapi_login import LoginManager

from ka_backend.models import Student
from ka_backend.helper.settings import settings


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
