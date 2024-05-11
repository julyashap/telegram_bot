from src.classes.abctract_db_connector import AbstractDBConnector
import psycopg2
from src.config import config
from src.classes.student import Student


class DBConnector(AbstractDBConnector):
    def __init__(self, dbname: str) -> None:
        params = config()

        self.conn = psycopg2.connect(dbname=dbname, **params)
        self.cur = self.conn.cursor()

    def get_data(self, data: str, table_name: str) -> list[tuple]:
        with self.conn:
            self.cur.execute(f"select {data} from {table_name}")
            data_from_table = self.cur.fetchall()

        return data_from_table

    def insert_student(self, student: Student) -> None:
        with self.conn:
            self.cur.execute("""insert into registrations (student_id, student_first_name, student_last_name, 
            student_patronymic, student_group, registration_date, team_id) values (%s, %s, %s, %s, %s, %s, %s)""",
                             (student.id, student.first_name, student.last_name, student.patronymic,
                              student.group, student.registration_date, student.team_id))

    def delete_student(self, student: Student) -> None:
        with self.conn:
            self.cur.execute("delete from registrations where student_id = {student.student_id}")
