from ComicsLibrary.CRUDs import UserCRUD
from .EntityRepository import EntityRepository
from ComicsLibrary.entities import User
from typing import Optional


class UserRepository(EntityRepository):
    def __init__(self):
        super().__init__(UserCRUD())

    def save(self, user: User) -> Optional[User]:
        if user.id is None:
            entity = self.find_by_chat_id(user.chat_id)
            if entity is None:
                return super().save(user)
            return entity
        else:
            return self.update(user)

    def find_by_chat_id(self, chat_id) -> Optional[User]:
        self.logger.info("Finding user by chat id")
        try:
            val = self.crud.read_by_chat_id(chat_id)
            self.logger.info("Founded user by chat id: {}".format(val))
            print(type(val))
            val = User.from_dict(val)
            self.logger.info("Converted from dict to entity: {}".format(val))
            return val
        except:
            self.logger.error("Could not find user by chat id {}".format(chat_id))