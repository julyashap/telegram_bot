from abc import ABC, abstractmethod
from src.classes.student import Student


class AbstractDBConnector(ABC):
    @abstractmethod
    def __init__(self, dbname: str) -> None:
        pass

    @abstractmethod
    def get_data(self, data: str, table_name: str) -> list[tuple]:
        pass

    @abstractmethod
    def insert_student(self, student: Student) -> None:
        pass

    @abstractmethod
    def delete_student(self, student: Student) -> None:
        pass
