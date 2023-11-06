import logging

import asyncio

from aiogram import Bot, Dispatcher

from app.config import settings
from app.dataaccess.utils.unitofwork import SqlAlchemyUnitOfWork
from app.telegram_bot.quizes.routes import router as router_quiz
from app.telegram_bot.main_menu.routes import router as router_main
from app.telegram_bot.storages.postgresql import PGStorage


# from app.telegram_bot.entrance_exams.roblox.routes import router as roblox_exams


async def tg_app(uow):
    bot = Bot(token=settings.TG_API_TOKEN)
    # uow = SqlAlchemyUnitOfWork()
    storage = PGStorage(uow)

    dp = Dispatcher(storage=storage)

    # dp.include_router(roblox_exams)
    dp.include_router(router_main)
    dp.include_router(router_quiz)

    await dp.start_polling(bot, uow=uow)


async def main():
    uow = SqlAlchemyUnitOfWork()
    task1 = asyncio.create_task(tg_app(uow))
    await task1


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
