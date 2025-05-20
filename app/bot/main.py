from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.types import Message


from app.bot.middlewares.middleware import Middleware
from app.bot.config import TOKEN
from app.bot.handlers.commands import router as start_router
from app.bot.handlers.keyboard_handler import router as keyboard_router
import asyncio

bot = Bot(TOKEN)
dp = Dispatcher()


async def run():

    try:
        dp.include_router(start_router)
        dp.include_router(keyboard_router)
        dp.message.middleware(Middleware())
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(run())
