from src.classes.abstract_student import AbstractStudent


class Student(AbstractStudent):
    def __init__(self, id: int, first_name: str, last_name: str, patronymic: str,
                 group: str, registration_date: str, team_id: int):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.patronymic = patronymic
        self.group = group
        self.registration_date = registration_date
        self.team_id = team_id
