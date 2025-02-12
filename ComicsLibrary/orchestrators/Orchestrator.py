from typing import Optional, List

from ComicsLibrary.services import UserService, ComicService
from ComicsLibrary.DTO import UserDTO, ComicDTO
from ComicsLibrary.loggers.Logger import Logger


class Orchestrator:
    def __init__(self):
        self.user_service = UserService()
        self.comic_service = ComicService()
        self.logger = Logger.get_logger(self.__class__.__name__)

    def add_user(self, user_to_add: UserDTO) -> Optional[UserDTO]:
        self.logger.info(f"Adding user {user_to_add}")
        user_dto = self.user_service.add(user_to_add)
        self.logger.info(f"User added: {user_to_add}")
        return user_dto

    def add_comic(self, comic_to_add: ComicDTO) -> Optional[ComicDTO]:
        self.logger.info(f"Adding comic {comic_to_add}")
        comic_dto = self.comic_service.add(comic_to_add)
        self.logger.info(f"Comic added: {comic_to_add}")
        return comic_dto

    def get_user(self, chat_id=None, id=None) -> Optional[UserDTO]:
        self.logger.info(f"Getting user {chat_id} {id}")
        if id is not None:
            self.logger.info(f"Getting user {id}")
            user_dto = self.user_service.get_by_id(id)
            self.logger.info(f"User found: {user_dto}")
            return user_dto
        elif chat_id is not None:
            self.logger.info(f"Getting user {chat_id}")
            user_dto = self.user_service.get_by_chat_id(chat_id)
            self.logger.info(f"User found: {user_dto}")
            return user_dto
        return None

    def get_comic(self, id=None, title=None) -> Optional[ComicDTO]:
        self.logger.info(f"Getting comic {id} {title}")
        if id is not None:
            self.logger.info(f"Getting comic {id}")
            comic_dto = self.comic_service.get_by_id(id)
            self.logger.info(f"Comic found: {comic_dto}")
            return comic_dto
        elif title is not None:
            self.logger.info(f"Getting comic {title}")
            comic_dto = self.comic_service.get_by_title(title)
            self.logger.info(f"Comic found: {comic_dto}")
            return comic_dto
        return None

    def get_comics(self) -> Optional[List[ComicDTO]]:
        self.logger.info(f"Getting comics")
        users_dto = self.comic_service.get_all()
        self.logger.info(f"Comics found: {users_dto}")
        return users_dto

    def add_comic_to_user(self, comic_id: str, chat_id: int) -> bool:
        self.logger.info(f"Adding comic {comic_id} to user {chat_id}")
        try:
            comic = self.get_comic(id = comic_id)
            self.logger.info(f"Got comic: {comic}")
            if comic:
                user = self.user_service.get_by_chat_id(chat_id)
                user.comics.append(comic.id)
                comic.users.append(user.id)
                updated_user = self.user_service.update(user)
                updated_comic = self.comic_service.update(comic)
                if updated_comic is not None and updated_user is not None:
                    return True
            else:
                return False
        except Exception as e:
            self.logger.error(f"Error adding comic {e}")
            return False