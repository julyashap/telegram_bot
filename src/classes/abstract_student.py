from abc import ABC, abstractmethod


class AbstractStudent(ABC):
    @abstractmethod
    def __init__(self, id: int, first_name: str, last_name: str, patronymic: str,
                 group: str, registration_date: str, team_id: int):
        pass
