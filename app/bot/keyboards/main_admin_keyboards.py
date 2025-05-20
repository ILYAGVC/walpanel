from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


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
                KeyboardButton(text="🔒 Sales Plan"),
                KeyboardButton(text="🔒 Notifications"),
            ],
            [
                KeyboardButton(text="🔒 Help text"),
                KeyboardButton(text="🔒 Registration text"),
            ],
            [KeyboardButton(text="📦 Backup"), KeyboardButton(text="🌎 Language")],
            [KeyboardButton(text="🔙 Back")],
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
