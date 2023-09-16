from aiogram.filters.callback_data import CallbackData


class OpenLessonCallback(CallbackData, prefix='fabnum'):
    id_lesson: int
