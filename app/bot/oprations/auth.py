from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from app.bot.messages.messages import BOT_MESSAGE
from app.bot.services.query import panels_query
from app.bot.states.states import RegisterUserStates, LoginUserStates
from app.bot.keyboards.main_admin_keyboards import cancel_keyboard, main_admin_menu
from app.bot.keyboards.keyboards import (
    cancel_keyboard as dealer_cancel_keyboard,
    sign_up_menu,
    start_menu,
    admin_menu,
)
from app.bot.services.query import admins_query, panels_query
from app.bot.oprations.captcha import generate_captcha
from datetime import datetime, timedelta

router = Router()

# Global list to store logged in admins
logged_in_admins = []


# Registration confirmation by main admin
@router.message(RegisterUserStates.enter_username)
async def enter_username(message: types.Message, bot_language: str, state: FSMContext):
    try:
        if message.text in [
            BOT_MESSAGE.BUTTON_CANCEL["en"],
            BOT_MESSAGE.BUTTON_CANCEL["fa"],
        ]:
            await message.answer(
                BOT_MESSAGE.CANCEL_OPERATION[bot_language],
                reply_markup=main_admin_menu(bot_language),
            )
            await state.clear()
            return

        username = message.text

        await state.update_data(username=username)
        await message.answer(
            BOT_MESSAGE.CHOOSE_A_PASSWORD_FOR_THE_REQUESTER[bot_language],
            reply_markup=cancel_keyboard(bot_language),
        )
        await state.set_state(RegisterUserStates.enter_password)
    except Exception as e:
        await message.answer(
            BOT_MESSAGE.ERROR[bot_language].format(e=e),
            reply_markup=main_admin_menu(bot_language),
        )


@router.message(RegisterUserStates.enter_password)
async def enter_password(message: types.Message, bot_language: str, state: FSMContext):
    try:
        if message.text in [
            BOT_MESSAGE.BUTTON_CANCEL["en"],
            BOT_MESSAGE.BUTTON_CANCEL["fa"],
        ]:
            await message.answer(
                BOT_MESSAGE.CANCEL_OPERATION[bot_language],
                reply_markup=main_admin_menu(bot_language),
            )
            await state.clear()
            return

        password = message.text

        await state.update_data(password=password)

        panels = await panels_query.get_all_panels()
        show_panels = ""
        if panels:
            for panel in panels:
                show_panels += f"<b>🆔: {panel['id']}  Name: {panel['name']}</b>\n➖➖➖➖➖➖➖➖➖➖\n"

        await message.answer(
            show_panels, parse_mode="HTML", reply_markup=cancel_keyboard(bot_language)
        )
        await message.answer(
            BOT_MESSAGE.CHOOSE_A_PANEL_FOR_THE_REQUESTER[bot_language],
            reply_markup=cancel_keyboard(bot_language),
        )
        await state.set_state(RegisterUserStates.enter_panel_id)
    except Exception as e:
        await message.answer(
            BOT_MESSAGE.ERROR[bot_language].format(e=e),
            reply_markup=main_admin_menu(bot_language),
        )


@router.message(RegisterUserStates.enter_panel_id)
async def enter_panel_id(message: types.Message, bot_language: str, state: FSMContext):
    try:
        if message.text in [
            BOT_MESSAGE.BUTTON_CANCEL["en"],
            BOT_MESSAGE.BUTTON_CANCEL["fa"],
        ]:
            await message.answer(
                BOT_MESSAGE.CANCEL_OPERATION[bot_language],
                reply_markup=main_admin_menu(bot_language),
            )
            await state.clear()
            return

        panel_id = int(message.text)

        if not panels_query.get_panel_by_id(panel_id):
            raise ValueError

        await state.update_data(panel_id=panel_id)
        await message.answer(
            BOT_MESSAGE.CHOOSE_A_INBOUND_FOR_THE_REQUESTER[bot_language],
            reply_markup=cancel_keyboard(bot_language),
        )
        await state.set_state(RegisterUserStates.enter_inbound_id)

    except ValueError:
        await message.answer(
            BOT_MESSAGE.PANEL_NOT_EXIST[bot_language],
            reply_markup=cancel_keyboard(bot_language),
        )


@router.message(RegisterUserStates.enter_inbound_id)
async def enter_inbound_id(
    message: types.Message, bot_language: str, state: FSMContext
):
    try:
        if message.text in [
            BOT_MESSAGE.BUTTON_CANCEL["en"],
            BOT_MESSAGE.BUTTON_CANCEL["fa"],
        ]:
            await message.answer(
                BOT_MESSAGE.CANCEL_OPERATION[bot_language],
                reply_markup=main_admin_menu(bot_language),
            )
            await state.clear()
            return

        inbound_id = int(message.text)
        data = await state.get_data()

        username = data["username"]
        password = data["password"]
        panel_id = data["panel_id"]
        requested_user_id = data["requested_user_id"]

        # Create admin with proper date format
        expiry_time = datetime.now() + timedelta(days=0)

        admin_data = {
            "username": username,
            "password": password,
            "panel_id": panel_id,
            "inbound_id": inbound_id,
            "expiry_time": expiry_time,
        }

        if admins_query.create_admin(
            username, password, panel_id, inbound_id, expiry_time
        ):
            await message.answer(
                BOT_MESSAGE.REGISTERITION_REQUEST_APPROVED[bot_language],
                parse_mode="HTML",
                reply_markup=main_admin_menu(bot_language),
            )

            notif_for_admin = BOT_MESSAGE.YOUR_REGISTERITION_REQUEST_HAS_BEEN_CONFIRMED[
                bot_language
            ].format(username=username, password=password)

            await message.bot.send_message(
                requested_user_id, text=notif_for_admin, parse_mode="HTML"
            )
        else:
            await message.answer(
                BOT_MESSAGE.ERROR[bot_language],
                reply_markup=main_admin_menu(bot_language),
            )

        await state.clear()

    except Exception as e:
        await message.answer(
            BOT_MESSAGE.ERROR[bot_language].format(e=e),
            reply_markup=main_admin_menu(bot_language),
        )
        await state.clear()


# Dealers/admins login
@router.message(LoginUserStates.enter_username)
async def enter_username(message: types.Message, bot_language: str, state: FSMContext):
    try:
        if message.text in [
            BOT_MESSAGE.BUTTON_CANCEL["en"],
            BOT_MESSAGE.BUTTON_CANCEL["fa"],
        ]:
            await message.answer(
                BOT_MESSAGE.CANCEL_OPERATION[bot_language],
                reply_markup=start_menu(bot_language),
            )
            await state.clear()
            return

        username = message.text
        await message.answer(BOT_MESSAGE.LOGIN_STEP2[bot_language])
        await state.update_data(username=username)
        await state.set_state(LoginUserStates.enter_password)

    except Exception as e:
        await message.answer(
            BOT_MESSAGE.ERROR[bot_language].format(e=e),
            reply_markup=start_menu(bot_language),
        )
        await state.clear()


@router.message(LoginUserStates.enter_password)
async def enter_password(message: types.Message, bot_language: str, state: FSMContext):
    try:
        if message.text in [
            BOT_MESSAGE.BUTTON_CANCEL["en"],
            BOT_MESSAGE.BUTTON_CANCEL["fa"],
        ]:
            await message.answer(
                BOT_MESSAGE.CANCEL_OPERATION[bot_language],
                reply_markup=start_menu(bot_language),
            )
            await state.clear()
            return

        password = message.text
        await state.update_data(password=password)

        # Generate and send captcha
        question, answer = await generate_captcha()
        await state.update_data(captcha_answer=answer)
        await message.answer(
            BOT_MESSAGE.LOGIN_STEP3[bot_language].format(question=question),
            reply_markup=dealer_cancel_keyboard(bot_language),
        )
        await state.set_state(LoginUserStates.enter_captcha)

    except Exception as e:
        await message.answer(
            BOT_MESSAGE.ERROR[bot_language].format(e=e),
            reply_markup=start_menu(bot_language),
        )
        await state.clear()


@router.message(LoginUserStates.enter_captcha)
async def enter_captcha(message: types.Message, bot_language: str, state: FSMContext):
    try:
        if message.text in [
            BOT_MESSAGE.BUTTON_CANCEL["en"],
            BOT_MESSAGE.BUTTON_CANCEL["fa"],
        ]:
            await message.answer(
                BOT_MESSAGE.CANCEL_OPERATION[bot_language],
                reply_markup=start_menu(bot_language),
            )
            await state.clear()
            return

        user_answer = message.text
        state_data = await state.get_data()
        correct_answer = state_data.get("captcha_answer")
        username = state_data.get("username")
        password = state_data.get("password")

        if user_answer != correct_answer:
            # Generate new captcha if answer is wrong
            question, answer = await generate_captcha()
            await state.update_data(captcha_answer=answer)
            await message.answer(
                BOT_MESSAGE.CAPTCHA_WRONG[bot_language],
                reply_markup=dealer_cancel_keyboard(bot_language),
            )
            await message.answer(
                BOT_MESSAGE.LOGIN_STEP3[bot_language].format(question=question)
            )
            return

        if admins_query.login_admin(username, password, message.chat.id):
            await message.answer(
                BOT_MESSAGE.LOGIN_SUCCESS[bot_language],
                reply_markup=admin_menu(bot_language),
            )
            await state.clear()
        else:
            await message.answer(
                BOT_MESSAGE.LOGIN_FAILED[bot_language],
                reply_markup=start_menu(bot_language),
            )
            await state.clear()
            return

    except Exception as e:
        await message.answer(
            BOT_MESSAGE.ERROR[bot_language].format(e=e),
            reply_markup=start_menu(bot_language),
        )
        await state.clear()


#
async def check_loged_in(chat_id: str) -> bool:
    try:
        if chat_id in logged_in_admins:
            return True

        # Check database for login status
        if admins_query.check_loged_in(chat_id):
            logged_in_admins.append(chat_id)
            return True

        return False
    except:
        return False


async def logout_admin(chat_id: str) -> None:
    """Remove admin from logged_in_admins list and database"""
    if chat_id in logged_in_admins:
        logged_in_admins.remove(chat_id)
        admins_query.logout_admin(chat_id)
