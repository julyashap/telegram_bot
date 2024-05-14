from src.classes.abctract_db_connector import AbstractDBConnector

import psycopg2

from src.config import config


class DBConnector(AbstractDBConnector):
    def __init__(self, dbname: str) -> None:
        params = config()

        self.conn = psycopg2.connect(dbname=dbname, **params)
        self.cur = self.conn.cursor()

    def get_data(self, query: str) -> list[tuple]:
        with self.conn:
            self.cur.execute(query)
            data_from_table = self.cur.fetchall()

        return data_from_table

    def insert_student(self, student: dict) -> None:
        with self.conn:
            self.cur.execute("""insert into registrations (student_id, student_first_name, student_last_name, 
            student_patronymic, student_group, team_name, registration_date, selection_location, test_score, team_id) 
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (student['id'], student['first_name'],
                                                                 student['last_name'], student['patronymic'],
                                                                 student['group'], student['team_name'],
                                                                 student['registration_date'],
                                                                 student['selection_location'],
                                                                 student['test_score'], student['team_id']))

    def delete_student(self, registration_id: int) -> None:
        with self.conn:
            self.cur.execute(f"delete from registrations where registration_id = {registration_id}")

    def update_code(self, chat_id:int, supervisor_id: int) -> None:
        with self.conn:
            self.cur.execute(f"update leaders set chat_id = {chat_id} where leader_id = {supervisor_id}")
