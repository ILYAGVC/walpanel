from aiogram.fsm.state import State, StatesGroup


class HelpTextStates(StatesGroup):
    waiting_for_new_help_text = State()


class RegistrationTextStates(StatesGroup):
    waiting_for_new_registration_text = State()


class AddPlanStates(StatesGroup):
    waiting_for_traffic = State()
    waiting_for_deadline = State()
    waiting_for_price = State()


class EditPlanStates(StatesGroup):
    waiting_for_id = State()
    waiting_for_traffic = State()
    waiting_for_deadline = State()
    waiting_for_price = State()


class DeletePlanStates(StatesGroup):
    waiting_for_id = State()
    waiting_for_confirmation = State()


class RegisterUserStates(StatesGroup):
    enter_username = State()
    enter_password = State()
    enter_panel_id = State()
    enter_inbound_id = State()


class LoginUserStates(StatesGroup):
    enter_username = State()
    enter_password = State()
    enter_captcha = State()


class PaymentState(StatesGroup):
    waiting_for_card_payment = State()


class SettingsState(StatesGroup):
    waiting_for_card_number = State()
