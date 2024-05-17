import telebot
from telebot import types

from src.config import TOKEN_FOR_DANCE_BOT

from src.utils import create_start_markup, create_registration_markup, create_style_reference_markup, \
    create_hip_hop_markup, create_contemporary_markup, create_teams_markup, create_beho1ders_dates_markup, \
    create_cherdak_dates_markup, create_podval_dates_markup, create_raslabon_dates_markup, \
    team_button_handler, selection_handler, direction_button_handler, team_photo_handler

from src.classes.db_connector import DBConnector

import os.path


# экземпляр бота
bot = telebot.TeleBot(TOKEN_FOR_DANCE_BOT)

# состояние для отслеживания статуса пользователя
user_states = {}

# данные о пользователе
student_data = {}

# соединение с БД
db_connector = DBConnector('dance_icmit')
db_connector_students = DBConnector('students_icmit')

# результаты теста
test_score = 0


@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = create_start_markup()
    bot.send_message(message.chat.id, "Привет! Подскажи мне, кто ты?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'student')
def student_button_handler(call):
    bot.send_message(call.message.chat.id, "Привет, студент! Назови мне своё ФИО и номер группы для идентификации...")
    user_states[call.message.chat.id] = 'waiting_for_info_student'


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_info_student')
def student_info_handler(message):
    student_info = message.text.split()

    if len(student_info) != 4:
        bot.send_message(message.chat.id, "Попробуй еще раз!")
    else:
        last_name = student_info[0]
        first_name = student_info[1]
        patronymic = student_info[2]
        group = student_info[3]

        student_in_database = db_connector_students.get_data(f'select * from students where student_first_name '
                                                      f'= \'{first_name}\' and '
                                                      f'student_last_name = \'{last_name}\' and '
                                                      f'student_patronymic = \'{patronymic}\' '
                                                      f'and student_group = \'{group}\'')

        if student_in_database:
            student_data['id'] = str(message.chat.id)
            student_data['last_name'] = last_name
            student_data['first_name'] = first_name
            student_data['patronymic'] = patronymic
            student_data['group'] = group

            bot.send_message(message.chat.id, "Спасибо! А теперь давай пройдем тест! 💃\n\n"
                                              "P.S. Отвечай просто: 'да' или 'нет'")
            bot.send_message(message.chat.id, "Вопрос 1: Занимался ли ты танцами до этого?")
            bot.register_next_step_handler(message, question_two)

            user_states[message.chat.id] = None  # сброс состояния пользователя
        else:
            bot.send_message(message.chat.id, "К сожалению, тебя нет в базе данных 😢")


def question_two(message):
    global test_score

    if message.text.lower().strip() == 'да':
        test_score += 1

    bot.send_message(message.chat.id, "Вопрос 2: Стесняешься ли ты танцевать перед людьми?")
    bot.register_next_step_handler(message, question_three)


def question_three(message):
    global test_score

    if message.text.lower().strip() == 'нет':
        test_score += 1

    bot.send_message(message.chat.id, "Вопрос 3: Ты когда нибудь участвовал в танцевальных конкурсах или посещал их?")
    bot.register_next_step_handler(message, question_four)


def question_four(message):
    global test_score

    if message.text.lower().strip() == 'да':
        test_score += 1

    bot.send_message(message.chat.id, "Вопрос 4: Ты занимался каким-нибудь видом спорта?")
    bot.register_next_step_handler(message, question_five)


def question_five(message):
    global test_score

    if message.text.lower().strip() == 'да':
        test_score += 1

    bot.send_message(message.chat.id, "Вопрос 5: Готов ли ты выучить новый танцевальный стиль?")
    bot.register_next_step_handler(message, final_score)


def final_score(message):
    global test_score

    if message.text.lower().strip() == 'да':
        test_score += 1

    student_data['test_score'] = test_score

    bot.send_message(message.chat.id, "Отлично! Ты всё прошел! 🥳")

    bot.send_message(message.chat.id, "<b>Список команд бота</b>\n\n/registration: зарегистрироваться на отбор\n"
                                      "/selections: список твоих отборов\n"
                                      "/cancel: отмена регистрации\n/styleReference: узнать больше о стилях танцев\n"
                                      "/teams: узнать больше о танцевальных коллективах\n"
                                      "/otherStudents: посмотреть других участников потока\n"
                                      "/question: задать вопрос руководителю\n/help: справка по командам бота",
                     parse_mode='html')


@bot.callback_query_handler(func=lambda call: call.data == 'supervisor')
def supervisor_button_handler(call):
    bot.send_message(call.message.chat.id, "Напиши свой пароль...")
    user_states[call.message.chat.id] = 'waiting_for_info_supervisor'


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_info_supervisor')
def supervisor_info_handler(message):
    supervisor_info = message.text

    leader_info = db_connector.get_data(f'select leader_id, leader_first_name '
                                         f'from leaders where leader_code = \'{supervisor_info}\'')

    if leader_info:
        db_connector.update_code(str(message.chat.id), leader_info[0][0])
        bot.send_message(message.chat.id, f"Отлично, {leader_info[0][1]}! Верификация пройдена! 💃")

        bot.send_message(message.chat.id, "<b>Список команд бота</b>\n\n"
                                          "/selectionSchedule: информация о расписании отборов\n"
                                          "/listStudents: информация о записях на отборы\n"
                                          "/showCommands: справка по командам бота\n", parse_mode='html')

        user_states[message.chat.id] = None
    else:
        bot.send_message(message.chat.id, "К сожалению, тебя нет в базе данных 😢")


@bot.message_handler(commands=['registration'])
def handle_registration(message):
    markup = create_registration_markup()
    bot.send_message(message.chat.id, "Время <b>регистрации</b>! Выбери направление танцев! 🤩\n\n"
                                      "P.S. Для справки по стилям танцев набери команду: /styleReference",
                     reply_markup=markup, parse_mode='html')


@bot.callback_query_handler(func=lambda call: call.data == 'hip_hop_r')
def hip_hop_button_handler(call):
    markup = create_hip_hop_markup()
    bot.send_message(call.message.chat.id, "Выбери коллектив:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'contemporary_r')
def contemporary_button_handler(call):
    markup = create_contemporary_markup()
    bot.send_message(call.message.chat.id, "Выбери коллектив:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'beho1ders_r')
def beho1ders_button_handler(call):
    team_button_handler(call, 'Beho1ders', create_beho1ders_dates_markup, db_connector, bot)


@bot.callback_query_handler(func=lambda call: call.data == 'cherdak_r')
def cherdak_button_handler(call):
    team_button_handler(call, 'Чердак', create_cherdak_dates_markup, db_connector, bot)


@bot.callback_query_handler(func=lambda call: call.data == 'podval_r')
def podval_button_handler(call):
    team_button_handler(call, 'Подвал', create_podval_dates_markup, db_connector, bot)


@bot.callback_query_handler(func=lambda call: call.data in ['jazz_funk_r', 'dancehall_r', 'raslabon_r'])
def raslabon_button_handler(call):
    team_button_handler(call, 'RA`s Lab.On', create_raslabon_dates_markup, db_connector, bot)


@bot.callback_query_handler(func=lambda call: call.data == 'beho1ders_t')
def beho1ders_button_handler(call):
    team_photo_handler(call, 'Beho1ders', os.path.join('..', 'assets', 'beho1ders.jpg'), db_connector, bot)


@bot.callback_query_handler(func=lambda call: call.data == 'cherdak_t')
def cherdak_button_handler(call):
    team_photo_handler(call, 'Чердак', os.path.join('..', 'assets', 'cherdak.jpg'), db_connector, bot)


@bot.callback_query_handler(func=lambda call: call.data == 'podval_t')
def podval_button_handler(call):
    team_photo_handler(call, 'Подвал', os.path.join('..', 'assets', 'podval.jpg'), db_connector, bot)


@bot.callback_query_handler(func=lambda call: call.data == 'raslabon_t')
def raslabon_button_handler(call):
    team_photo_handler(call, 'RA`s Lab.On', os.path.join('..', 'assets', 'raslabon.jpg'), db_connector, bot)


@bot.callback_query_handler(func=lambda call: call.data == 'main_p')
def main_podval_handler(call):
    selection_handler(call, 'Подвал', 'main_selection', db_connector, student_data, bot)


@bot.callback_query_handler(func=lambda call: call.data == 'reserve_p')
def reserve_podval_handler(call):
    selection_handler(call, 'Подвал', 'reserve_selection', db_connector, student_data, bot)


@bot.callback_query_handler(func=lambda call: call.data == 'main_b')
def main_beho1ders_handler(call):
    selection_handler(call, 'Beho1ders', 'main_selection', db_connector, student_data, bot)


@bot.callback_query_handler(func=lambda call: call.data == 'reserve_b')
def reserve_beho1ders_handler(call):
    selection_handler(call, 'Beho1ders', 'reserve_selection', db_connector, student_data, bot)


@bot.callback_query_handler(func=lambda call: call.data == 'main_r')
def main_beho1ders_handler(call):
    selection_handler(call, 'RA`s Lab.On', 'main_selection', db_connector, student_data, bot)


@bot.callback_query_handler(func=lambda call: call.data == 'reserve_r')
def reserve_beho1ders_handler(call):
    selection_handler(call, 'RA`s Lab.On', 'reserve_selection', db_connector, student_data, bot)


@bot.callback_query_handler(func=lambda call: call.data == 'main_c')
def main_beho1ders_handler(call):
    selection_handler(call, 'Чердак', 'main_selection', db_connector, student_data, bot)


@bot.callback_query_handler(func=lambda call: call.data == 'reserve_c')
def reserve_beho1ders_handler(call):
    selection_handler(call, 'Чердак', 'reserve_selection', db_connector, student_data, bot)


@bot.callback_query_handler(func=lambda call: call.data in
                                              ['hip_hop_s', 'jazz_funk_s', 'dancehall_s', 'contemporary_s'])
def handle_direction_buttons(call):
    if call.data == 'hip_hop_s':
        direction_button_handler(call, 'Хип-хоп', db_connector, bot)
    elif call.data == 'jazz_funk_s':
        direction_button_handler(call, 'Джаз-фанк', db_connector, bot)
    elif call.data == 'dancehall_s':
        direction_button_handler(call, 'Дэнсхолл', db_connector, bot)
    elif call.data == 'contemporary_s':
        direction_button_handler(call, 'Контемпорари', db_connector, bot)


@bot.message_handler(commands=['styleReference'])
def handle_style_reference(message):
    markup = create_style_reference_markup()
    bot.send_message(message.chat.id, "Выбери направление, по которому хочешь узнать чуть больше:",
                     reply_markup=markup)


@bot.message_handler(commands=['teams'])
def handle_teams(message):
    markup = create_teams_markup()
    bot.send_message(message.chat.id, "Выбери коллектив, о котором хочешь узнать чуть больше:",
                     reply_markup=markup)


@bot.message_handler(commands=['cancel'])
def handle_cancel(message):
    registrations_data = db_connector.get_data(f'select registration_id, team_name, registration_date '
                                               f'from registrations where student_id = \'{message.chat.id}\'')

    if registrations_data:
        markup = types.InlineKeyboardMarkup()

        for registration_data in registrations_data:
            registration = types.InlineKeyboardButton(f'{registration_data[1]} {str(registration_data[2])[:-3]}',
                                                      callback_data=f'registration{registration_data[0]}')
            markup.add(registration)

        bot.send_message(message.chat.id, "Выбери запись, которую хочешь отменить: ", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Упс! У тебя нет записей 😢")


@bot.callback_query_handler(func=lambda call: call.data[:len('registration')] == 'registration')
def cancel_handler(call):
    registrations_data = db_connector.get_data(f'select registration_id, student_last_name, '
                                               f'student_first_name, student_patronymic, student_group, '
                                               f'team_name, registration_date from registrations '
                                               f'where student_id = \'{call.message.chat.id}\'')

    for registration_data in registrations_data:
        if str(registration_data[0]) == call.data[len('registration'):]:
            db_connector.delete_student(registration_data[0])
            bot.send_message(call.message.chat.id, 'Готово! Отменили твою запись! 😉')

            leader_chat_id = str(db_connector.get_data(f'select chat_id from leaders join teams using(leader_id) '
                                                   f'where team_name = \'{registration_data[5]}\'')[0][0])
            bot.send_message(leader_chat_id, f"<b>Отмена записи</b>\n\n{registration_data[1]} {registration_data[2]} "
                                             f"{registration_data[3]} {registration_data[4]}\n"
                                             f"{registration_data[5]} {str(registration_data[6])[:-3]}",
                             parse_mode='html')
            break


@bot.message_handler(commands=['otherStudents'])
def hanle_other_students(message):
    student_parameters = db_connector.get_data(f'select team_name, registration_date '
                                               f'from registrations where student_id = \'{message.chat.id}\'')
    other_students = ""
    for student_parameter in student_parameters:
        other_students_info = db_connector.get_data(f'select student_first_name, student_last_name, student_group, '
                                                    f'team_name, registration_date from registrations where '
                                                    f'student_id <> \'{message.chat.id}\' and team_name = '
                                                    f'\'{student_parameter[0]}\' and registration_date = '
                                                    f'\'{student_parameter[1]}\'')

        for other_student_info in other_students_info:
            other_students += f"{other_student_info[1]} {other_student_info[0]} {other_student_info[2]}, " \
                              f"{other_student_info[3]}: {str(other_student_info[4])[:-3]}\n"

    if other_students:
        bot.send_message(message.chat.id, f"<b>Список участников</b>\n\n{other_students}", parse_mode='html')
    else:
        bot.send_message(message.chat.id, "С тобой пока никого нет 😢")


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "<b>Список команд бота</b>\n\n/registration: зарегистрироваться на отбор\n"
                                      "/selections: список твоих отборов\n"
                                      "/cancel: отмена регистрации\n/styleReference: узнать больше о стилях танцев\n"
                                      "/teams: узнать больше о танцевальных коллективах\n"
                                      "/otherStudents: посмотреть других участников потока\n"
                                      "/question: задать вопрос руководителю\n/help: справка по командам бота",
                     parse_mode='html')


@bot.message_handler(commands=['question'])
def handle_question(message):
    leaders_data = db_connector.get_data(f'select distinct team_name, leader_tg '
                                         f'from teams join leaders using(leader_id)')

    data_to_send = ""
    for leader_data in leaders_data:
        data_to_send += f"{leader_data[0]}: {leader_data[1]}\n"

    bot.send_message(message.chat.id, f"Если у тебя появился вопрос, ты можешь написать его\n"
                                      f"✨<b>руководителям</b>✨\n\n"
                                      f"{data_to_send}", parse_mode='html')


@bot.message_handler(commands=['selections'])
def handle_selections(message):
    selections = db_connector.get_data(f'select distinct team_name, registration_date, selection_location '
                                       f'from registrations '
                                       f'where student_id = \'{message.chat.id}\'')

    if selections:
        selections_info = ""

        for selection in selections:
            selections_info += f"{selection[0]}: {str(selection[1])[:-3]}\nМесто проведения: {selection[2]}\n\n"

        bot.send_message(message.chat.id, f"<b>Список твоих отборов</b>\n\n{selections_info}\n\n", parse_mode='html')
        bot.send_message(message.chat.id, "<b>Не забудь взять с собой тренировочную форму и водичку!</b>",
                         parse_mode='html')
    else:
        bot.send_message(message.chat.id, "Но ведь у тебя нет записей на отборы 😢")


@bot.message_handler(commands=['showCommands'])
def handle_show_commands(message):
    bot.send_message(message.chat.id, "<b>Список команд бота</b>\n\n"
                                      "/selectionSchedule: информация о расписании отборов\n"
                                      "/listStudents: информация о записях на отборы\n"
                                      "/showCommands: справка по командам бота\n", parse_mode='html')


@bot.message_handler(commands=['selectionSchedule'])
def handle_selection_schedule(message):
    selections_data = db_connector.get_data(f'select distinct team_name, main_selection, reserve_selection from teams '
                                            f'join leaders using(leader_id) where chat_id = \'{message.chat.id}\'')

    if selections_data:
        selection_schedule = "<b>Расписание отборов</b>\n\n"

        for selection_data in selections_data:
            selection_schedule += f"{selection_data[0]}: {str(selection_data[1])[:-3]}\n" \
                                  f"{selection_data[0]}: {str(selection_data[2])[:-3]}\n"

        bot.send_message(message.chat.id, selection_schedule, parse_mode='html')
    else:
        bot.send_message(message.chat.id, "Похоже у тебя нет отборов 😢")


@bot.message_handler(commands=['listStudents'])
def handle_list_students(message):
    selections_data = db_connector.get_data(f'select distinct team_name from teams '
                                            f'join leaders using(leader_id) where chat_id = \'{message.chat.id}\'')

    if selections_data:
        markup = types.InlineKeyboardMarkup()

        for selection_data in selections_data:
            selection = types.InlineKeyboardButton(f'{selection_data[0]}',
                                                   callback_data=f'selection_{selection_data[0]}')
            markup.add(selection)

        bot.send_message(message.chat.id, "Выбери отбор, список участников которого хочешь увидеть:",
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Похоже у тебя нет отборов 😢")


@bot.callback_query_handler(func=lambda call: call.data[:len('selection')] == 'selection')
def list_students_handler(call):
    students_in_selection = db_connector.get_data(f'select student_first_name, student_last_name, '
                                                  f'student_patronymic, student_group, r.team_name, '
                                                  f'registration_date, test_score '
                                                  f'from registrations r join teams using(team_id) '
                                                  f'join leaders using(leader_id) '
                                                  f'where chat_id = \'{call.message.chat.id}\'')

    list_students = ""

    for student_in_selection in students_in_selection:
        if str(student_in_selection[4]) == call.data[len('selection_'):]:
            list_students += f"{student_in_selection[1]} {student_in_selection[0]} {student_in_selection[2]} " \
                             f"{student_in_selection[3]}:\n{str(student_in_selection[5])[:-3]}, " \
                             f"тест: {student_in_selection[6]}/5\n\n"

    if list_students:
        bot.send_message(call.message.chat.id, f"<b>Список участников</b>\n\n{list_students}", parse_mode='html')
    else:
        bot.send_message(call.message.chat.id, "Похоже на этот отбор пока никто не записался 😢")


@bot.message_handler(func=lambda message: "спасибо" in message.text.lower())
def thank_you_handler(message):
    bot.send_message(message.chat.id, "Всегда пожалуйста!")


# запуск бота
bot.polling(none_stop=True, interval=0)

db_connector.cur.close()
db_connector.conn.close()
