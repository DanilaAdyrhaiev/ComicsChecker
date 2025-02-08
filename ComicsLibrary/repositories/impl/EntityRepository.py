from astroid.modutils import logger

from ..Repository import Repository
from ComicsLibrary.entities import BaseEntity as Entity
from ComicsLibrary.CRUDs import EntityCRUD
from typing import Optional, Dict, Any, List
from ComicsLibrary.loggers.Logger import Logger


class EntityRepository(Repository):
    def __init__(self, crud: EntityCRUD):
        self.crud = crud
        self.logger = Logger.get_logger(name=self.__class__.__name__)

    def save(self, entity: Entity) -> Optional[Entity]:
        self.logger.debug(f'Saving {entity}')
        try:
            if entity._id is None:
                dict_entity = entity.to_dict()
                id = self.crud.create(dict_entity)
                if id is None:
                    self.logger.error('Failed to create entity - no id returned')
                    return None
                self.logger.debug(f'Created entity with id {id}')
                dict_entity['_id'] = str(id)
                self.logger.debug(f'Added _id {id} to dict: {dict_entity}')
                val = entity.from_dict(dict_entity)
                self.logger.debug(f'Converted from dict to entity: {val}')
                return val
            else:
                self.logger.debug(f'Updating existing entity with id {entity._id}')
                existing = self.find_by_id(entity._id)
                if existing:
                    updated_entity = self.update(entity)
                    return updated_entity
                else:
                    self.logger.warning(f'Entity with id {entity._id} not found for update')
                    return None
        except Exception as e:
            self.logger.error(f'Failed to save entity with id {entity._id}')
            return None

    def update(self, entity: Entity) -> Optional[Entity]:
        self.logger.debug(f'Updating {entity}')
        try:
            val = self.crud.update(entity._id, entity.to_dict())
            if val > 0:
                self.logger.debug(f'Successfully updated entity with id {entity._id}')
                return entity
            else:
                self.logger.warning(f'No documents were updated for entity with id {entity._id}')
                return None
        except Exception as e:
            self.logger.error(f'Failed to update entity with id {entity._id}: {str(e)}', exc_info=True)
            return None

    def find_by_id(self, entity_id) -> Optional[Dict[str, Any]]:
        self.logger.debug(f'Finding entity with id {entity_id}')
        try:
            result = self.crud.read_by_id(entity_id)
            if result is None:
                self.logger.debug(f'No entity found with id {entity_id}')
            return result
        except Exception as e:
            self.logger.error(f'Failed to find entity with id {entity_id}: {str(e)}', exc_info=True)
            return None

    def get_all(self) -> Optional[List[Entity]]:
        self.logger.debug('Getting all entities')
        try:
            results: List[Dict[str, Any]] = self.crud.read_all()
            self.logger.debug(f'Found {len(results) if results else 0} entities')
            for entity in results:
                entity['_id'] = str(entity['_id'])
            vals = [Entity.from_dict(entity) for entity in results]
            return vals
        except Exception as e:
            self.logger.error(f'Failed to get all entities: {str(e)}', exc_info=True)
            return None

    def delete(self, entity: Entity) -> int:
        self.logger.debug(f'Deleting entity with id {entity._id}')
        try:
            result = self.crud.delete(entity._id)
            if result > 0:
                self.logger.debug(f'Successfully deleted entity with id {entity._id}')
            else:
                self.logger.warning(f'No entity was deleted with id {entity._id}')
            return result
        except Exception as e:
            self.logger.error(f'Failed to delete entity with id {entity._id}: {str(e)}', exc_info=True)
            return 0