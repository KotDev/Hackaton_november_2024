from profile.schemas import *

from abc import ABC, abstractmethod

class ProfileManagerInterface(ABC):

    @abstractmethod
    async def get_profile(self, profile_id: int | None, **kwargs):
        pass

    @abstractmethod
    async def update_profile(self, profile_id: int | None, update_data: dict, **kwargs):
        pass

    @abstractmethod
    async def delete_profile(self, profile_id: int | None, **kwargs):
        pass

    @abstractmethod
    async def add_profile(self, user_id: int, schema: ProfileSchema):
        pass


class PhotoManagerInterface(ABC):

    @abstractmethod
    async def get_photo(self, photo_id: int | None, **kwargs):
        pass

    @abstractmethod
    async def update_photo(self, photo_id: int | None, update_data: dict, **kwargs):
        pass

    @abstractmethod
    async def delete_photo(self, photo_id: int | None, **kwargs):
        pass

    @abstractmethod
    async def add_photo(self, schema:PhotoSchema):
        pass


class NewsManagerInterface(ABC):

    @abstractmethod
    async def get_news(self, news_id: int | None, **kwargs):
        pass

    @abstractmethod
    async def update_news(self, news_id: int | None, update_data: dict, **kwargs):
        pass

    @abstractmethod
    async def delete_news(self, news_id: int | None, **kwargs):
        pass

    @abstractmethod
    async def add_news(self, schema=NewsSchema):
        pass

    @abstractmethod
    async def get_news_by_tag(self, tag_id: int | None, **kwargs):
        pass


class TagManagerInterface(ABC):

    @abstractmethod
    async def get_tag(self, tag_id: int | None, **kwargs):
        pass

    @abstractmethod
    async def update_tag(self, tag_id: int | None, update_data: dict, **kwargs):
        pass

    @abstractmethod
    async def delete_tag(self, tag_id: int | None, **kwargs):
        pass

    @abstractmethod
    async def add_tag(self, schema: TagSchema):
        pass

    @abstractmethod
    async def get_tags_for_news(self, news_id: int | None, **kwargs):
        pass

