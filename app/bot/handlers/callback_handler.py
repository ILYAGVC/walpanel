from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.keyboards.main_admin_keyboards import registration_confirmation_menu
from app.bot.services.query import settings_query, plans_query, payment_gateway_query
from app.bot.messages.messages import BOT_MESSAGE
from app.bot.states.states import RegisterUserStates, PaymentState
from app.bot.config import MAIN_ADMIN

router = Router()


@router.callback_query(F.data.startswith("accept_rules:"))
async def accept_rules(callback: types.CallbackQuery, state: FSMContext):
    _, chat_id, full_name, username, bot_language = callback.data.split(":")
    await callback.message.delete()
    await callback.message.answer(
        BOT_MESSAGE.WAITING_FOR_CONFIRM_SIGNUP_ADMIN[bot_language]
    )

    notif_for_main_admin = BOT_MESSAGE.A_NEW_SIGNUP_REQUEST[bot_language].format(
        chat_id=chat_id, name=full_name, user_id=username
    )
    await callback.bot.send_message(
        MAIN_ADMIN,
        notif_for_main_admin,
        parse_mode="HTML",
        reply_markup=registration_confirmation_menu(chat_id, bot_language),
    )


@router.callback_query(F.data.startswith("decline_rules:"))
async def decline_rules(callback: types.CallbackQuery):
    _, chat_id, full_name, username, bot_language = callback.data.split(":")

    await callback.message.delete()

    notif_for_main_admin = BOT_MESSAGE.REJECT_REGISTERATION_RULES[bot_language].format(
        chat_id=chat_id, name=full_name, user_id=username
    )
    await callback.bot.send_message(
        MAIN_ADMIN,
        notif_for_main_admin,
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("buy_plan:"))
async def handle_buy_plan(callback: types.CallbackQuery):
    try:
        _, plan_id, chat_id, bot_language = callback.data.split(":")
        plan = plans_query.get_a_plan_by_id(plan_id)

        message_text = BOT_MESSAGE.SELECTED_PLAN[bot_language].format(
            traffic=plan["traffic"],
            expiry_time=plan["deadline"],
            price=plan["price"],
        )
        await callback.message.delete()

        # Check payments methods
        card_enabled = await settings_query.get_card_method()
        intermediary_enabled = await settings_query.get_intermediary_gateway()

        if not (card_enabled or intermediary_enabled):
            await callback.message.answer(
                BOT_MESSAGE.PAYMENT_DISABLED[bot_language], parse_mode="HTML"
            )
            return

        keyboard_buttons = []

        if card_enabled:
            keyboard_buttons.append(
                [
                    InlineKeyboardButton(
                        text=BOT_MESSAGE.PAYMENT_WITH_CARD[bot_language],
                        callback_data=f"confirm_payment_card:{plan_id}:{chat_id}:{bot_language}",
                    )
                ]
            )

        if intermediary_enabled:
            keyboard_buttons.append(
                [
                    InlineKeyboardButton(
                        text=BOT_MESSAGE.PAYMENT_WITH_INTERMEDIARY[bot_language],
                        callback_data=f"confirm_payment_intermediary:{plan_id}:{chat_id}:{bot_language}",
                    )
                ]
            )

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

        await callback.message.answer(
            message_text + "\n\n" + BOT_MESSAGE.SEND_PAYMENT_METHODS[bot_language],
            parse_mode="HTML",
            reply_markup=keyboard,
        )

    except Exception as e:
        await callback.answer(
            BOT_MESSAGE.ERROR[bot_language].format(e=e), show_alert=True
        )


@router.callback_query(F.data.startswith("cancel_payment:"))
async def cancel_payment(callback: types.CallbackQuery):
    _, bot_language = callback.data.split(":")
    await callback.message.delete()
    await callback.answer(
        BOT_MESSAGE.PAYMENT_CANCELLED[bot_language],
        parse_mode="HTML",
        show_alert=True,
    )
