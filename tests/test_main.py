import pytest

from src.main import handle_start, student_button_handler, student_info_handler, question_two, \
    student_data, user_states, bot, db_connector, test_score, supervisor_button_handler, supervisor_info_handler, \
    handle_cancel, cancel_handler, handle_show_commands, handle_selection_schedule, handle_help, handle_teams, \
    handle_style_reference, handle_direction_buttons, main_podval_handler, beho1ders_button_handler, \
    hip_hop_button_handler
from src.utils import team_photo_handler


def test_handle_start(mocker):
    mock_bot = mocker.Mock()
    message = mocker.Mock()
    message.chat.id = 692738947
    handle_start(mock_bot, message)
    mock_bot.send_message.assert_called_with(692738947, "Привет! Подскажи мне, кто ты?",
                                             reply_markup=mock_bot.create_start_markup.return_value)


def test_student_button_handler(mocker):
    mock_bot = mocker.Mock()
    call = mocker.Mock()
    call.message.chat.id = 692738947
    student_button_handler(mock_bot, call)
    mock_bot.send_message.assert_called_with(692738947, "Привет, студент! Назови мне своё ФИО и "
                                                        "номер группы для идентификации...")
    assert call.message.chat.id in mock_bot.user_states
    assert mock_bot.user_states[call.message.chat.id] == 'waiting_for_info_student'


def test_student_info_handler(mocker):
    mocker.patch('bot.send_message')
    mocker.patch('bot.register_next_step_handler')
    mocker.patch('db_connector_students.get_data', return_value=True)

    message = mocker.Mock()
    message.text = "Шапаева Юлия Александровна 09-112"
    message.chat.id = 692738947

    student_info_handler(message)

    assert student_data['id'] == 692738947
    assert user_states[692738947] is None
    assert bot.send_message.call_count == 3


def test_question_two(mocker):
    mocker.patch('bot.send_message')
    mocker.patch('bot.register_next_step_handler')

    message = mocker.Mock()
    message.text = 'да'

    question_two(message)

    assert test_score == 1
    assert bot.send_message.call_count == 2


def test_supervisor_button_handler(mocker):
    mocker.patch('bot.send_message')
    mocker.patch('user_states')

    call = mocker.Mock()
    call.data = 'supervisor'
    call.message.chat.id = 692738947

    supervisor_button_handler(call)

    assert bot.send_message.call_count == 1
    assert user_states[692738947] == 'waiting_for_info_supervisor'


def test_supervisor_info_handler(mocker):
    mocker.patch('bot.send_message')
    mocker.patch('db_connector.get_data')
    mocker.patch('db_connector.update_code')

    message = mocker.Mock()
    message.text = 'U852S'
    message.chat.id = 692738947

    db_connector.get_data.return_value = [(5, 'Юлия')]

    supervisor_info_handler(message)

    assert db_connector.get_data.call_count == 1
    assert db_connector.update_code.call_count == 1
    assert bot.send_message.call_count == 2
    assert user_states[692738947] is None


def test_handle_cancel(mocker):
    mocker.patch('bot.send_message')
    mocker.patch('db_connector.get_data')

    message = mocker.Mock()
    message.chat.id = 692738947

    db_connector.get_data.return_value = [(1, 'Чердак', '2024-05-15')]

    handle_cancel(message)

    assert bot.send_message.call_count == 1


def test_cancel_handler(mocker):
    mocker.patch('bot.send_message')
    mocker.patch('db_connector.get_data')
    mocker.patch('db_connector.delete_student')

    call = mocker.Mock()
    call.data = 'registration1'
    call.message.chat.id = 692738947

    db_connector.get_data.return_value = [(1, 'Шапаева', 'Юлия', 'Александровна', '09-112', 'Чердак', '2024-05-15')]

    cancel_handler(call)

    assert db_connector.delete_student.call_count == 1
    assert bot.send_message.call_count == 2


def test_hip_hop_button_handler(mocker):
    call = mocker.Mock()
    call.data = 'hip_hop_r'
    with mocker.patch('telegram.Bot.send_message') as mock_send_message:
        hip_hop_button_handler(call)
        mock_send_message.assert_called_once()


def test_beho1ders_button_handler(mocker):
    call = mocker.Mock()
    call.data = 'beho1ders_r'
    with mocker.patch('telegram.Bot.send_message') as mock_send_message:
        beho1ders_button_handler(call)
        mock_send_message.assert_called_once()


def test_team_photo_handler(mocker):
    call = mocker.Mock()
    call.data = 'beho1ders_t'
    with mocker.patch('telegram.Bot.send_photo') as mock_send_photo:
        team_photo_handler(call, 'Beho1ders', 'path/to/photo.jpg', db_connector, bot)
        mock_send_photo.assert_called_once()


def test_main_podval_handler(mocker):
    call = mocker.Mock()
    call.data = 'main_p'
    with mocker.patch('telegram.Bot.send_message') as mock_send_message:
        main_podval_handler(call)
        mock_send_message.assert_called_once()


def test_handle_direction_buttons(mocker):
    data_values = ['hip_hop_s', 'jazz_funk_s', 'dancehall_s', 'contemporary_s']
    for data_value in data_values:
        call = mocker.Mock()
        call.data = data_value
        with mocker.patch('telegram.Bot.send_message') as mock_send_message:
            handle_direction_buttons(call)
            mock_send_message.assert_called_once()


def test_handle_style_reference(mocker):
    message = mocker.Mock()
    with mocker.patch('telegram.Bot.send_message') as mock_send_message:
        handle_style_reference(message)
        mock_send_message.assert_called_once()


def test_handle_teams(mocker):
    message = mocker.Mock()
    with mocker.patch('telegram.Bot.send_message') as mock_send_message:
        handle_teams(message)
        mock_send_message.assert_called_once()


def test_handle_help(mocker):
    message = mocker.Mock()
    with mocker.patch('telegram.Bot.send_message') as mock_send_message:
        handle_help(message)
        mock_send_message.assert_called_once()


def test_handle_show_commands(mocker):
    message = mocker.Mock()
    with mocker.patch('telegram.Bot.send_message') as mock_send_message:
        handle_show_commands(message)
        mock_send_message.assert_called_once()


def test_handle_selection_schedule(mocker):
    message = mocker.Mock()
    with mocker.patch('telegram.Bot.send_message') as mock_send_message:
        handle_selection_schedule(message)
        mock_send_message.assert_called()
