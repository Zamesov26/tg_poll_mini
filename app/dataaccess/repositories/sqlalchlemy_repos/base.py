from abc import abstractmethod

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.dataaccess.database import Base
from app.dataaccess.repositories.abstract_repos import IRepository


class ISQLAlchemyRepo(IRepository):
    @abstractmethod
    async def model(self, *args, **kwargs) -> type[Base]:
        pass

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, **data):
        item = self.model(**data)
        return item
        # self.session.add(item)

    async def find_one(self, **filters):
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

    async def find_all(self, **filters):
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def edit_one(self, id_, **values):
        stmt = update(self.model).where(self.model.id == id_).values(**values)
        await self.session.execute(stmt)

    async def delete_one(self, id_):
        stmt = delete(self.model).filter_by(self.model.id == id_)
        await self.session.execute(stmt)

    async def delete_all(self, **filters):
        stmt = delete(self.model).filter_by(**filters)
        await self.session.execute(stmt)
