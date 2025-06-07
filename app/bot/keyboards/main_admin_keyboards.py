from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from app.bot.messages.messages import BOT_MESSAGE


def main_admin_menu(bot_language: str):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BOT_MESSAGE.BUTTON_ADMINS[bot_language]),
                KeyboardButton(text=BOT_MESSAGE.BUTTON_PANELS[bot_language]),
            ],
            [KeyboardButton(text=BOT_MESSAGE.BUTTON_SETTINGS[bot_language])],
            [KeyboardButton(text=BOT_MESSAGE.BUTTON_LOGS[bot_language])],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard


def settings_menu(bot_language: str):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BOT_MESSAGE.BUTTON_SALES_PLAN[bot_language]),
                KeyboardButton(text=BOT_MESSAGE.BUTTON_NOTIFICATIONS[bot_language]),
            ],
            [
                KeyboardButton(text=BOT_MESSAGE.BUTTON_HELP_TEXT[bot_language]),
                KeyboardButton(text=BOT_MESSAGE.BUTTON_REGISTRATION_TEXT[bot_language]),
            ],
            [
                KeyboardButton(text=BOT_MESSAGE.BUTTON_DATABASE[bot_language]),
                KeyboardButton(text=BOT_MESSAGE.BUTTON_LANGUAGE[bot_language]),
            ],
            [KeyboardButton(text=BOT_MESSAGE.BUTTON_BACK[bot_language])],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard


def database_menu(bot_language: str):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BOT_MESSAGE.BUTTON_BACKUP[bot_language]),
                KeyboardButton(text=BOT_MESSAGE.BUTTON_RESTORE[bot_language]),
            ],
            [KeyboardButton(text=BOT_MESSAGE.BUTTON_BACK_TO_SETTINGS[bot_language])],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard


def sales_plan_menu(bot_language: str):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BOT_MESSAGE.BUTTON_ADD_PLAN[bot_language])],
            [
                KeyboardButton(text=BOT_MESSAGE.BUTTON_DELETE_PLAN[bot_language]),
                KeyboardButton(text=BOT_MESSAGE.BUTTON_EDIT_PLAN[bot_language]),
            ],
            [KeyboardButton(text=BOT_MESSAGE.BUTTON_CARD_METHOD[bot_language])],
            [KeyboardButton(text=BOT_MESSAGE.BUTTON_INTERMEDIARY_METHOD[bot_language])],
            [KeyboardButton(text=BOT_MESSAGE.BUTTON_BACK_TO_SETTINGS[bot_language])],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard


def language_menu(bot_language: str):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BOT_MESSAGE.BUTTON_ENGLISH[bot_language]),
                KeyboardButton(text=BOT_MESSAGE.BUTTON_PERSIAN[bot_language]),
            ],
            [KeyboardButton(text=BOT_MESSAGE.BUTTON_BACK[bot_language])],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard


def cancel_keyboard(bot_language: str):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BOT_MESSAGE.BUTTON_CANCEL[bot_language])],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard


def confirmation_keyboard(bot_language: str):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BOT_MESSAGE.BUTTON_YES[bot_language])],
            [KeyboardButton(text=BOT_MESSAGE.BUTTON_NO[bot_language])],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard


def registration_confirmation_menu(chat_id: int, bot_language: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BOT_MESSAGE.BUTTON_CONFIRM[bot_language],
                    callback_data=f"confirm_registration:{chat_id}:{bot_language}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=BOT_MESSAGE.BUTTON_REJECT[bot_language],
                    callback_data=f"cancel_registration:{chat_id}:{bot_language}",
                )
            ],
        ]
    )
    return keyboard


def notif_setting_menu(bot_language: str, user_role: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄️ Start the bot",
                    callback_data=f"change_start_notif_status:{bot_language}:{user_role}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄️ Create client",
                    callback_data=f"change_create_notif_status:{bot_language}:{user_role}",
                ),
                InlineKeyboardButton(
                    text="🔄️ Delete client",
                    callback_data=f"change_delete_notif_status:{bot_language}:{user_role}",
                ),
            ],
        ]
    )
    return keyboard


def card_method_settings_keyboard(bot_language: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BOT_MESSAGE.CHANGE_CARD_METHOD_STATUS[bot_language],
                    callback_data=f"change_card_method_status:{bot_language}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=BOT_MESSAGE.CHANGE_CARD_NUMBER[bot_language],
                    callback_data=f"change_card_number:{bot_language}",
                )
            ],
        ]
    )
    return keyboard


def intermediary_method_settings_keyboard(bot_language: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BOT_MESSAGE.CHANGE_INTERMEDIARY_METHOD_STATUS[bot_language],
                    callback_data=f"change_intermediary_method_status:{bot_language}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=BOT_MESSAGE.CHANGE_INTERMEDIARY_METHOD_API_KEY[bot_language],
                    callback_data=f"change_intermediary_method_api_key:{bot_language}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=BOT_MESSAGE.BUTTON_INTERMEDIARY_METHOD_HELP[bot_language],
                    callback_data=f"intermediary_method_help:{bot_language}",
                )
            ],
        ]
    )
    return keyboard
