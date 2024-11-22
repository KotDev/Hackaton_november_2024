import uuid
from pathlib import Path

from fastapi import Request


from settings import MEDIA_PROFILE_PATH


class MediaLogic:

    @staticmethod
    async def save_photo(request: Request) -> str:
        form = await request.form()
        file = form.get("file")
        file_name = f"{uuid.uuid4()}_{file.filename.lower()}"
        file_path: Path = MEDIA_PROFILE_PATH / "photo_profile" / file_name.lower()
        with open(str(file_path), "wb") as f:
            f.write(await file.read())
        return str(file_path)

