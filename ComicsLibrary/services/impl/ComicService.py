from .EntityService import EntityService
from ComicsLibrary.repositories import ComicRepository
from ComicsLibrary.mappers import ComicMapper
from ComicsLibrary.DTO import ComicDTO
from ComicsLibrary.entities import Comic
from typing import Optional


class ComicService(EntityService):
    def __init__(self):
        super().__init__(ComicRepository(), ComicMapper())

    def get_by_title(self, entity_title: str) -> Optional[ComicDTO]:
        self.logger.info("Getting comic by title")
        comic = self.repository.find_by_title(entity_title)
        self.logger.info("Found comic by title")
        return self.mapper.to_dto(comic) if comic else None

    def remove(self, entity_id: str) -> bool:
        self.logger.info("Removing comic by id")
        entity: Comic = self.repository.find_by_id(entity_id)
        if entity is not None:
            if entity.users is not None:
                if len(entity.users) > 0:
                    val = self.repository.remove_by_id(entity_id)
                    self.logger.info("Removing comic by id")
                    return True if val > 0 else False
