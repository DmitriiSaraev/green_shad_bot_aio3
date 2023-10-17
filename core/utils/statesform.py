from aiogram.fsm.state import StatesGroup, State


class StepForm(StatesGroup):
    GET_NAME = State()
    GET_MID_NAME = State()
    GET_LAST_NAME = State()
    GET_AGE = State()


class StateSchedule(StatesGroup):
    INPUT_DATE = State()
    INPUT_START_LESSON = State()
    INPUT_END_LESSON = State()
    INPUT_LESSON_DURATION = State()


class StateAddParty(StatesGroup):
    INPUT_NAME = State()


class StateEditLesson(StatesGroup):
    INPUT_DATE_EDIT = State()
    INPUT_START_LESSON_EDIT = State()
    INPUT_LESSON_DURATION_EDIT = State()