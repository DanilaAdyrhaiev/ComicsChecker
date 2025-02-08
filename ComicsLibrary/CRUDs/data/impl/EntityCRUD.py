from ..CRUD import CRUD
from pymongo import MongoClient
from bson import ObjectId
from typing import Dict, Optional, List, Any
from dotenv import load_dotenv
import os
from ComicsLibrary.loggers.Logger import Logger


class EntityCRUD(CRUD):
    def __init__(self, db_name: str = None,
                 collection_name: str = None):
        self.logger = Logger.get_logger(name=self.__class__.__name__)
        load_dotenv()
        mongo_uri = os.getenv('MONGO_URI')
        if not mongo_uri:
            raise ValueError("MONGO_URI environment variable is not set")
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create(self, entity: Dict[str, Any]) -> Optional[ObjectId]:
        self.logger.info(f"Creating entity {entity}")
        try:
            result = self.collection.insert_one(entity)
            inserted_id = result.inserted_id
            self.logger.info(f"Successfully created entity with id: {inserted_id}")
            self.logger.info(f"Entity {entity}")
            return inserted_id
        except Exception as e:
            self.logger.error(f"Failed to create entity {entity}: {str(e)}", exc_info=True)
            return None
    
    def read_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        self.logger.info(f"Reading entity with id: {entity_id}")
        try:
            if isinstance(entity_id, str):
                try:
                    entity_id = ObjectId(entity_id)
                except Exception as e:
                    self.logger.error(f"Invalid ObjectId format: {entity_id}")
                    return None

            entity = self.collection.find_one({"_id": entity_id})
            if entity:
                self.logger.info(f"Successfully read entity with id: {entity_id}")
            else:
                self.logger.debug(f"No entity found with id: {entity_id}")
            return entity

        except Exception as e:
            self.logger.error(f"Failed to read entity with id {entity_id}: {str(e)}", exc_info=True)
            return None
    
    def read_all(self) -> List[Dict[str, Any]]:
        self.logger.info(f"Reading all entities")
        try:
            vals = self.collection.find()
            self.logger.info(f"Entities read")
            return list(vals)
        except Exception as e:
            self.logger.error(f"Failed to read entities: {e}")
            return None

    def update(self, entity_id: str, updated_fields: Dict[str, Any]) -> int:
        self.logger.info(f"Updating entity {entity_id}")
        try:
            if isinstance(entity_id, str):
                entity_id = ObjectId(entity_id)
            result = self.collection.update_one(
                {"_id": entity_id},
                {"$set": updated_fields}
            )
            return result.modified_count
        except Exception as e:
            self.logger.error(f"Failed to update entity {entity_id}: {e}")
            return 0

    def delete(self, entity_id: str) -> int:
        self.logger.info(f"Deleting entity {entity_id}")
        try:
            if isinstance(entity_id, str):
                entity_id = ObjectId(entity_id)
            result = self.collection.delete_one({"_id": entity_id})
            self.logger.info(f"Entity {entity_id} deleted")
            return result.deleted_count
        except Exception as e:
            self.logger.error(f"Failed to delete entity {entity_id}: {e}")
            return 0