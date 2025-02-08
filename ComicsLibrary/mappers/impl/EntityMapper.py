from typing import TypeVar, Generic
from ..Mapper import Mapper
from ComicsLibrary.entities import BaseEntity as Entity
from ComicsLibrary.DTO import EntityDTO

TEntity = TypeVar("TEntity", bound=Entity)
TDTO = TypeVar("TDTO", bound=EntityDTO)


class EntityMapper(Mapper[Entity, EntityDTO], Generic[TEntity, TDTO]):
    def to_dto(self, entity: Entity) -> EntityDTO:
        return EntityDTO()

    def to_entity(self, dto: EntityDTO) -> Entity:
        return Entity()
