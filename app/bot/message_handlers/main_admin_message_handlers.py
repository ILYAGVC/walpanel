from telebot.types import Message
from app.bot.keyboards.main_admin_keyboards import main_menu, settings_menu

from app.bot.db.query import admins_query, panels_query
from app.bot.config import MAIN_ADMIN
from app.bot.oprations.backup import get_bckup_from_bot


def message_handlers(bot):
    @bot.message_handler(func=lambda message: True)
    async def message_handler(message: Message):
        chat_id = message.chat.id

        if message.text == "🔙 Back" and chat_id == MAIN_ADMIN:
            await bot.send_message(
                chat_id, "This is Main menu...", reply_markup=main_menu()
            )

        if message.text == "⚙️ Settings" and chat_id == MAIN_ADMIN:
            await bot.send_message(
                chat_id, "This is Settings menu...", reply_markup=settings_menu()
            )

        if message.text == "👤 Admins" and chat_id == MAIN_ADMIN:
            admins = await admins_query.get_all_admins()

            if admins == "no admins found!":
                await bot.send_message(chat_id, admins, reply_markup=main_menu())
                return

            message_text = "Admins / Dealerships\n\n"
            for admin in admins:
                admin_status = "✅" if admin["is_active"] else "❌"

                message_text += (
                    f"<pre>👤 username: {admin['username']}</pre>\n"
                    f"⌛ days remaining: {admin['days_remaining']} Days\n"
                    f"📊 traffic: {admin['traffic']} GB\n"
                    f"💻 status: {admin_status}\n"
                    f"\n"
                )
            await bot.send_message(
                chat_id, message_text, parse_mode="HTML", reply_markup=main_menu()
            )

        if message.text == "🌐 Panels" and chat_id == MAIN_ADMIN:
            panels = await panels_query.get_all_panels()

            if panels == "no panels found!":
                await bot.send_message(chat_id, panels, reply_markup=main_menu())
                return

            message_text = "Panels\n\n"
            for panel in panels:

                message_text += (
                    f"<pre>👤 Panle name: {panel['name']}</pre>\n"
                    f"<pre>🌐 url:\n{panel['url']}</pre>\n"
                    f"<pre>💻 sub:\n{panel['sub']}</pre>\n"
                    f"\n\n"
                )
            await bot.send_message(
                chat_id, message_text, parse_mode="HTML", reply_markup=main_menu()
            )

        if message.text == "🗂 Backup" and chat_id == MAIN_ADMIN:
            await get_bckup_from_bot(bot, message)
