from aiogram import filters, types, Router
from aiogram.filters import Command


from app.bot.messages.messages import BOT_MESSAGE

from app.bot.keyboards.main_admin_keyboards import main_admin_menu
from app.bot.config import MAIN_ADMIN

router = Router()


@router.message(Command("start"))
async def command_start_handler(
    message: types.Message, bot_language: str, user_role: str
):
    if user_role == "main_admin":
        await message.answer(
            BOT_MESSAGE.START_MAIN_ADMIN[bot_language], reply_markup=main_admin_menu()
        )
