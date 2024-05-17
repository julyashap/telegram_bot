import pytest
from src.classes.db_connector import DBConnector


@pytest.fixture
def db_connector():
    connector = DBConnector("dance_icmit")
    yield connector
    connector.conn.close()


def test_get_data(db_connector):
    query = "select distinct team_name from teams"
    results = db_connector.get_data(query)

    assert isinstance(results, list)

    for result in results:
        assert isinstance(result, tuple)


def test_insert_student(db_connector):
    student = {
        "id": 123,
        "first_name": "Юлия",
        "last_name": "Шапаева",
        "patronymic": "Александровна",
        "group": "09-112",
        "team_name": "Чердак",
        "registration_date": "2024-05-15 19:00:00",
        "selection_location": "УНИКС, спортивный блок: Центр Карпова",
        "test_score": 4,
        "team_id": 1
    }
    db_connector.insert_student(student)

    student_ids = [student_id[0] for student_id in db_connector.get_data('select student_id from registrations')]

    assert str(student['id']) in student_ids


def test_delete_student(db_connector):
    registration_id = 1
    db_connector.delete_student(registration_id)

    data = db_connector.get_data(f'select * from registrations where registration_id = {registration_id}')

    assert str(data) == '[]'


def test_update_code(db_connector):
    chat_id = 456
    supervisor_id = 1
    db_connector.update_code(chat_id, supervisor_id)

    data = db_connector.get_data(f'select chat_id from leaders where leader_id = {supervisor_id}')[0][0]

    assert data == str(chat_id)
