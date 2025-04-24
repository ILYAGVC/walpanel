from telebot.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


# main admin menu
def main_menu():
    reply_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=False, row_width=2
    )
    reply_keyboard.add("👤 Admins", "🌐 Panels", "⚙️ Settings")
    return reply_keyboard


# setting menu
def settings_menu():
    reply_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=False, row_width=2
    )
    reply_keyboard.add(
        "🔒 Prices",
        "🔒 Notifications",
        "🔒 Help text",
        "🔒 Registration text",
        "🗂 Backup",
        "🔙 Back",
    )
    return reply_keyboard
