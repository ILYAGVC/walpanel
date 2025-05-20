from aiogram import Router, types, F
from bot.keyboards.main_admin_keyboards import (
    main_admin_menu,
    settings_menu,
    language_menu,
)
from app.bot.services.query import admins_query, panels_query, settings_query
from app.admin_services.api import panels_api
from app.bot.messages.messages import BOT_MESSAGE
from app.bot.middlewares.middleware import set_new_language
from app.bot.oprations.backup import get_backup_from_bot
import os


router = Router()


@router.message(F.text == "👤 Admins")
async def handle_admins_button(
    message: types.Message, bot_language: str, user_role: str
):
    if user_role == "main_admin":
        admins = await admins_query.get_all_admins()
        if not admins:
            await message.answer("No admins found!")
            return

        message_text = "📊 Dealers/Admins Status\n\n"
        try:
            for admin in admins:
                admin_status = "active" if admin["is_active"] else "disabled"
                message_text += BOT_MESSAGE.DEALERS_STATUS[bot_language].format(
                    username=admin["username"],
                    days_remaining=admin["days_remaining"],
                    traffic=admin["traffic"],
                    panel=admin["panel"],
                    status=admin_status,
                )
            await message.answer(
                message_text, parse_mode="HTML", reply_markup=main_admin_menu()
            )
        except Exception as e:
            await message.answer(f"Error: {e}")


@router.message(F.text == "🌐 Panels")
async def handle_panels_button(
    message: types.Message, bot_language: str, user_role: str
):
    if user_role == "main_admin":
        panels = await panels_query.get_all_panels()
        if not panels:
            await message.answer("No panels found!")
            return

        message_text = "📊 Panel Status Report\n\n"
        try:
            for panel in panels:
                panel_status = await panels_api.server_status(
                    panel["url"], panel["username"], panel["password"]
                )
                status_data = panel_status.get("obj", {})
                xray_status = status_data.get("xray", "unknown")
                used_mem = status_data.get("mem", {}).get("current", 0)
                total_mem = status_data.get("mem", {}).get("total", 1)
                mem_percent = (used_mem / total_mem) * 100
                uptime = status_data.get("uptime", 0) // 3600

                message_text += BOT_MESSAGE.PANELS_STATUS[bot_language].format(
                    name=panel["name"],
                    cpu_usage=int(status_data.get("cpu", 0)),
                    ram_usage=int(mem_percent),
                    xray_status=xray_status.get("state", "unknown"),
                    xray_version=xray_status.get("version", "N/A"),
                    uptime=uptime,
                )

            await message.answer(
                message_text, parse_mode="HTML", reply_markup=main_admin_menu()
            )
        except Exception as e:
            await message.answer(f"Error: {e}")


@router.message(F.text == "🌎 Language")
async def handle_lang_button(message: types.Message, user_role: str):
    if user_role == "main_admin":
        await message.answer("🤖 Bot Language", reply_markup=language_menu())


@router.message(F.text == "🇺🇸 English")
async def handle_en_button(message: types.Message, user_role: str):
    if user_role == "main_admin":
        new_language = "en"
        await settings_query.change_language(new_language)
        await message.answer(
            BOT_MESSAGE.START_MAIN_ADMIN[new_language], reply_markup=main_admin_menu()
        )
        await set_new_language()


@router.message(F.text == "🇮🇷 Persian")
async def handle_fa_button(message: types.Message, user_role: str):
    if user_role == "main_admin":
        new_language = "fa"
        await settings_query.change_language(new_language)
        await message.answer(
            BOT_MESSAGE.START_MAIN_ADMIN[new_language], reply_markup=main_admin_menu()
        )
        await set_new_language()


@router.message(F.text == "🇺🇸 English")
async def handle_en_button(message: types.Message, user_role: str):
    if user_role == "main_admin":

        await message.answer("🇺🇸 English", reply_markup=settings_menu())


@router.message(F.text == "⚙️ Settings")
async def handle_settings_button(message: types.Message, user_role: str):
    if user_role == "main_admin":
        await message.answer("⚙️ Settings Menu", reply_markup=settings_menu())


@router.message(F.text == "🔙 Back")
async def handle_back_button(message: types.Message, user_role: str):
    if user_role == "main_admin":
        await message.answer("📱 Main menu", reply_markup=main_admin_menu())


@router.message(F.text == "📝 Logs")
async def handle_logs_button(message: types.Message, user_role: str, bot_language: str):
    if user_role == "main_admin":
        current_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        log_file_path = os.path.join(current_dir, "data", "app.log")

        try:
            if not os.path.exists(log_file_path):
                await message.answer(f"Log file not found at: {log_file_path}")
                return

            with open(log_file_path, "r", encoding="utf-8") as file:
                # Read all lines and get the last 10
                lines = file.readlines()
                last_10_lines = lines[-10:] if len(lines) >= 10 else lines

                log_content = "".join(last_10_lines)
                await message.answer(
                    f"{BOT_MESSAGE.LOG_MESSAGE[bot_language]}<pre>{log_content}</pre>",
                    parse_mode="HTML",
                    reply_markup=main_admin_menu(),
                )
        except Exception as e:
            await message.answer(f"Error reading log file: {str(e)}")


@router.message(F.text == "📦 Backup")
async def handle_backup_button(
    message: types.Message, user_role: str, bot_language: str
):
    if user_role == "main_admin":
        await get_backup_from_bot(message, bot_language)
