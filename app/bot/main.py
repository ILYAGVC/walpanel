import asyncio

from telebot.async_telebot import AsyncTeleBot

from app.bot.handlers import register_all_handlers
from app.bot.message_handlers import register_all_message_handlers
from app.bot.config import TOKEN


bot = AsyncTeleBot(TOKEN)

register_all_handlers(bot)
register_all_message_handlers(bot)


async def run():
    await bot.infinity_polling()


if __name__ == "__main__":
    asyncio.run(run())
