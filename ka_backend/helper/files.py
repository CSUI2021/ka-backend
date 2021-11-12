from typing import Literal

import aiofiles
import random
import string
from fastapi import UploadFile

from ka_backend.helper.settings import settings


def generate_random(n: int) -> str:
    valid_chars = string.ascii_lowercase + string.digits
    return "".join([random.choice(valid_chars) for _ in range(n)])


async def save_file(
    category: Literal["SIG", "Competition", "Student", "Story"],
    file: UploadFile,
    save_as: str = None,
    randomize_name: bool = True,
):
    ext = file.filename.split(".")[-1]
    if randomize_name:
        filename = generate_random(16) + f".{ext}"
    else:
        filename = save_as or file.filename

    target_path = settings.upload_path / category.lower() / filename
    async with aiofiles.open(target_path, "wb") as f:
        await f.write(await file.read())

    return filename
