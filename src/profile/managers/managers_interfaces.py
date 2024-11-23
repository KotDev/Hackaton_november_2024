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
    async def add_profile(self, user_id: int):
        pass


class BusinessFormManagerInterface(ABC):

    @abstractmethod
    async def get_business_form(self, business_form_id: int | None, **kwargs):
        pass

    @abstractmethod
    async def update_business_form(self, business_form_id: int | None, update_data: dict, **kwargs):
        pass

    @abstractmethod
    async def delete_business_form(self, business_form_id: int | None, **kwargs):
        pass

    @abstractmethod
    async def add_business_form(self, profile_id: int):
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
