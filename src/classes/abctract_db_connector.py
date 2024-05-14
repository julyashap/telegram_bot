from abc import ABC, abstractmethod


class AbstractDBConnector(ABC):
    @abstractmethod
    def __init__(self, dbname: str) -> None:
        pass

    @abstractmethod
    def get_data(self, query: str) -> list[tuple]:
        pass

    @abstractmethod
    def insert_student(self, student: dict) -> None:
        pass

    @abstractmethod
    def delete_student(self, registration_id: int) -> None:
        pass
