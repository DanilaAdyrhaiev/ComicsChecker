from .EntityMapper import EntityMapper
from ComicsLibrary.entities import Comic
from ComicsLibrary.DTO import ComicDTO


class ComicMapper(EntityMapper[Comic, ComicDTO]):
    def to_dto(self, comic: Comic) -> ComicDTO:
        return ComicDTO(id=comic.id, title=comic.title, last_chapter_date=comic.last_chapter_date, users=comic.users if comic.users else [])

    def to_entity(self, dto: ComicDTO) -> Comic:
        return Comic(_id=dto.id, title=dto.title, last_chapter_date=dto.last_chapter_date, users=dto.users if dto.users else [])
