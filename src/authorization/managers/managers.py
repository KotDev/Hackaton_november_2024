from sqlalchemy import select, ScalarResult

from authorization.schemas import RegisterSchema
from .managers_interfaces import UserManagerInterface
from authorization.models.model import User
from database import DataBase

class UserManager(UserManagerInterface, DataBase):
    def __init__(self) -> None:
        super().__init__()

    async def get_user(self, user_id: int | None, **kwargs):
        return await self.get_obj(user_id, User, **kwargs)

    async def add_user(self, schema: RegisterSchema, pw_hash: str) -> User:
        async with self.async_session() as session:
            user: User = User(email=schema.email, password=pw_hash, role=schema.role)
            session.add(user)
            await session.commit()
            return user

    async def delete_user(self, user_id: int | None, **kwargs) -> None:
        return await self.delete_obj(user_id, User, **kwargs)

    async def update_user(self, user_id: int | None, new_data: dict | None = None, **kwargs) -> ScalarResult[User]:
        return await self.update_obj(user_id, new_data, **kwargs)



