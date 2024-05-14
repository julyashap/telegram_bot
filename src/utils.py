from telebot import types


def create_start_markup():
    markup = types.InlineKeyboardMarkup()
    student = types.InlineKeyboardButton('Я студент', callback_data='student')
    supervisor = types.InlineKeyboardButton('Я руководитель', callback_data='supervisor')
    markup.add(student, supervisor)
    return markup


def create_registration_markup():
    markup = types.InlineKeyboardMarkup()
    hip_hop = types.InlineKeyboardButton('Хип-хоп', callback_data='hip_hop_r')
    jazz_funk = types.InlineKeyboardButton('Джаз-фанк', callback_data='jazz_funk_r')
    dancehall = types.InlineKeyboardButton('Дэнсхолл', callback_data='dancehall_r')
    contemporary = types.InlineKeyboardButton('Контемпорари', callback_data='contemporary_r')
    markup.add(hip_hop, jazz_funk, dancehall, contemporary)
    return markup


def create_style_reference_markup():
    markup = types.InlineKeyboardMarkup()
    hip_hop = types.InlineKeyboardButton('Хип-хоп', callback_data='hip_hop_s')
    jazz_funk = types.InlineKeyboardButton('Джаз-фанк', callback_data='jazz_funk_s')
    dancehall = types.InlineKeyboardButton('Дэнсхолл', callback_data='dancehall_s')
    contemporary = types.InlineKeyboardButton('Контемпорари', callback_data='contemporary_s')
    markup.add(hip_hop, jazz_funk, dancehall, contemporary)
    return markup


def create_hip_hop_markup():
    markup = types.InlineKeyboardMarkup()
    beho1ders = types.InlineKeyboardButton('Beho1ders', callback_data='beho1ders_r')
    raslabon = types.InlineKeyboardButton('RA\'s Lab.On', callback_data='raslabon_r')
    markup.add(beho1ders, raslabon)
    return markup


def create_contemporary_markup():
    markup = types.InlineKeyboardMarkup()
    cherdak = types.InlineKeyboardButton('Чердак', callback_data='cherdak_r')
    podval = types.InlineKeyboardButton('Подвал', callback_data='podval_r')
    markup.add(cherdak, podval)
    return markup


def create_teams_markup():
    markup = types.InlineKeyboardMarkup()
    beho1ders = types.InlineKeyboardButton('Beho1ders', callback_data='beho1ders_t')
    raslabon = types.InlineKeyboardButton('RA\'s Lab.On', callback_data='raslabon_t')
    cherdak = types.InlineKeyboardButton('Чердак', callback_data='cherdak_t')
    podval = types.InlineKeyboardButton('Подвал', callback_data='podval_t')
    markup.add(beho1ders, raslabon, cherdak, podval)
    return markup


def create_beho1ders_dates_markup():
    markup = types.InlineKeyboardMarkup()
    main = types.InlineKeyboardButton('Основной день', callback_data='main_b')
    reserve = types.InlineKeyboardButton('Резервный день', callback_data='reserve_b')
    markup.add(main, reserve)
    return markup


def create_cherdak_dates_markup():
    markup = types.InlineKeyboardMarkup()
    main = types.InlineKeyboardButton('Основной день', callback_data='main_c')
    reserve = types.InlineKeyboardButton('Резервный день', callback_data='reserve_c')
    markup.add(main, reserve)
    return markup


def create_podval_dates_markup():
    markup = types.InlineKeyboardMarkup()
    main = types.InlineKeyboardButton('Основной день', callback_data='main_p')
    reserve = types.InlineKeyboardButton('Резервный день', callback_data='reserve_p')
    markup.add(main, reserve)
    return markup


def create_raslabon_dates_markup():
    markup = types.InlineKeyboardMarkup()
    main = types.InlineKeyboardButton('Основной день', callback_data='main_r')
    reserve = types.InlineKeyboardButton('Резервный день', callback_data='reserve_r')
    markup.add(main, reserve)
    return markup


def team_button_handler(call, team_name, create_markup_func, db_connector, bot):
    markup = create_markup_func()
    team_data = db_connector.get_data(f"select distinct team_name, team_description, main_selection, "
                                      f"reserve_selection, selection_location "
                                      f"from teams where team_name = '{team_name}'")
    bot.send_message(call.message.chat.id, f"Название коллектива: <b>{team_data[0][0]}</b>\n\n{team_data[0][1]}\n\n"
                                           f"<b>Основной</b> день отбора: <b>{str(team_data[0][2])[:-3]}</b>\n"
                                           f"<b>Резервный</b> день: <b>{str(team_data[0][3])[:-3]}</b>\n\n"
                                           f"<b>Место проведения:</b> {team_data[0][4]}",
                     reply_markup=markup, parse_mode='html')


def selection_handler(call, team_name, selection_type, db_connector, student_data, bot):
    team_data = db_connector.get_data(f"select team_name, {selection_type}, selection_location, team_id from teams "
                                      f"where team_name = '{team_name}'")
    student_data['team_name'] = team_data[0][0]
    student_data['registration_date'] = team_data[0][1]
    student_data['selection_location'] = team_data[0][2]
    student_data['team_id'] = team_data[0][3]
    db_connector.insert_student(student_data)
    bot.send_message(call.message.chat.id, 'Отлично! Ты записан на отбор! 🥰\n\n<b>P.S. Не забудь взять на отбор '
                                           'тренировочную форму и водичку!</b>', parse_mode='html')
    leader_chat_id = db_connector.get_data(f"select chat_id from leaders join teams using(leader_id) "
                                           f"where team_name = '{team_name}'")[0][0]
    bot.send_message(leader_chat_id, f"<b>Запись</b>\n\n{student_data['last_name']} {student_data['first_name']} "
                                     f"{student_data['patronymic']} {student_data['group']}\n"
                                     f"{student_data['team_name']}  |  {str(student_data['registration_date'])[:-3]}\n"
                                     f"Результаты теста: {student_data['test_score']}/5", parse_mode='html')


def direction_button_handler(call, direction_name, db_connector, bot):
    direction_data = db_connector.get_data(f"select direction_name, direction_description, direction_example "
                                           f"from directions where direction_name = '{direction_name}'")
    bot.send_message(call.message.chat.id, f"Выбранный стиль: <b>{direction_data[0][0]}</b>"
                                           f"\n\n{direction_data[0][1]}\n\n"
                                           f"Видео для понимания стиля: {direction_data[0][2]}", parse_mode='html')


def team_photo_handler(call, team_name, image_path, db_connector, bot):
    team_data = db_connector.get_data(f"select distinct team_name, team_description "
                                      f"from teams where team_name = '{team_name}'")
    photo = open(image_path, 'rb')
    caption = f"Название коллектива: <b>{team_data[0][0]}</b>\n\n{team_data[0][1]}"
    bot.send_photo(call.message.chat.id, photo, caption=caption, parse_mode='html')
