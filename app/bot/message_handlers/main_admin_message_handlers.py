from telebot.types import Message
from app.bot.keyboards.main_admin_keyboards import main_menu, settings_menu
from app.bot.config import MAIN_ADMIN


def message_handlers(bot):
    @bot.message_handler(func=lambda message: True)
    async def message_handler(message: Message):
        chat_id = message.chat.id

        if message.text == "🔙 Back" and chat_id == MAIN_ADMIN:
            await bot.send_message(
                chat_id, "This is Main menu...", reply_markup=main_menu()
            )

        if message.text == "⚙️ Settings" and chat_id == MAIN_ADMIN:
            await bot.send_message(
                chat_id, "This is Settings menu...", reply_markup=settings_menu()
            )
