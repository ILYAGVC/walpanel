from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

import os
import time

from app.bot.messages.messages import BOT_MESSAGE
from app.bot.keyboards.main_admin_keyboards import main_admin_menu
from app.bot.states.states import DatabaseRestoreState

router = Router()

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
            caption=f"WALPANEL {time.strftime('%Y-%m-%d', time.localtime())}",
        )
    except Exception as e:
        await message.answer(f"Error creating backup: {str(e)}")


@router.message(DatabaseRestoreState.waiting_for_backup_file)
async def restore_database(message: Message, bot_language: str, state: FSMContext):
    try:
        if message.text == "❌ Cancel":
            await state.clear()
            await message.answer(
                BOT_MESSAGE.CANCEL_OPERATION[bot_language],
                reply_markup=main_admin_menu(),
            )
            return

        if not message.document:
            await message.answer(BOT_MESSAGE.NO_FILE[bot_language])
            return

        if not message.document.file_name.endswith(".db"):
            await message.answer(BOT_MESSAGE.INVALID_FILE[bot_language])
            return

        await message.answer(BOT_MESSAGE.RESTORING[bot_language])

        # Download the backup file
        download_file = await message.bot.download(message.document)

        with open(TEMP_DB_PATH, "wb") as new_db:
            new_db.write(download_file.getvalue())

        try:
            if os.path.exists(DB_PATH):
                os.remove(DB_PATH)

            os.replace(TEMP_DB_PATH, DB_PATH)

            # Restart container manually :D
            await message.answer(
                BOT_MESSAGE.RESTORE_SUCCESS[bot_language],
                reply_markup=main_admin_menu(),
            )
            os._exit(1)

        except Exception as e:
            if os.path.exists(TEMP_DB_PATH):
                os.remove(TEMP_DB_PATH)
            raise e

    except Exception as e:
        await message.answer(
            BOT_MESSAGE.ERROR[bot_language].format(e=str(e)),
            reply_markup=main_admin_menu(),
        )
        if os.path.exists(TEMP_DB_PATH):
            os.remove(TEMP_DB_PATH)
    finally:
        await state.clear()
