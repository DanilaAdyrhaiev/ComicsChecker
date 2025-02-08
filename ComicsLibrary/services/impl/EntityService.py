from ..Service import Service
from ComicsLibrary.repositories import EntityRepository
from ComicsLibrary.mappers import EntityMapper
from ComicsLibrary.DTO import EntityDTO
from typing import Optional, List
from ComicsLibrary.loggers.Logger import Logger


class EntityService(Service):
    def __init__(self, entity_repository: EntityRepository, entity_mapper: EntityMapper):
        self.repository = entity_repository
        self.mapper = entity_mapper
        self.logger = Logger.get_logger(self.__class__.__name__)

    def add(self, entity_dto: EntityDTO) -> Optional[EntityDTO]:
        self.logger.debug('Adding entity %s', entity_dto)
        entity = self.mapper.to_entity(entity_dto)
        self.logger.info("Adding entity %s to repository", entity)
        val = self.repository.save(entity)
        self.logger.info("Entity from repository %s", val)
        if val is not None:
            entity_dto = self.mapper.to_dto(val)
            self.logger.info("Entity mapped to dto %s", entity_dto)
            return entity_dto
        else:
            self.logger.error('Failed to add entity %s', entity_dto)
            return None

    def remove(self, entity_id: str) -> bool:
        pass

    def update(self, entity_dto: EntityDTO) -> Optional[EntityDTO]:
        self.logger.debug('Updating entity %s', entity_dto)
        entity = self.mapper.to_entity(entity_dto)
        self.logger.debug('Mapping from dto to entity %s', entity)
        updated_entity = self.repository.save(entity)
        if updated_entity:
            self.logger.debug('Updated entity %s', updated_entity)
            return self.mapper.to_dto(updated_entity)
        else:
            self.logger.debug("Failed to update entity %s", entity_dto)
            return None

    def get_all(self) -> List[EntityDTO]:
        self.logger.debug('Getting all entities')
        entities = self.repository.get_all()
        self.logger.debug('Entities %s', entities)
        vals = [self.mapper.to_dto(entity) for entity in entities]
        self.logger.info('Converted entities %s', vals)
        return vals

    def get_by_id(self, entity_id: str) -> Optional[EntityDTO]:
        self.logger.debug('Getting entity %s', entity_id)
        entity = self.repository.find_by_id(entity_id)
        return self.mapper.to_dto(entity) if entity else None