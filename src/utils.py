from telebot import types


def create_start_markup():
    markup = types.InlineKeyboardMarkup()
    student = types.InlineKeyboardButton('Я студент', callback_data='student')
    supervisor = types.InlineKeyboardButton('Я руководитель', callback_data='supervisor')
    markup.add(student, supervisor)
    return markup
