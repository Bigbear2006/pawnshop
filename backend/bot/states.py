from aiogram.fsm.state import State, StatesGroup


class EvaluationState(StatesGroup):
    photo = State()
    amount = State()


class RegistrationState(StatesGroup):
    confirmation = State()
    name = State()
    birth_date = State()
