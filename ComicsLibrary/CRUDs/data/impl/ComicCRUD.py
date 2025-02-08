from .EntityCRUD import EntityCRUD
from dotenv import load_dotenv
import os
from typing import Optional, Dict, Any
from ComicsLibrary.loggers.Logger import Logger


class ComicCRUD(EntityCRUD):
    def __init__(self):
        load_dotenv()
        db_name = os.getenv('MONGO_DB_NAME', 'comics_db')
        collection_name = os.getenv('MONGO_COMICS_COLLECTION', 'comics')
        super().__init__(db_name, collection_name)

    def read_by_title(self, comic_title: str) -> Optional[Dict[str, Any]]:
        self.logger.info("Reading comic by title")
        try:
            entity = self.collection.find_one({"title": comic_title})
            self.logger.info(f"Read comic: {entity}")
            entity["_id"] = str(entity["_id"])
            return entity
        except Exception as e:
            self.logger.error(f"Error reading comic title: {comic_title}, {e}")