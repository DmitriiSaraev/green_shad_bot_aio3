from aiogram.fsm.state import StatesGroup, State


class StepForm(StatesGroup):
    GET_NAME = State()
    GET_MID_NAME = State()
    GET_LAST_NAME = State()
    GET_AGE = State()


class StateSchedule(StatesGroup):
    INPUT_DATE = State()
    INPUT_START_LESSON = State()
    INPUT_AND_LESSON = State()



