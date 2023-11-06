from typing import Optional

from app.dataaccess.models import Users
from app.dataaccess.utils.unitofwork import IUnitOfWork


class UserService:
    @classmethod
    async def get_by_id(cls, uow: IUnitOfWork, user_id) -> Optional[Users]:
        async with uow:
            return await uow.users.find_one(id=user_id)

    @classmethod
    async def create(cls, uow: IUnitOfWork,
                     user_id, user_name) -> Optional[Users]:
        async with uow:
            return await uow.users.add_one(user_id=user_id, name=user_name)
