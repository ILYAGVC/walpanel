import os
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.bot.version import __version__


class _MessageSetings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "..", "..", ".env"),
        case_sensitive=True,
        extra="ignore",
    )

    START_MAIN_ADMIN: str = (
        "The bot is not complete yet❕\n"
        "━━━━━━━━━━━━━━━━━\n"
        f"🐋 version: {__version__}\n"
        "👨‍💻 devlop by: @primez_dev\n"
        f"🏢 Sponsor: @pingihostbot"
    )


BOT_MESSAGE = _MessageSetings()
