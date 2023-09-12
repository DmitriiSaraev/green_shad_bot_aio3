from aiogram.fsm.state import StatesGroup, State


class StepForm(StatesGroup):
    GET_NAME = State()
    GET_MID_NAME = State()
    GET_LAST_NAME = State()
    GET_AGE = State()
