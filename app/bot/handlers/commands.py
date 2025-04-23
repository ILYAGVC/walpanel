from telebot.types import Message
from app.bot.messages.messages import BOT_MESSAGE
from app.bot.keyboards.main_admin_keyboards import main_menu
from app.bot.config import MAIN_ADMIN


def register(bot):
    @bot.message_handler(commands=["start"])
    async def start(message: Message):
        if message.chat.id == MAIN_ADMIN:
            await bot.send_message(
                message.chat.id, BOT_MESSAGE.START_MAIN_ADMIN, reply_markup=main_menu()
            )
