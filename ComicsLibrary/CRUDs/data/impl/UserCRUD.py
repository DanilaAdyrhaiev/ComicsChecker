from .EntityCRUD import EntityCRUD
from dotenv import load_dotenv
from typing import Optional, Dict, Any
import os

class UserCRUD(EntityCRUD):
    def __init__(self):
        load_dotenv()
        db_name = os.getenv('MONGO_DB_NAME', 'comics_db')
        collection_name = os.getenv('MONGO_USERS_COLLECTION', 'users')
        super().__init__(db_name, collection_name)

    def read_by_chat_id(self, user_chat_id: int) -> Optional[Dict[str, Any]]:
        self.logger.info("Reading user by chat id: {}".format(user_chat_id))
        try:
            entity = self.collection.find_one({"chat_id": user_chat_id})
            entity["_id"] = str(entity["_id"])
            self.logger.info(f"Read user by chat id: {entity}")
            return entity
        except Exception as e:
            self.logger.error("Error reading user chat id: {}".format(e))
            return None