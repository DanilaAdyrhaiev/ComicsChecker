from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def save(self, entity):
        pass

    @abstractmethod
    def find_by_id(self, entity_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def delete(self, entity):
        pass
