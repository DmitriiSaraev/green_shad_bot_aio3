from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder


from core.keyboards.inline import (get_inline_keyboard_for_schedule,
                                   get_keyboard_lessons,
                                   get_keyboard_id_lesson)
from core.utils.callback_data import OpenLessonCallback
from core.utils.statesform import StateSchedule
from core.utils.parser import (main_date_parser,
                               pars_date,
                               pars_time)
from core.sql.worker_sql import (add_lesson,
                                 get_all_future_lessons,
                                 get_lesson)



schedule_router = Router()

@schedule_router.message(Command('schedule'))
async def cmd_schedule(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='Составить расписание',
        callback_data='make_a_schedule')
    )

    await message.answer(text='Нажми на кнопку - получишь результат!',
                         reply_markup=builder.as_markup())


@schedule_router.callback_query(F.data == 'make_a_schedule')
async def send_schedule(callback: types.CallbackQuery):
    await callback.message.answer(str('Лови расписание'))
    await callback.answer()


# Выбираем просмотр расписания, либо создание урока
@schedule_router.callback_query(F.data == 'get_buttons_for_work_schedule')
async def action_selection_schedule(callback: types.CallbackQuery):
    await callback.message.answer(text='Что будешь делать?',
                         reply_markup=get_inline_keyboard_for_schedule())
    await callback.answer()


### Блок создания урока ###
@schedule_router.callback_query(F.data == 'add_lesson')
async def get_date_for_new_lesson(callback: types.CallbackQuery,
                                  state: FSMContext):
    await callback.message.answer(text='Введи дату урока в формате дд.мм.гг')
    await state.set_state(StateSchedule.INPUT_DATE)
    await callback.answer()


@schedule_router.message(StateSchedule.INPUT_DATE)
async def get_time_start_for_new_lesson(message: types.Message,
                                        state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer('Введи время начала урока в формате чч.мм')
    await state.set_state(StateSchedule.INPUT_START_LESSON)


@schedule_router.message(StateSchedule.INPUT_START_LESSON)
async def get_duration_for_new_lesson(message: types.Message,
                                      state: FSMContext):
    await state.update_data(start_time=message.text)
    await message.answer('Введи продолжительность урока в формате мм')
    await state.set_state(StateSchedule.INPUT_LESSON_DURATION)


@schedule_router.message(StateSchedule.INPUT_LESSON_DURATION)
async def create_new_lesson(message: types.Message, state: FSMContext):
    await state.update_data(and_time=message.text)

    context_data = await state.get_data()

    date_dict = main_date_parser(context_data)

    lesson = add_lesson(date_dict['date'],
                        date_dict['start_lesson'],
                        date_dict['and_lesson']
                        )

    await message.answer(f'Создан урок дата: {pars_date(date_dict["date"])}\r\n'
                         f'Время начала:'
                         f' {pars_time(date_dict["start_lesson"])}\r\n'
                         f'Конец урока: {pars_time(date_dict["and_lesson"])}')

    await state.clear()

### Конец блока создания урока ###



### Блок просморта расписания ###

@schedule_router.callback_query(F.data == 'get_schedule')
async def get_schedule(callback: types.CallbackQuery):
    lessons = get_all_future_lessons()
    keyboard = get_keyboard_lessons(lessons)

    if len(lessons) == 0:
        await callback.message.answer(text='Уроков нет.',
                                      reply_markup=keyboard)
    else:
        await callback.message.answer(text='Вот оно - расписание твоей мечты:',
                                      reply_markup=keyboard)
    await callback.answer()


@schedule_router.callback_query(OpenLessonCallback.filter())
async def callbacks_lesson_fub(callback: types.CallbackQuery,
                               callback_data: OpenLessonCallback):
    lesson = get_lesson(callback_data.id_lesson)

    keyboard = get_keyboard_id_lesson(lesson)
    await callback.message.answer(text='Урок',
                                  reply_markup=keyboard)




    await callback.answer()








