from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from app.bot.messages.messages import BOT_MESSAGE
from app.bot.states.states import HelpTextStates, RegistrationTextStates
from app.bot.keyboards.main_admin_keyboards import settings_menu, cancel_keyboard
from app.bot.services.query import help_message_query, registering_message_query

router = Router()


@router.message(HelpTextStates.waiting_for_new_help_text)
async def change_help_text(
    message: types.Message, state: FSMContext, bot_language: str
):
    if message.text in [
        BOT_MESSAGE.BUTTON_CANCEL["en"],
        BOT_MESSAGE.BUTTON_CANCEL["fa"],
    ]:
        await state.clear()
        await message.answer(
            BOT_MESSAGE.CANCEL_OPERATION[bot_language],
            reply_markup=settings_menu(bot_language),
        )
    else:
        if help_message_query.change_help_message(message.text):
            await message.answer(
                BOT_MESSAGE.HELP_TEXT_CHANGED[bot_language],
                reply_markup=settings_menu(bot_language),
            )
        else:
            await message.answer(
                BOT_MESSAGE.ERROR[bot_language],
                reply_markup=settings_menu(bot_language),
            )
        await state.clear()


@router.message(RegistrationTextStates.waiting_for_new_registration_text)
async def change_registration_text(
    message: types.Message, state: FSMContext, bot_language: str
):
    if message.text in [
        BOT_MESSAGE.BUTTON_CANCEL["en"],
        BOT_MESSAGE.BUTTON_CANCEL["fa"],
    ]:
        await state.clear()
        await message.answer(
            BOT_MESSAGE.CANCEL_OPERATION[bot_language],
            reply_markup=settings_menu(bot_language),
        )
    else:
        if registering_message_query.chage_registering_message(message.text):
            await message.answer(
                BOT_MESSAGE.REGISTRATION_TEXT_CHANGED[bot_language],
                reply_markup=settings_menu(bot_language),
            )
        else:
            await message.answer(
                BOT_MESSAGE.ERROR[bot_language],
                reply_markup=settings_menu(bot_language),
            )
        await state.clear()
