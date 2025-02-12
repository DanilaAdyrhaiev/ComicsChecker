from typing import Optional

from .EntityService import EntityService
from ComicsLibrary.repositories import UserRepository
from ComicsLibrary.mappers import UserMapper
from ComicsLibrary.entities import User
from ComicsLibrary.DTO import UserDTO


class UserService(EntityService):
    def __init__(self):
        super().__init__(UserRepository(), UserMapper())

    def get_by_chat_id(self, chat_id: int) -> Optional[UserDTO]:
        self.logger.info("Getting user by chat id")
        user = self.repository.find_by_chat_id(chat_id)
        self.logger.info("User found")
        return self.mapper.to_dto(user) if user else None

    def remove(self, entity_id: str) -> bool:
        self.logger.info("Removing user by chat id")
        entity: User = self.repository.find_by_id(entity_id)
        if entity is not None:
            if entity.comics is not None:
                if len(entity.comics) > 0:
                    val = self.repository.remove_by_id(entity_id)
                    self.logger.info("User removed")
                    return True if val > 0 else False