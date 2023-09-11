import logging

import asyncio
from aiogram import Bot, Dispatcher

from app.config import settings
from app.quizes.router import router as router_quiz
from app.entrance_exams.roblox.routes import router as roblox_exams


async def main():
    bot = Bot(token=settings.TG_API_TOKEN)
    dp = Dispatcher()

    dp.include_router(roblox_exams)
    dp.include_router(router_quiz)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
