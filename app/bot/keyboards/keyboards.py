from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from app.bot.config import PANEL_ADDRESS
from app.bot.messages.messages import BOT_MESSAGE


def start_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💎 sign up"),
                KeyboardButton(text="🛡️ Login"),
            ],
            [
                KeyboardButton(text="ℹ️ Help"),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard


def sign_up_menu(chat_id: str, full_name: str, username: str, bot_language: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Accept",
                    callback_data=f"accept_rules:{chat_id}:{full_name}:{username}:{bot_language}",
                ),
                InlineKeyboardButton(
                    text="❌ Decline",
                    callback_data=f"decline_rules:{chat_id}:{full_name}:{username}:{bot_language}",
                ),
            ],
        ],
    )
    return keyboard


def admin_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💎 My account"),
            ],
            [
                KeyboardButton(text="🛍️ Store"),
                KeyboardButton(text="ℹ️ Help"),
            ],
            [
                KeyboardButton(text="❌ Logout"),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard


def admin_panel():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛜 Open panel",
                    url=f"{PANEL_ADDRESS}",
                ),
            ],
        ],
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


def cancel_payment_keyboard(bot_language: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BOT_MESSAGE.CANCEL[bot_language],
                    callback_data=f"cancel_payment:{bot_language}",
                )
            ]
        ]
    )
    return keyboard
