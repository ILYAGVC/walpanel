from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from app.bot.keyboards.main_admin_keyboards import (
    notif_setting_menu,
    settings_menu,
    cancel_keyboard,
)
from app.bot.services.query import (
    bot_settings_query,
    settings_query,
    card_query,
    payment_gateway_query,
)
from app.bot.oprations.notif_settings import get_current_notif_settings
from app.bot.messages.messages import BOT_MESSAGE
from app.bot.states.states import RegisterUserStates, SettingsState
from app.bot.keyboards.main_admin_keyboards import (
    card_method_settings_keyboard,
    intermediary_method_settings_keyboard,
)

router = Router()


@router.callback_query(F.data.startswith("change_start_notif_status:"))
async def handle_start_notif_status(callback: types.CallbackQuery):
    _, bot_language, user_role = callback.data.split(":")

    if user_role != "main_admin":
        await callback.answer(
            BOT_MESSAGE.ERROR[bot_language].format(
                e="Access denied" if bot_language == "en" else "دسترسی رد شد"
            ),
            show_alert=True,
        )
        return

    current_status = bot_settings_query.get_start_notif()
    new_status = not current_status

    if bot_settings_query.change_start_notif(new_status):
        text_message = await get_current_notif_settings(bot_language)
        await callback.message.edit_text(
            text_message,
            parse_mode="HTML",
            reply_markup=notif_setting_menu(bot_language, user_role),
        )
    else:
        await callback.message.edit_text(
            BOT_MESSAGE.ERROR[bot_language].format(
                e=(
                    "Failed to change notification status"
                    if bot_language == "en"
                    else "تغییر وضعیت اعلان ناموفق بود"
                )
            ),
            reply_markup=settings_menu(bot_language),
        )
    await callback.answer()


@router.callback_query(F.data.startswith("change_create_notif_status:"))
async def handle_create_notif_status(callback: types.CallbackQuery):
    _, bot_language, user_role = callback.data.split(":")

    if user_role != "main_admin":
        await callback.answer(
            BOT_MESSAGE.ERROR[bot_language].format(
                e="Access denied" if bot_language == "en" else "دسترسی رد شد"
            ),
            show_alert=True,
        )
        return

    current_status = bot_settings_query.get_create_notif()
    new_status = not current_status

    if bot_settings_query.change_create_notif(new_status):
        text_message = await get_current_notif_settings(bot_language)
        await callback.message.edit_text(
            text_message,
            parse_mode="HTML",
            reply_markup=notif_setting_menu(bot_language, user_role),
        )
    else:
        await callback.message.edit_text(
            BOT_MESSAGE.ERROR[bot_language].format(
                e=(
                    "Failed to change notification status"
                    if bot_language == "en"
                    else "تغییر وضعیت اعلان ناموفق بود"
                )
            ),
            reply_markup=settings_menu(bot_language),
        )
    await callback.answer()


@router.callback_query(F.data.startswith("change_delete_notif_status:"))
async def handle_delete_notif_status(callback: types.CallbackQuery):
    _, bot_language, user_role = callback.data.split(":")

    if user_role != "main_admin":
        await callback.answer(
            BOT_MESSAGE.ERROR[bot_language].format(
                e="Access denied" if bot_language == "en" else "دسترسی رد شد"
            ),
            show_alert=True,
        )
        return

    current_status = bot_settings_query.get_delete_notif()
    new_status = not current_status

    if bot_settings_query.change_delete_notif(new_status):
        text_message = await get_current_notif_settings(bot_language)
        await callback.message.edit_text(
            text_message,
            parse_mode="HTML",
            reply_markup=notif_setting_menu(bot_language, user_role),
        )
    else:
        await callback.message.edit_text(
            BOT_MESSAGE.ERROR[bot_language].format(
                e=(
                    "Failed to change notification status"
                    if bot_language == "en"
                    else "تغییر وضعیت اعلان ناموفق بود"
                )
            ),
            reply_markup=settings_menu(bot_language),
        )
    await callback.answer()


@router.callback_query(F.data.startswith("confirm_registration:"))
async def handle_confirm_registration(callback: types.CallbackQuery, state: FSMContext):
    _, chat_id, bot_language = callback.data.split(":")

    await callback.message.delete()

    await callback.message.answer(
        BOT_MESSAGE.CHOOSE_A_USERNAME_FOR_THE_REQUESTER[bot_language],
        reply_markup=cancel_keyboard(bot_language),
    )

    await state.update_data(requested_user_id=chat_id, bot_language=bot_language)
    await state.set_state(RegisterUserStates.enter_username)


@router.callback_query(F.data.startswith("change_card_method_status:"))
async def handle_change_card_method_status(callback: types.CallbackQuery):
    try:
        _, bot_language = callback.data.split(":")
        await settings_query.change_card_method_status()

        status = await settings_query.get_card_method()
        card_num = card_query.get_card()
        status_text = "✅" if status else "❌"

        await callback.message.edit_text(
            BOT_MESSAGE.CARD_METHOD_SETTINGS[bot_language].format(
                status=status_text, card_num=card_num
            ),
            parse_mode="HTML",
            reply_markup=card_method_settings_keyboard(bot_language),
        )
    except Exception as e:
        await callback.answer(
            BOT_MESSAGE.ERROR[bot_language].format(e=e), show_alert=True
        )


@router.callback_query(F.data.startswith("change_card_number:"))
async def handle_change_card_number(callback: types.CallbackQuery, state: FSMContext):
    try:
        _, bot_language = callback.data.split(":")
        await state.update_data(bot_language=bot_language)
        await state.set_state(SettingsState.waiting_for_card_number)
        await callback.message.edit_text(
            BOT_MESSAGE.ENTER_NEW_CARD_NUMBER[bot_language], parse_mode="HTML"
        )
    except Exception as e:
        await callback.answer(
            BOT_MESSAGE.ERROR[bot_language].format(e=e), show_alert=True
        )


@router.callback_query(F.data.startswith("change_intermediary_method_status:"))
async def handle_change_intermediary_method_status(callback: types.CallbackQuery):
    try:
        _, bot_language = callback.data.split(":")
        await settings_query.change_intermediary_gateway_status()
        status = await settings_query.get_intermediary_gateway()
        api_key = payment_gateway_query.get_intermediary_gateway_key()
        status_text = "✅" if status else "❌"

        await callback.message.edit_text(
            BOT_MESSAGE.INTERMEDIARY_METHOD_SETTINGS[bot_language].format(
                status=status_text, api_key=api_key
            ),
            parse_mode="HTML",
            reply_markup=intermediary_method_settings_keyboard(bot_language),
        )
    except Exception as e:
        await callback.answer(
            BOT_MESSAGE.ERROR[bot_language].format(e=e), show_alert=True
        )


@router.callback_query(F.data.startswith("change_intermediary_method_api_key:"))
async def handle_change_intermediary_method_key(
    callback: types.CallbackQuery, state: FSMContext
):
    try:
        _, bot_language = callback.data.split(":")
        await state.update_data(bot_language=bot_language)
        await state.set_state(SettingsState.waiting_api_key)
        await callback.message.edit_text(
            BOT_MESSAGE.ENTER_NEW_API_KEY[bot_language], parse_mode="HTML"
        )
    except Exception as e:
        await callback.answer(
            BOT_MESSAGE.ERROR[bot_language].format(e=e), show_alert=True
        )


@router.callback_query(F.data.startswith("intermediary_method_help:"))
async def handle_intermediary_method_help(callback: types.CallbackQuery):
    _, bot_language = callback.data.split(":")
    await callback.message.answer(
        BOT_MESSAGE.HELP_INTERMEDIARY_METHOD[bot_language],
        parse_mode="HTML",
    )


@router.message(SettingsState.waiting_for_card_number)
async def handle_new_card_number(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        bot_language = data.get("bot_language")
        new_card_number = message.text.strip()

        card_query.add_card(new_card_number)
        await state.clear()

        status = await settings_query.get_card_method()
        status_text = "✅" if status else "❌"

        await message.answer(
            BOT_MESSAGE.CARD_NUMBER_UPDATED[bot_language],
            parse_mode="HTML",
            reply_markup=card_method_settings_keyboard(bot_language),
        )

        # Show updated settings
        await message.answer(
            BOT_MESSAGE.CARD_METHOD_SETTINGS[bot_language].format(
                status=status_text, card_num=new_card_number
            ),
            parse_mode="HTML",
        )
    except Exception as e:
        await message.answer(
            BOT_MESSAGE.ERROR[bot_language].format(e=e), parse_mode="HTML"
        )
        await state.clear()


@router.message(SettingsState.waiting_api_key)
async def handle_new_api_key(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        bot_language = data.get("bot_language")
        new_api_key = message.text.strip()

        await payment_gateway_query.change_intermediary_gateway_key(new_api_key)
        await state.clear()

        status = await settings_query.get_intermediary_gateway()
        status_text = "✅" if status else "❌"

        await message.answer(
            BOT_MESSAGE.APIKEY_UPDATED[bot_language],
            parse_mode="HTML",
        )
    except Exception as e:
        await message.answer(
            BOT_MESSAGE.ERROR[bot_language].format(e=e), parse_mode="HTML"
        )
        await state.clear()
