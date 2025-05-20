import os
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.oprations import admin
from app.version import __version__


class _MessageSetings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "..", "..", ".env"),
        case_sensitive=True,
        extra="ignore",
    )

    START_MAIN_ADMIN: dict = {
        "en": (
            "Welcome!\n"
            "━━━━━━━━━━━━━━━━━\n"
            f"🐋 version: {__version__}\n"
            "👨‍💻 devlop by: @primez_dev\n"
            "🏢 Sponsor: @pingihostbot"
        ),
        "fa": (
            "خوش آمدید!\n"
            "━━━━━━━━━━━━━━━━━\n"
            f"🐋 version: {__version__}\n"
            "👨‍💻 devlop by: @primez_dev\n"
            "🏢 Sponsor: @pingihostbot"
        ),
    }
    DEALERS_STATUS: dict = {
        "en": (
            "<pre>👤 Username: {username}</pre>\n"
            "⌛ Days remaining: {days_remaining} D\n"
            "📊 Traffic: {traffic} GB\n"
            "💻 Panel in use: {panel}\n"
            "ℹ️ Status: {status}\n"
            "➖➖➖➖➖➖➖➖➖➖\n"
        ),
        "fa": (
            "<pre>👤 نام کاربری: {username}</pre>\n"
            "⌛ روزهای باقی‌مانده: {days_remaining} روز\n"
            "📊 ترافیک: {traffic} گیگابایت\n"
            "💻 پنل درحال استفاده: {panel}\n"
            "ℹ️ وضعیت: {status}\n"
            "➖➖➖➖➖➖➖➖➖➖\n"
        ),
    }
    PANELS_STATUS: dict = {
        "en": (
            "<pre>🌐 Panel name: {name}</pre>\n"
            "⚙️ <b>CPU Usage:</b> {cpu_usage}%\n"
            "💾 <b>Memory Usage:</b> {ram_usage}%\n"
            "🛡️ <b>Xray Status:</b> {xray_status}\n"
            "📝 <b>Xray Version:</b> {xray_version}\n"
            "⏱️ <b>Uptime:</b> {uptime} hours\n"
            "➖➖➖➖➖➖➖➖➖➖\n"
        ),
        "fa": (
            "<pre>🌐 نام پنل: {name}</pre>\n"
            "⚙️ <b>استفاده پردازنده:</b> %{cpu_usage}\n"
            "💾 <b>استفاده رم:</b> %{ram_usage}\n"
            "🛡️ <b>وضعیت ایکسری:</b> {xray_status}\n"
            "📝 <b>نسخه ایکسری:</b> {xray_version}\n"
            "⏱️ <b>مدت روشن بودن:</b> {uptime} ساعت\n"
            "➖➖➖➖➖➖➖➖➖➖\n"
        ),
    }
    LOG_MESSAGE: dict = {
        "en": ("📝 Last 10 log entries:"),
        "fa": ("📝 10 لاگ اخر:"),
    }
    BACKING_UP: dict = {
        "en": ("Backing up database..."),
        "fa": ("پشتیبان گیری از دیتابیس..."),
    }


BOT_MESSAGE = _MessageSetings()
