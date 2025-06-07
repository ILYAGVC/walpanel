from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, date

import time
import random

from app.bot.services.query import (
    payment_gateway_query,
    plans_query,
    purchase_history_query,
    admins_query,
)
from app.bot.messages.messages import BOT_MESSAGE
from app.bot.states.states import PaymentState
from app.bot.config import MAIN_ADMIN, EXTOPAY_CALLBACK_URL
from app.bot.keyboards.keyboards import (
    intermediary_gateway_keyboard,
)
from app.bot.services.api import intermediary_api

router = Router()


@router.callback_query(F.data.startswith("confirm_payment_intermediary:"))
async def confirm_payment_intermediary_handle(
    callback: types.CallbackQuery, state: FSMContext
):
    try:
        _, plan_id, chat_id, bot_language = callback.data.split(":")

        await callback.message.delete()
        plan = plans_query.get_a_plan_by_id(plan_id)
        await state.set_state(PaymentState.waiting_for_intermediary_payment)
        await state.update_data(
            plan_id=plan_id, chat_id=chat_id, bot_language=bot_language
        )

        await callback.message.answer(
            BOT_MESSAGE.PRE_PAY_WITH_GATEWAY[bot_language].format(price=plan["price"]),
            parse_mode="HTML",
            reply_markup=intermediary_gateway_keyboard(
                plan["price"], bot_language, plan_id
            ),
        )

    except Exception as e:
        await callback.answer(
            BOT_MESSAGE.ERROR[bot_language].format(e=e), show_alert=True
        )


@router.callback_query(F.data.startswith("process_gateway_payment:"))
async def process_gateway_payment_handle(callback: types.CallbackQuery):
    try:
        _, bot_language, amount, plan_id = callback.data.split(":")

        # Generate a unique order ID
        today = datetime.now().strftime("%Y%m%d")
        randomint = random.randint(1, 99)
        order_id = f"PAY_{amount}_{bot_language}_{plan_id}_{callback.from_user.id}_{today}_{randomint}"

        callback_url = EXTOPAY_CALLBACK_URL

        payment_result = await intermediary_api.make_a_payment_url(
            order_id=order_id,
            amount=int(amount),
            callback_url=callback_url,
        )

        if payment_result:
            # Send payment URL to user
            await callback.message.edit_text(
                BOT_MESSAGE.PRE_PAY_WITH_GATEWAY[bot_language].format(price=amount),
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text=BOT_MESSAGE.BUTTON_PAY[bot_language],
                                url=payment_result["link"],
                            )
                        ],
                    ]
                ),
            )
        else:
            await callback.message.edit_text(BOT_MESSAGE.GEATWAY_ERROR[bot_language])

    except Exception as e:
        await callback.answer(
            BOT_MESSAGE.ERROR[bot_language].format(e=e), show_alert=True
        )


# Send notification when payment fails
async def payment_filed(
    amount: int,
    bot_language: str,
    plan_id: int,
    chat_id: int,
    order_id: str,
    timestamp: date,
):
    """Notify user and admin when payment fails and update purchase history."""
    from app.bot.main import bot

    await bot.send_message(
        chat_id,
        BOT_MESSAGE.PAYMENT_FAILED[bot_language].format(order_id=order_id),
        parse_mode="HTML",
    )
    await bot.send_message(
        MAIN_ADMIN,
        BOT_MESSAGE.ADMIN_PAYMENT_FAILED_NOTIF[bot_language].format(
            amount=amount,
            chat_id=chat_id,
            plan_id=plan_id,
            order_id=order_id,
            timestamp=timestamp,
        ),
        parse_mode="HTML",
    )

    await purchase_history_query.add_purchase_history(
        chat_id=chat_id,
        amount=amount,
        status=False,
        order_id=order_id,
        timestamp=timestamp,
    )


# Send notification when payment is made
async def payment_is_made(
    amount: int,
    bot_language: str,
    plan_id: int,
    chat_id: int,
    order_id: str,
    timestamp: datetime,
):
    """Notify user and admin when payment is successful and update purchase history."""
    from app.bot.main import bot

    await purchase_history_query.add_purchase_history(
        chat_id=chat_id,
        amount=amount,
        status=True,
        order_id=order_id,
        timestamp=timestamp,
    )

    plan = plans_query.get_a_plan_by_id(plan_id)
    # Update the dealer's plan in the database
    if admins_query.purchase_confirmation(chat_id, plan["traffic"], plan["deadline"]):
        await bot.send_message(
            chat_id,
            BOT_MESSAGE.PAYMENT_SUCCESS[bot_language].format(order_id=order_id),
            parse_mode="HTML",
        )
        await bot.send_message(
            MAIN_ADMIN,
            BOT_MESSAGE.ADMIN_PAYMENT_SUCCESS_NOTIF[bot_language].format(
                amount=amount,
                chat_id=chat_id,
                plan_id=plan_id,
                order_id=order_id,
                timestamp=timestamp,
            ),
            parse_mode="HTML",
        )
