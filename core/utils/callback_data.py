from aiogram.filters.callback_data import CallbackData
from datetime import datetime, timedelta, time


class OpenLessonCallback(CallbackData, prefix='fabnum'):
    id_lesson: int
    date: datetime
    start_lesson: datetime
    and_lesson: datetime
    student: int
    party: int
