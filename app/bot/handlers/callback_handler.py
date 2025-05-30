from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.keyboards.main_admin_keyboards import registration_confirmation_menu
from app.bot.services.query import settings_query, plans_query, admins_query
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

        if await settings_query.get_card_method():
            # Create confirmation keyboard
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=BOT_MESSAGE.PAYMENT_WITH_CARD[bot_language],
                            callback_data=f"confirm_payment:{plan_id}:{chat_id}:{bot_language}",
                        )
                    ],
                ]
            )

            await callback.message.answer(
                message_text + "\n\n" + BOT_MESSAGE.SEND_PAYMENT_METHODS[bot_language],
                parse_mode="HTML",
                reply_markup=keyboard,
            )
        else:
            await callback.message.answer(
                BOT_MESSAGE.CARD_PAYMENT_DISABLED[bot_language], parse_mode="HTML"
            )

    except Exception as e:
        await callback.answer(
            BOT_MESSAGE.ERROR[bot_language].format(e=e), show_alert=True
        )
