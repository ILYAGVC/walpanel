from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from app.bot.config import PANEL_ADDRESS
from app.bot.messages.messages import BOT_MESSAGE


def start_menu(bot_language: str):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BOT_MESSAGE.BUTTON_SIGN_UP[bot_language]),
                KeyboardButton(text=BOT_MESSAGE.BUTTON_LOGIN[bot_language]),
            ],
            [
                KeyboardButton(text=BOT_MESSAGE.BUTTON_HELP[bot_language]),
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
                    text=BOT_MESSAGE.BUTTON_ACCEPT[bot_language],
                    callback_data=f"accept_rules:{chat_id}:{full_name}:{username}:{bot_language}",
                ),
                InlineKeyboardButton(
                    text=BOT_MESSAGE.BUTTON_DECLINE[bot_language],
                    callback_data=f"decline_rules:{chat_id}:{full_name}:{username}:{bot_language}",
                ),
            ],
        ],
    )
    return keyboard


def admin_menu(bot_language: str):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BOT_MESSAGE.BUTTON_MY_ACCOUNT[bot_language]),
            ],
            [
                KeyboardButton(text=BOT_MESSAGE.BUTTON_STORE[bot_language]),
                KeyboardButton(text=BOT_MESSAGE.BUTTON_HELP[bot_language]),
            ],
            [
                KeyboardButton(text=BOT_MESSAGE.BUTTON_LOGOUT[bot_language]),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard


def admin_panel(bot_language: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BOT_MESSAGE.BUTTON_OPEN_PANEL[bot_language],
                    url=f"{PANEL_ADDRESS}",
                ),
            ],
        ],
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


def cancel_payment_keyboard(bot_language: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BOT_MESSAGE.BUTTON_CANCEL[bot_language],
                    callback_data=f"cancel_payment:{bot_language}",
                )
            ]
        ]
    )
    return keyboard
