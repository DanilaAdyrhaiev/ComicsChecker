from ComicsLibrary.CRUDs import ComicCRUD
from .EntityRepository import EntityRepository
from ComicsLibrary.entities import Comic
from typing import Optional


class ComicRepository(EntityRepository):
    def __init__(self):
        super().__init__(ComicCRUD())

    def save(self, comic: Comic) -> Optional[Comic]:
        if comic.id is None:
            entity = self.find_by_title(comic.title)
            if entity is None:
                return super().save(comic)
            return entity
        else:
            return self.update(comic)

    def find_by_title(self, title: str) -> Optional[Comic]:
        self.logger.info("Finding comic with title: {}".format(title))
        try:
            val = self.crud.read_by_title(title)
            self.logger.info("Founded comics by title: {}".format(val))
            print(type(val))
            val = Comic.from_dict(val)
            self.logger.info("Converted from dict to entity: {}".format(val))
            return val
        except Exception as e:
            self.logger.error("Could not find comic with title: {} {}".format(title, e))
