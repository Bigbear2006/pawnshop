from aiogram.fsm.state import State, StatesGroup


class EvaluationState(StatesGroup):
    photo = State()
    amount = State()
