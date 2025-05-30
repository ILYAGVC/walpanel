from aiogram import filters, types, Router
from aiogram.filters import Command


from app.bot.messages.messages import BOT_MESSAGE
from app.bot.keyboards.main_admin_keyboards import main_admin_menu
from app.bot.keyboards.keyboards import start_menu, admin_menu
from app.bot.config import MAIN_ADMIN
from app.bot.services.query import bot_settings_query, admins_query

router = Router()


@router.message(Command("start"))
async def command_start_handler(
    message: types.Message, bot_language: str, user_role: str
):
    if user_role == "main_admin":
        await message.answer(
            BOT_MESSAGE.START_MAIN_ADMIN[bot_language], reply_markup=main_admin_menu()
        )
    else:
        if bot_settings_query.get_start_notif():
            notif = BOT_MESSAGE.START_NOTIF[bot_language].format(
                name=message.from_user.full_name,
                user_id=message.from_user.username or message.from_user.id,
                chat_id=message.chat.id,
            )
            await message.bot.send_message(MAIN_ADMIN, notif, parse_mode="HTML")
        if not admins_query.check_loged_in(message.chat.id):
            await message.answer(
                BOT_MESSAGE.START_MESSAGE[bot_language], reply_markup=start_menu()
            )
        else:
            await message.answer(
                BOT_MESSAGE.START_DEALER[bot_language], reply_markup=admin_menu()
            )
