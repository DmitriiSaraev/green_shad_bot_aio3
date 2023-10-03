import datetime

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder


from core.keyboards.inline import (get_inline_keyboard_for_schedule,
                                   get_keyboard_lessons,
                                   get_keyboard_id_lesson,
                                   get_inline_keyboard_add_student_to_lesson,
                                   keyboard_for_working_with_students,
                                   keyboard_add_party_to_lesson,
                                   keyboard_get_students_without_group,
                                   keyboard_add_student_to_party,
                                   keyboard_choice_student_for_lesson,
                                   get_keyboard_recorded_student_to_lesson_and_edit_lesson)

from core.utils.callback_data import (OpenLessonCallback, GetStudentForLesson,
                                      AddPartyToLesson,
                                      ShowPartyForAddToStudent,
                                      AddStudentToParty, AddStudentToLesson,
                                      StudentChoice, ShowPartyForAddToLesson)
from core.utils.statesform import StateSchedule, StateAddParty
from core.utils.parser import (main_date_parser,
                               pars_date,
                               pars_time, get_user_id)

from core.sql.worker_sql import (add_lesson,
                                 get_all_future_lessons,
                                 get_lesson,
                                 get_students_id_from_lesson, get_active_party,
                                 add_party, get_student_without_party,
                                 add_student_to_party_worker,
                                 add_student_to_lesson_worker,
                                 add_party_id_to_users_worker, get_user_data)



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
                        date_dict['end_lesson']
                        )

    await message.answer(f'Создан урок дата: {pars_date(date_dict["date"])}\r\n'
                         f'Время начала:'
                         f' {pars_time(date_dict["start_lesson"])}\r\n'
                         f'Конец урока: {pars_time(date_dict["end_lesson"])}')

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
    list_lesson = get_lesson(callback_data.id_lesson)
    lesson = list_lesson[0]

    keyboard = get_keyboard_id_lesson(lesson)
    await callback.message.answer(text=f'Урок дата {pars_date(lesson["date"])}\r\n'
                                       f'Время {pars_time(lesson["start_lesson"])} - '
                                       f'{pars_time(lesson["end_lesson"])}',
                                  reply_markup=keyboard)

    await callback.answer()


@schedule_router.callback_query(GetStudentForLesson.filter())
async def open_students(callback: types.CallbackQuery,
                        callback_data: GetStudentForLesson):

    # выводит список студентов которые записаны на выбранный урок
    # или кнопки для записи на урок

    lesson_id = callback_data.id_lesson
    students_data_id = get_students_id_from_lesson(lesson_id)

    if len(students_data_id) == 0:
        keyboard = get_inline_keyboard_add_student_to_lesson(lesson_id)
        await callback.message.answer(text='На данный урок ни кто не записан',
                                      reply_markup=keyboard)
    else:
        students_id = get_user_id(students_data_id)
        students = get_user_data(students_id) # Получить имена студентов
        keyboard = get_keyboard_recorded_student_to_lesson_and_edit_lesson(
            lesson_id,
            students
        )

        await callback.message.answer(text='Список записанных:',
                                  reply_markup=keyboard)



    await callback.answer()


@schedule_router.callback_query(AddPartyToLesson.filter())
async def add_party_to_lesson(callback: types.CallbackQuery,
                              callback_data: AddPartyToLesson):
    lesson_id = callback_data.id_lesson
    list_party = get_active_party()

    keyboard = keyboard_add_party_to_lesson(lesson_id, list_party)
    await callback.message.answer(text='Такие вот группы у нас',
                                  reply_markup=keyboard)


    # print(list_party)


    # keyboard = get_keyboard_lessons()
    await callback.answer()


@schedule_router.callback_query(ShowPartyForAddToLesson.filter())
async def choice_and_add_party_to_lesson(
        callback: types.CallbackQuery,
        callback_data: ShowPartyForAddToStudent):
# Записать группу на урок

    lesson_id = callback_data.lesson_id
    party_id = callback_data.party_id
    party_name = callback_data.party_name

    add_student_to_lesson_worker(lesson_id, party_id)

    await callback.message.answer(text=f'Группа записана на урок')
    await callback.answer()





@schedule_router.callback_query(F.data == 'get_buttons_for_work_students')
async def get_buttons_for_working_with_students(callback: types.CallbackQuery):
    keyboard = keyboard_for_working_with_students()

    await callback.message.answer(text='Выбирай',
                                  reply_markup=keyboard)

    await callback.answer()


### Блок создания группы ###
@schedule_router.callback_query(F.data == 'add_party')
async def add_new_party(callback: types.CallbackQuery,
                            state: FSMContext):
    await callback.message.answer(text='Введи название группы')
    await state.set_state(StateAddParty.INPUT_NAME)
    await callback.answer()


@schedule_router.message(StateAddParty.INPUT_NAME)
async def get_name_for_new_party(message: types.Message,
                                 state: FSMContext):

    date = datetime.date.today()
    name = message.text

    party = add_party(date, name)
    await message.answer(text=f'Созданая группа: {name}')


    await state.clear()

### Конец блока создания группы ###


### Блок работы с учеником ###

# Добавить ученика в группу
@schedule_router.callback_query(F.data == 'add_student_to_party')
async def get_student_for_party(callback: types.CallbackQuery):
    students = get_student_without_party()

    keyboard = keyboard_get_students_without_group(
        'show_party_for_add_student', students)


    await callback.message.answer(text='Выбирай ученика',
                                  reply_markup=keyboard)
    await callback.answer()


# Показать группы в которые можно записаться
@schedule_router.callback_query(AddStudentToParty.filter(
    F.action == 'show_party_for_add_student')
)
async def show_party_for_add_student(callback: types.CallbackQuery,
                                     callback_data: AddStudentToParty):
    student_id = callback_data.student_id
    list_party = get_active_party()

    keyboard = keyboard_add_student_to_party(student_id, list_party)
    await callback.message.answer(text='Такие вот группы у нас',
                                  reply_markup=keyboard)

    await callback.answer()


# Записать ученика в группу
@schedule_router.callback_query(ShowPartyForAddToStudent.filter())
async def add_student_to_party(callback: types.CallbackQuery,
                               callback_data: ShowPartyForAddToStudent):
    student_id = callback_data.student_id
    party_id = callback_data.party_id

    add_student_to_party_worker(datetime.date.today(), party_id, student_id)
    add_party_id_to_users_worker(party_id, student_id)

    await callback.message.answer(text=f'Ученик добавлен в группу')
    await callback.answer()


# Показать клаву с учениками, для записи на урок
@schedule_router.callback_query(AddStudentToParty.filter(
    F.action == 'show_student_for_add_to_lesson'))
async def show_student_for_add_lesson(callback: types.CallbackQuery,
                                     callback_data: AddStudentToParty):
    action = 'add_student_to_lesson'
    students = get_student_without_party()
    lesson_id = callback_data.lesson_id

    keyboard = keyboard_get_students_without_group(action, students, lesson_id)
    await callback.message.answer(text='Выбери ученика',
                                  reply_markup=keyboard)

    await callback.answer()


@schedule_router.callback_query(AddStudentToParty.filter(
    F.action == 'add_student_to_lesson'))
async def add_student_to_lesson(callback: types.CallbackQuery,
                                callback_data: AddStudentToLesson):
    student_id = callback_data.student_id
    lesson_id = callback_data.lesson_id

    add_student_to_lesson_worker(lesson_id, student_id)

    await callback.message.answer(text=f'Ученик записан на урок')
    await callback.answer()


