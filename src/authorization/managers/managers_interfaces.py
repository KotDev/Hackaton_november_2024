from authorization.schemas import RegisterSchema
from abc import ABC, abstractmethod

class UserManagerInterface(ABC):

    @abstractmethod
    async def get_user(self, user_id: int | None, **kwargs):
        pass

    @abstractmethod
    async def update_user(self, user_id: int | None, new_data: dict, **kwargs):
        pass

    @abstractmethod
    async def delete_user(self, user_id: int | None, **kwargs):
        pass

    @abstractmethod
    async def add_user(self, schema: RegisterSchema, pw_hash: str):
        pass
