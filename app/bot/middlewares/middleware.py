from aiogram import BaseMiddleware
from aiogram.types import Message
from app.bot.services.query import settings_query
from app.bot.config import MAIN_ADMIN


BOT_LANGUAGE = None


class Middleware(BaseMiddleware):
    """Middleware to set the language and handle admin-specific logic"""

    async def __call__(self, handler, event: Message, data):
        global BOT_LANGUAGE

        if BOT_LANGUAGE is None:
            BOT_LANGUAGE = await settings_query.get_language()

        data["bot_language"] = BOT_LANGUAGE

        data["user_role"] = "main_admin" if event.chat.id == MAIN_ADMIN else "user"
        return await handler(event, data)


async def set_new_language():
    """Update the global language setting"""
    global BOT_LANGUAGE
    BOT_LANGUAGE = await settings_query.get_language()
