from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.services.query import settings_query, plans_query, admins_query, card_query
from app.bot.messages.messages import BOT_MESSAGE
from app.bot.states.states import PaymentState
from app.bot.config import MAIN_ADMIN
from app.bot.keyboards.keyboards import cancel_keyboard, cancel_payment_keyboard

router = Router()


@router.callback_query(F.data.startswith("confirm_payment_card:"))
async def handle_confirm_payment(callback: types.CallbackQuery, state: FSMContext):
    try:
        _, plan_id, chat_id, bot_language = callback.data.split(":")

        plan = plans_query.get_a_plan_by_id(plan_id)
        card_num = card_query.get_card()
        await state.set_state(PaymentState.waiting_for_card_payment)
        await state.update_data(
            plan_id=plan_id, chat_id=chat_id, bot_language=bot_language
        )

        await callback.message.answer(
            BOT_MESSAGE.SEND_CARD_PAYMENT_PHOTO[bot_language].format(
                price=plan["price"], card_num=card_num
            ),
            parse_mode="HTML",
            reply_markup=cancel_payment_keyboard(bot_language),
        )
    except Exception as e:
        await callback.answer(
            BOT_MESSAGE.ERROR[bot_language].format(e=e), show_alert=True
        )


@router.message(PaymentState.waiting_for_card_payment)
async def handle_card_payment_message(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        bot_language = data.get("bot_language")

        if message.text in [
            BOT_MESSAGE.BUTTON_CANCEL["en"],
            BOT_MESSAGE.BUTTON_CANCEL["fa"],
        ]:
            await message.answer(
                BOT_MESSAGE.PAYMENT_CANCELLED[bot_language], parse_mode="HTML"
            )
            await state.clear()
            return

        if not message.photo:
            await message.answer(
                BOT_MESSAGE.ERROR[bot_language].format(
                    e="Please send a photo of your payment receipt"
                ),
                parse_mode="HTML",
                reply_markup=cancel_payment_keyboard(bot_language),
            )
            return

        plan_id = data.get("plan_id")
        chat_id = data.get("chat_id")
        plan = plans_query.get_a_plan_by_id(plan_id)
        admin = admins_query.get_admin_by_chat_id(chat_id)

        # Forward payment photo to main admin for confirmation
        admin_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=BOT_MESSAGE.APPROVE_PAYMENT[bot_language],
                        callback_data=f"approve_payment:{chat_id}:{plan_id}:{message.message_id}:{bot_language}",
                    ),
                    InlineKeyboardButton(
                        text=BOT_MESSAGE.REJECT_PAYMENT[bot_language],
                        callback_data=f"reject_payment:{chat_id}:{message.message_id}:{bot_language}",
                    ),
                ]
            ]
        )

        payment_info = BOT_MESSAGE.PAYMENT_CONFIRMATION_REQUEST[bot_language].format(
            username=admin["username"],
            traffic=plan["traffic"],
            days=plan["deadline"],
            price=plan["price"],
        )

        # Send to main admin
        await message.bot.send_photo(
            chat_id=MAIN_ADMIN,
            photo=message.photo[-1].file_id,
            caption=payment_info,
            reply_markup=admin_keyboard,
        )

        await message.answer(
            BOT_MESSAGE.PAYMENT_SENT_FOR_APPROVAL[bot_language], parse_mode="HTML"
        )
        await state.clear()

    except Exception as e:
        await message.answer(
            BOT_MESSAGE.ERROR[bot_language].format(e=e),
            parse_mode="HTML",
            reply_markup=cancel_payment_keyboard(bot_language),
        )


@router.callback_query(F.data.startswith("approve_payment:"))
async def handle_approve_payment(callback: types.CallbackQuery):
    try:
        _, user_chat_id, plan_id, message_id, bot_language = callback.data.split(":")
        plan = plans_query.get_a_plan_by_id(plan_id)

        if admins_query.purchase_confirmation(
            user_chat_id, plan["traffic"], plan["deadline"]
        ):
            await callback.bot.send_message(
                chat_id=user_chat_id,
                text=BOT_MESSAGE.PAYMENT_APPROVED[bot_language],
                parse_mode="HTML",
            )

            # Update admin's message
            await callback.message.edit_caption(
                caption=callback.message.caption
                + "\n\n"
                + BOT_MESSAGE.PAYMENT_APPROVED_BY_ADMIN[bot_language],
                reply_markup=None,
            )
            await callback.answer(BOT_MESSAGE.PAYMENT_APPROVED_BY_ADMIN[bot_language])
        else:
            await callback.answer(
                BOT_MESSAGE.ERROR[bot_language].format(
                    e="Failed to update user's plan"
                ),
                show_alert=True,
            )

    except Exception as e:
        await callback.answer(
            BOT_MESSAGE.ERROR[bot_language].format(e=e), show_alert=True
        )


@router.callback_query(F.data.startswith("reject_payment:"))
async def handle_reject_payment(callback: types.CallbackQuery):
    try:
        _, user_chat_id, message_id, bot_language = callback.data.split(":")

        # Notify user
        await callback.bot.send_message(
            chat_id=user_chat_id,
            text=BOT_MESSAGE.PAYMENT_REJECTED[bot_language],
            parse_mode="HTML",
        )

        await callback.message.edit_caption(
            caption=callback.message.caption
            + "\n\n"
            + BOT_MESSAGE.PAYMENT_REJECTED_BY_ADMIN[bot_language],
            reply_markup=None,
        )

    except Exception as e:
        await callback.answer(
            BOT_MESSAGE.ERROR[bot_language].format(e=e), show_alert=True
        )


@router.callback_query(F.data.startswith("cancel_payment_card:"))
async def handle_cancel_payment(callback: types.CallbackQuery, state: FSMContext):
    try:
        _, bot_language = callback.data.split(":")
        await callback.message.delete()
        await callback.answer(
            BOT_MESSAGE.PAYMENT_CANCELLED[bot_language], parse_mode="HTML"
        )
        await state.clear()
    except Exception as e:
        await callback.answer(
            BOT_MESSAGE.ERROR[bot_language].format(e=e), show_alert=True
        )
