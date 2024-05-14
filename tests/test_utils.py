import pytest

from src.utils import *

from unittest.mock import MagicMock

import os.path


def test_create_start_markup():
    markup = create_start_markup()
    student = markup.keyboard[0][0]
    supervisor = markup.keyboard[0][1]
    assert student.text == 'Я студент'
    assert supervisor.text == 'Я руководитель'


def test_create_registration_markup():
    markup = create_registration_markup()
    hip_hop_r = markup.keyboard[0][0]
    jazz_funk_r = markup.keyboard[0][1]
    dancehall_r = markup.keyboard[0][2]
    contemporary_r = markup.keyboard[1][0]
    assert hip_hop_r.text == 'Хип-хоп'
    assert jazz_funk_r.text == 'Джаз-фанк'
    assert dancehall_r.text == 'Дэнсхолл'
    assert contemporary_r.text == 'Контемпорари'


def test_create_style_reference_markup():
    markup = create_style_reference_markup()
    hip_hop_s = markup.keyboard[0][0]
    jazz_funk_s = markup.keyboard[0][1]
    dancehall_s = markup.keyboard[0][2]
    contemporary_s = markup.keyboard[1][0]
    assert hip_hop_s.text == 'Хип-хоп'
    assert jazz_funk_s.text == 'Джаз-фанк'
    assert dancehall_s.text == 'Дэнсхолл'
    assert contemporary_s.text == 'Контемпорари'


def test_create_hip_hop_markup():
    markup = create_hip_hop_markup()
    beho1ders = markup.keyboard[0][0]
    raslabon = markup.keyboard[0][1]
    assert beho1ders.text == 'Beho1ders'
    assert raslabon.text == 'RA\'s Lab.On'


def create_contemporary_markup():
    markup = create_contemporary_markup()
    assert markup.inline_keyboard[0][0].text == 'Чердак'
    assert markup.inline_keyboard[0][1].text == 'Подвал'


def create_teams_markup():
    markup = create_teams_markup()
    assert markup.inline_keyboard[0][0].text == 'Beho1ders'
    assert markup.inline_keyboard[0][1].text == 'RA\'s Lab.On'
    assert markup.inline_keyboard[0][2].text == 'Чердак'
    assert markup.inline_keyboard[0][3].text == 'Подвал'


def create_beho1ders_dates_markup():
    markup = create_beho1ders_dates_markup()
    assert markup.inline_keyboard[0][0].text == 'Основной день'
    assert markup.inline_keyboard[0][1].text == 'Резервный день'


def create_cherdak_dates_markup():
    markup = create_cherdak_dates_markup()
    assert markup.inline_keyboard[0][0].text == 'Основной день'
    assert markup.inline_keyboard[0][1].text == 'Резервный день'


def create_podval_dates_markup():
    markup = create_podval_dates_markup()
    assert markup.inline_keyboard[0][0].text == 'Основной день'
    assert markup.inline_keyboard[0][1].text == 'Резервный день'


def create_raslabon_dates_markup():
    markup = create_raslabon_dates_markup()
    assert markup.inline_keyboard[0][0].text == 'Основной день'
    assert markup.inline_keyboard[0][1].text == 'Резервный день'


@pytest.fixture
def mock_db_connector():
    return MagicMock()


@pytest.fixture
def mock_bot():
    return MagicMock()


def test_team_button_handler(mock_db_connector, mock_bot):
    mock_markup = MagicMock()
    mock_db_connector.get_data.return_value = [('Чердак', 'Чердак - коллектив современного танца!',
                                                '2024-05-15 19:00:00', '2024-10-05 19:30:00',
                                                'УНИКС, спортивный блок: Центр Карпова')]
    create_markup_func = MagicMock(return_value=mock_markup)

    call = MagicMock()
    team_button_handler(call, 'Чердак', create_markup_func, mock_db_connector, mock_bot)

    mock_bot.send_message.assert_called_once()


def test_selection_handler(mock_db_connector, mock_bot):
    mock_data = [('Чердак', '2024-05-15 19:00:00', 'УНИКС, спортивный блок: Центр Карпова', 1)]
    mock_db_connector.get_data.return_value = mock_data

    call = MagicMock()
    student_data = {'last_name': 'Шапаева', 'first_name': 'Юлия', 'patronymic': 'Александровна',
                    'group': '09-112', 'test_score': 4}
    selection_type = 'main_selection'
    selection_handler(call, 'Чердак', selection_type, mock_db_connector, student_data, mock_bot)

    mock_db_connector.insert_student.assert_called_once()
    mock_bot.send_message.assert_called()


def test_direction_button_handler(mock_db_connector, mock_bot):
    mock_data = [('Контемпорари', 'Современный стиль танца!', 'https://example.com/video')]
    mock_db_connector.get_data.return_value = mock_data

    call = MagicMock()
    direction_button_handler(call, 'Контемпорари', mock_db_connector, mock_bot)

    mock_bot.send_message.assert_called_once()


def test_team_photo_handler(mock_db_connector, mock_bot):
    mock_data = [('Чердак', 'Чердак - коллектив современного танца!')]
    mock_db_connector.get_data.return_value = mock_data

    call = MagicMock()
    team_name = 'Чердак'
    image_path = os.path.join('..', 'assets', 'cherdak.jpg')
    team_photo_handler(call, team_name, image_path, mock_db_connector, mock_bot)

    mock_bot.send_photo.assert_called_once()
