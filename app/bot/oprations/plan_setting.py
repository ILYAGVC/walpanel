from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from app.bot.messages.messages import BOT_MESSAGE

from app.bot.states.states import AddPlanStates, EditPlanStates, DeletePlanStates
from app.bot.keyboards.main_admin_keyboards import (
    settings_menu,
    sales_plan_menu,
    cancel_keyboard,
    confirmation_keyboard,
)
from app.bot.services.query import plans_query

router = Router()


async def show_plans(message: types.Message, bot_language: str):
    """Show current sales plans."""
    plans = plans_query.get_plans()
    if not plans:
        await message.answer(
            BOT_MESSAGE.PLAN_IS_NOT_EXIST[bot_language],
            reply_markup=sales_plan_menu(bot_language),
        )
        return

    text = "📊 Plans\n\n"
    for plan in plans:
        text += BOT_MESSAGE.SHOW_PLANS[bot_language].format(
            id=plan["id"],
            traffic=plan["traffic"],
            deadline=plan["deadline"],
            price=plan["price"],
        )

    await message.answer(
        text, reply_markup=sales_plan_menu(bot_language), parse_mode="HTML"
    )


@router.message(AddPlanStates.waiting_for_traffic)
async def add_plan_traffic(
    message: types.Message, bot_language: str, state: FSMContext
):
    try:
        if message.text in [
            BOT_MESSAGE.BUTTON_CANCEL["en"],
            BOT_MESSAGE.BUTTON_CANCEL["fa"],
        ]:
            await message.answer(
                BOT_MESSAGE.CANCEL_OPERATION[bot_language],
                reply_markup=settings_menu(bot_language),
            )
            await state.clear()
            return
        traffic = int(message.text)
        if traffic <= 0:
            raise ValueError
        # Save traffic and move to next state
        await state.update_data(traffic=traffic)
        await message.answer(
            BOT_MESSAGE.WAITING_FOR_PLAN_DEADLINE[bot_language],
            reply_markup=cancel_keyboard(bot_language),
        )
        await state.set_state(AddPlanStates.waiting_for_deadline)
    except ValueError:
        await message.answer(
            BOT_MESSAGE.INVALID_VALUE[bot_language],
            reply_markup=cancel_keyboard(bot_language),
        )


@router.message(AddPlanStates.waiting_for_deadline)
async def add_plan_deadline(
    message: types.Message, bot_language: str, state: FSMContext
):
    try:
        if message.text in [
            BOT_MESSAGE.BUTTON_CANCEL["en"],
            BOT_MESSAGE.BUTTON_CANCEL["fa"],
        ]:
            await message.answer(
                BOT_MESSAGE.CANCEL_OPERATION[bot_language],
                reply_markup=settings_menu(bot_language),
            )
            await state.clear()
            return
        deadline = int(message.text)
        if deadline <= 0:
            raise ValueError
        # Save deadline and move to next state
        await state.update_data(deadline=deadline)
        await message.answer(
            BOT_MESSAGE.WAITING_FOR_PLAN_PRICE[bot_language],
            reply_markup=cancel_keyboard(bot_language),
        )
        await state.set_state(AddPlanStates.waiting_for_price)
    except ValueError:
        await message.answer(
            BOT_MESSAGE.INVALID_VALUE[bot_language],
            reply_markup=cancel_keyboard(bot_language),
        )


@router.message(AddPlanStates.waiting_for_price)
async def add_plan_price(message: types.Message, bot_language: str, state: FSMContext):
    try:
        if message.text in [
            BOT_MESSAGE.BUTTON_CANCEL["en"],
            BOT_MESSAGE.BUTTON_CANCEL["fa"],
        ]:
            await message.answer(
                BOT_MESSAGE.CANCEL_OPERATION[bot_language],
                reply_markup=settings_menu(bot_language),
            )
            await state.clear()
            return
        price = int(message.text)
        if price <= 0:
            raise ValueError

        # Get all saved data
        data = await state.get_data()
        traffic = data.get("traffic")
        deadline = data.get("deadline")

        if plans_query.add_plan(traffic, deadline, price):
            await message.answer(
                BOT_MESSAGE.PLAN_ADDED[bot_language],
                reply_markup=settings_menu(bot_language),
            )
        else:
            await message.answer(
                BOT_MESSAGE.ERROR[bot_language],
                reply_markup=settings_menu(bot_language),
            )

        await state.clear()

    except ValueError:
        await message.answer(
            BOT_MESSAGE.INVALID_VALUE[bot_language],
            reply_markup=cancel_keyboard(bot_language),
        )


@router.message(EditPlanStates.waiting_for_id)
async def edit_plan_id_step(
    message: types.Message, bot_language: str, state: FSMContext
):
    try:
        if message.text in [
            BOT_MESSAGE.BUTTON_CANCEL["en"],
            BOT_MESSAGE.BUTTON_CANCEL["fa"],
        ]:
            await message.answer(
                BOT_MESSAGE.CANCEL_OPERATION[bot_language],
                reply_markup=settings_menu(bot_language),
            )
            await state.clear()
            return
        plan_id = int(message.text)
        if not plans_query.get_a_plan_by_id(plan_id):
            raise ValueError

        await state.update_data(plan_id=plan_id)
        await message.answer(
            BOT_MESSAGE.WAITING_FOR_PLAN_TRAFFIC[bot_language],
            reply_markup=cancel_keyboard(bot_language),
        )
        await state.set_state(EditPlanStates.waiting_for_traffic)
    except ValueError:
        await message.answer(
            BOT_MESSAGE.PLAN_NOT_EXIST[bot_language],
            reply_markup=cancel_keyboard(bot_language),
        )


@router.message(EditPlanStates.waiting_for_traffic)
async def edit_plan_traffic_step(
    message: types.Message, bot_language: str, state: FSMContext
):
    try:
        if message.text in [
            BOT_MESSAGE.BUTTON_CANCEL["en"],
            BOT_MESSAGE.BUTTON_CANCEL["fa"],
        ]:
            await message.answer(
                BOT_MESSAGE.CANCEL_OPERATION[bot_language],
                reply_markup=settings_menu(bot_language),
            )
            await state.clear()
            return
        traffic = int(message.text)
        if traffic <= 0:
            raise ValueError
        await state.update_data(traffic=traffic)
        await message.answer(
            BOT_MESSAGE.WAITING_FOR_PLAN_DEADLINE[bot_language],
            reply_markup=cancel_keyboard(bot_language),
        )
        await state.set_state(EditPlanStates.waiting_for_deadline)
    except ValueError:
        await message.answer(
            BOT_MESSAGE.INVALID_VALUE[bot_language],
            reply_markup=cancel_keyboard(bot_language),
        )


@router.message(EditPlanStates.waiting_for_deadline)
async def edit_plan_deadline_step(
    message: types.Message, bot_language: str, state: FSMContext
):
    try:
        if message.text in [
            BOT_MESSAGE.BUTTON_CANCEL["en"],
            BOT_MESSAGE.BUTTON_CANCEL["fa"],
        ]:
            await message.answer(
                BOT_MESSAGE.CANCEL_OPERATION[bot_language],
                reply_markup=settings_menu(bot_language),
            )
            await state.clear()
            return
        deadline = int(message.text)
        if deadline <= 0:
            raise ValueError
        await state.update_data(deadline=deadline)
        await message.answer(
            BOT_MESSAGE.WAITING_FOR_PLAN_PRICE[bot_language],
            reply_markup=cancel_keyboard(bot_language),
        )
        await state.set_state(EditPlanStates.waiting_for_price)
    except ValueError:
        await message.answer(
            BOT_MESSAGE.INVALID_VALUE[bot_language],
            reply_markup=cancel_keyboard(bot_language),
        )


@router.message(EditPlanStates.waiting_for_price)
async def edit_plan_price_step(
    message: types.Message, bot_language: str, state: FSMContext
):
    try:
        if message.text in [
            BOT_MESSAGE.BUTTON_CANCEL["en"],
            BOT_MESSAGE.BUTTON_CANCEL["fa"],
        ]:
            await message.answer(
                BOT_MESSAGE.CANCEL_OPERATION[bot_language],
                reply_markup=settings_menu(bot_language),
            )
            await state.clear()
            return
        price = int(message.text)
        if price <= 0:
            raise ValueError

        data = await state.get_data()
        id = data.get("plan_id")
        traffic = data.get("traffic")
        deadline = data.get("deadline")

        if plans_query.edit_plan(id, traffic, deadline, price):
            await message.answer(
                BOT_MESSAGE.PLAN_UPDATED[bot_language],
                reply_markup=settings_menu(bot_language),
            )
        else:
            await message.answer(
                BOT_MESSAGE.PLAN_NOT_EXIST[bot_language],
                reply_markup=settings_menu(bot_language),
            )
        await state.clear()
    except ValueError:
        await message.answer(
            BOT_MESSAGE.INVALID_VALUE[bot_language],
            reply_markup=cancel_keyboard(bot_language),
        )


@router.message(DeletePlanStates.waiting_for_id)
async def delete_plan_step(
    message: types.Message, bot_language: str, state: FSMContext
):
    try:
        if message.text in [
            BOT_MESSAGE.BUTTON_CANCEL["en"],
            BOT_MESSAGE.BUTTON_CANCEL["fa"],
        ]:
            await message.answer(
                BOT_MESSAGE.CANCEL_OPERATION[bot_language],
                reply_markup=settings_menu(bot_language),
            )
            await state.clear()
            return
        plan_id = int(message.text)

        # Check if plan exists
        if not plans_query.get_a_plan_by_id(plan_id):
            await message.answer(
                BOT_MESSAGE.PLAN_NOT_EXIST[bot_language],
                reply_markup=cancel_keyboard(bot_language),
            )
            return

        await state.update_data(plan_id=plan_id)
        await state.set_state(DeletePlanStates.waiting_for_confirmation)
        await message.answer(
            BOT_MESSAGE.CONFIRM_PLAN_DELETE[bot_language],
            reply_markup=confirmation_keyboard(bot_language),
        )
    except ValueError:
        await message.answer(
            BOT_MESSAGE.INVALID_VALUE[bot_language],
            reply_markup=cancel_keyboard(bot_language),
        )


@router.message(DeletePlanStates.waiting_for_confirmation)
async def delete_plan_confirmation_step(
    message: types.Message, bot_language: str, state: FSMContext
):
    try:
        if message.text in [BOT_MESSAGE.BUTTON_YES["en"], BOT_MESSAGE.BUTTON_YES["fa"]]:
            data = await state.get_data()
            plan_id = data.get("plan_id")
            if plans_query.delete_plan(plan_id):
                await message.answer(
                    BOT_MESSAGE.PLAN_DELETED[bot_language],
                    reply_markup=sales_plan_menu(bot_language),
                )
            else:
                await message.answer(
                    BOT_MESSAGE.PLAN_NOT_EXIST[bot_language],
                    reply_markup=sales_plan_menu(bot_language),
                )
            await state.clear()
        elif message.text in [BOT_MESSAGE.BUTTON_NO["en"], BOT_MESSAGE.BUTTON_NO["fa"]]:
            await message.answer(
                BOT_MESSAGE.CANCEL_OPERATION[bot_language],
                reply_markup=sales_plan_menu(bot_language),
            )
            await state.clear()
    except ValueError:
        await message.answer(
            BOT_MESSAGE.INVALID_VALUE[bot_language],
            reply_markup=cancel_keyboard(bot_language),
        )
