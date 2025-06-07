from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage

from app.bot.middlewares.middleware import Middleware
from app.bot.config import TOKEN
from app.bot.handlers.commands import router as start_router
from app.bot.handlers.keyboard_handler import router as keyboard_router
from app.bot.handlers.main_admin_callback_handler import (
    router as main_admin_callback_router,
)
from app.bot.handlers.callback_handler import router as callback_handler_router
from app.bot.oprations.change_messages import router as change_messages_router
from app.bot.oprations.plan_setting import router as plan_setting_router
from app.bot.oprations.auth import router as auth_router
from app.bot.handlers.payment.card_payment import router as payment_router
from app.bot.oprations.backup_restore import router as backup_restore_router
from app.bot.handlers.payment.Intermediary_gateway import (
    router as intermediary_gateway_router,
)
import asyncio

bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def run():

    try:
        dp.include_router(start_router)
        dp.include_router(keyboard_router)
        dp.include_router(main_admin_callback_router)
        dp.include_router(callback_handler_router)
        dp.include_router(change_messages_router)
        dp.include_router(plan_setting_router)
        dp.include_router(auth_router)
        dp.include_router(payment_router)
        dp.include_router(backup_restore_router)
        dp.include_router(intermediary_gateway_router)
        dp.message.middleware(Middleware())
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(run())
