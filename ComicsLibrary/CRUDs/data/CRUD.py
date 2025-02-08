from abc import ABC, abstractmethod
from typing import Dict, Any

class CRUD(ABC):
    @abstractmethod
    def create(self, entity: Dict[str, Any]):
        pass

    @abstractmethod
    def read_by_id(self, entity_id: str):
        pass

    @abstractmethod
    def update(self, entity_id: str, updated_fields: Dict[str, Any]):
        pass

    @abstractmethod
    def delete(self, entity_id: str):
        pass
