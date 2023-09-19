from aiogram.filters.callback_data import CallbackData
from datetime import datetime, date, time
from typing import Optional


class OpenLessonCallback(CallbackData, prefix='fabnum'):
    id_lesson: int
    # date: datetime
    # start_lesson: time
    # and_lesson: time
    # student: Optional[int] = None
    # party: Optional[int] = None
