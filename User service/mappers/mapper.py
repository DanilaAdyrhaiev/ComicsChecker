from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Dict

TEntity = TypeVar("TEntity")
TDTO = TypeVar("TDTO")


class Mapper(ABC, Generic[TEntity, TDTO]):
    @abstractmethod
    def to_dto(self, entity: TEntity) -> TDTO:
        pass

    @abstractmethod
    def to_entity(self, dto: TDTO) -> TEntity:
        pass