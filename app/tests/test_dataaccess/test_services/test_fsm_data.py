import asyncio

from app.dataaccess.services.fsm_data import FSMDataService
from app.dataaccess.utils.unitofwork import SqlAlchemyUnitOfWork


async def main():
    uof = SqlAlchemyUnitOfWork()
    await FSMDataService().set_state(uof, 1, 1, 1, 'test')


if __name__ == '__main__':
    asyncio.run(main())
