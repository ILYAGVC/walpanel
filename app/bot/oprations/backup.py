from aiogram.types import Message, FSInputFile
from app.bot.messages.messages import BOT_MESSAGE
import os
import time


current_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
DB_PATH = os.path.join(current_dir, "data", "walpanel.db")
TEMP_DB_PATH = os.path.join(current_dir, "data", "new.db")


async def get_backup_from_bot(message: Message, bot_language: str):
    try:
        if not os.path.exists(DB_PATH):
            await message.answer(f"Database file not found at: {DB_PATH}")
            return

        await message.answer(BOT_MESSAGE.BACKING_UP[bot_language])
        time.sleep(2)

        input_file = FSInputFile(DB_PATH)
        await message.answer_document(
            document=input_file,
            caption=f"WALPANEL\n\n{time.strftime('%Y-%m-%d', time.localtime())}",
        )
    except Exception as e:
        await message.answer(f"Error creating backup: {str(e)}")
