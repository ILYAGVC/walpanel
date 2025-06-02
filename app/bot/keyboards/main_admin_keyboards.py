from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from app.bot.messages.messages import BOT_MESSAGE


def main_admin_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Admins"), KeyboardButton(text="🌐 Panels")],
            [KeyboardButton(text="⚙️ Settings")],
            [KeyboardButton(text="📝 Logs")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard


def settings_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🛍️ Sales Plan"),
                KeyboardButton(text="🔔 Notifications"),
            ],
            [
                KeyboardButton(text="📄 Help text"),
                KeyboardButton(text="⚪ Registration text"),
            ],
            [KeyboardButton(text="📦 Database"), KeyboardButton(text="🌎 Language")],
            [KeyboardButton(text="🔙 Back")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard


def database_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📥 Backup"), KeyboardButton(text="📤 Restore")],
            [KeyboardButton(text="🔙 Back to settings")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard


def sales_plan_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Add a plan")],
            [
                KeyboardButton(text="❌ Delete a plan"),
                KeyboardButton(text="⚙️ Edit a plan"),
            ],
            [KeyboardButton(text="💳 Card method setting")],
            [KeyboardButton(text="🔙 Back to settings")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard


def language_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇸 English"), KeyboardButton(text="🇮🇷 Persian")],
            [KeyboardButton(text="🔙 Back")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard


def cancel_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Cancel")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard


def confirmation_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Yes")],
            [KeyboardButton(text="❌ No")],
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
                    text="✅ Confirm",
                    callback_data=f"confirm_registration:{chat_id}:{bot_language}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Reject",
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
