from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database import DataBase
from .managers_interfaces import *
from profile.models.model import *
from ..schemas import *


class ProfileManager(DataBase, ProfileManagerInterface):
    def __init__(self):
        super().__init__()

    async def get_profile(self, profile_id: int | None, **kwargs):
        return await self.get_obj(profile_id, Profile, **kwargs)

    async def delete_profile(self, profile_id: int | None, **kwargs):
        return await self.delete_obj(profile_id, Profile, **kwargs)

    async def update_profile(self, profile_id: int | None, update_data: dict, **kwargs):
        return await self.update_obj(profile_id, Profile, update_data, **kwargs)

    async def add_profile(self, user_id: int, schema: ProfileSchema):
        async  with self.async_session() as session:
            data = schema.model_dump()
            data["profile_id"] = user_id
            profile = Profile(**data)
            session.add(profile)
            await session.commit()
        return profile


    async def get_full_data_profile(self, profile_id: Optional[int] = None, **kwargs):
        async with self.async_session() as session:
            filters = []

            if profile_id:
                filters.append(Profile.profile_id == profile_id)

            filters += self.get_filters(Profile, kwargs)

            query = (
                select(Profile)
                .options(
                    joinedload(Profile.user),
                    joinedload(Profile.buisness_forms),
                )
                .filter(*filters)
            )
            result = await session.execute(query)
            return result


class PhotoManager(DataBase, PhotoManagerInterface):
    def __init__(self):
        super().__init__()

    async def get_photo(self, photo_id: int | None, **kwargs):
        return await self.get_obj(photo_id, Photo, **kwargs)


    async def delete_photo(self, photo_id: int | None, **kwargs):
        return await self.delete_obj(photo_id, Photo, **kwargs)


    async def update_photo(self, photo_id: int | None, update_data: dict, **kwargs):
        return await self.delete_obj(photo_id, Photo, **kwargs)

    async def add_photo(self, schema=PhotoSchema):
        async  with self.async_session() as session:
            photo = Photo(**schema.model_dump())
            session.add(photo)
            await session.commit()
        return photo

