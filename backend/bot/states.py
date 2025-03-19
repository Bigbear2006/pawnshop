from aiogram.fsm.state import StatesGroup, State


class EvaluationState(StatesGroup):
    photo = State()
    amount = State()
