from ..Entity import Entity
from dataclasses import dataclass


@dataclass
class BaseEntity(Entity):
    _id: str = None

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, _id: str):
        self._id = _id

    def to_dict(self):
        return {
            '_id': self._id
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            _id=data['_id'],
        )