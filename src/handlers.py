from src.main import bot


# Команды для студентов
@bot.message_handler(commands=['iamstudent'])
def iamstudent(message):
    pass


@bot.message_handler(commands=['lolkek'])
def lolkek(message):
    pass


# Команды для руководителей
@bot.message_handler(commands=['iamsupervisor'])
def iamsupervisor(message):
    pass


@bot.message_handler(commands=['cheburek'])
def cheburek(message):
    pass


# Обработчики нажатия на кнопки
@bot.callback_query_handler(func=lambda call: call.data == 'student')
def student_button_handler(call):
    bot.send_message(call.message.chat.id, "Ок вот команды для студентов")
    bot.add_message_handler(iamstudent)
    bot.add_message_handler(lolkek)


@bot.callback_query_handler(func=lambda call: call.data == 'supervisor')
def supervisor_button_handler(call):
    bot.send_message(call.message.chat.id, "Ок вот команды для руководителей")
    bot.add_message_handler(iamsupervisor)
    bot.add_message_handler(cheburek)
