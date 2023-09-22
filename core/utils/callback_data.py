from aiogram.filters.callback_data import CallbackData
from datetime import datetime, date, time
from typing import Optional


class OpenLessonCallback(CallbackData, prefix='fabnum'):
    id_lesson: int
    # date: datetime
    # start_lesson: time
    # end_lesson: time
    # student: Optional[int] = None
    # party: Optional[int] = None


class GetStudentForLesson(CallbackData, prefix='open_students'):
    id_lesson: int


class AddPartyToLesson(CallbackData, prefix='add_students'):
    id_lesson: int


class AddStudentToLesson(CallbackData, prefix='add_students'):
    id_lesson: int


class ShowPartyForAddToLesson(CallbackData, prefix='add_party_to_lesson'):
    lesson_id: int
    party_id: int
    party_name: str




