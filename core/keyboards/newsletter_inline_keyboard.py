from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inline_keyboard_newsletter():
    builder = InlineKeyboardBuilder()
    builder.button(text='Отправить напоминание о завтрашних уроках',
                   callback_data='send_reminder_tomorrow')


    # builder.adjust(1,1,1) сколько кнопок вывести в ряду
    # (по одной, в трех рядах)

    return builder.as_markup()


