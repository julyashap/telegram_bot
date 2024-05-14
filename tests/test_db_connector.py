import pytest
from src.classes.db_connector import DBConnector


# Фикстура для подготовки тестовой среды
@pytest.fixture
def db_connector():
    connector = DBConnector("test_db_name")  # Подставьте имя вашей тестовой базы данных
    yield connector
    connector.conn.close()  # Закрыть соединение после завершения тестов


# Тесты
def test_get_data(db_connector):
    query = "SELECT * FROM some_table"
    result = db_connector.get_data(query)
    assert isinstance(result, list)


def test_insert_student(db_connector):
    student = {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        # ... дополнительные данные студента ...
    }
    db_connector.insert_student(student)
    # Проверить, что студент был добавлен успешно


def test_delete_student(db_connector):
    registration_id = 123  # Подставьте существующий registration_id для теста
    db_connector.delete_student(registration_id)
    # Проверить, что студент был удален успешно


def test_update_code(db_connector):
    chat_id = 456  # Подставьте значение для теста
    supervisor_id = 789  # Подставьте значение для теста
    db_connector.update_code(chat_id, supervisor_id)
    # Проверить, что код был успешно обновлен
