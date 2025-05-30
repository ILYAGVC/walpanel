from aiogram import types
from aiogram.fsm.context import FSMContext
from app.bot.messages.messages import BOT_MESSAGE
from app.bot.keyboards.main_admin_keyboards import notif_setting_menu
from app.bot.services.query import bot_settings_query


async def get_current_notif_settings(bot_language: str):
    """Get current notif settings"""
    start_notif = bot_settings_query.get_start_notif()
    create_notif = bot_settings_query.get_create_notif()
    delete_notif = bot_settings_query.get_delete_notif()

    start_notif_status = "🔔" if start_notif else "🔕"
    create_notif_status = "🔔" if create_notif else "🔕"
    delete_notif_status = "🔔" if delete_notif else "🔕"
    text_message = BOT_MESSAGE.NOTIF_STATUS[bot_language].format(
        start_status=start_notif_status,
        create_status=create_notif_status,
        delete_status=delete_notif_status,
    )
    return text_message


async def show_notif_settings(
    message: types.Message, bot_language: str, user_role: str
):
    """Show notif settings"""
    text_message = await get_current_notif_settings(bot_language)
    await message.answer(
        text_message,
        parse_mode="HTML",
        reply_markup=notif_setting_menu(bot_language, user_role),
    )
