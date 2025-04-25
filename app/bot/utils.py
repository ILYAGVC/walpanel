import os
import time

DB_PATH = "data/walpanel.db"
TEMP_DB_PATH = "data/new.db"


async def get_bckup_from_bot(bot, message):
    with open(DB_PATH, "rb") as db_file:
        await bot.send_message(message.chat.id, "Backing up database...")
        time.sleep(2)

        await bot.send_document(
            message.chat.id,
            db_file,
            caption=f"🐋 WALPANEL (free edition!)\n\n{time.strftime('%Y-%m-%d  --  %H:%M', time.localtime())}",
        )
