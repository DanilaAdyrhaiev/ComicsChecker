from .EntityMapper import EntityMapper
from ComicsLibrary.entities import User
from ComicsLibrary.DTO import UserDTO

class UserMapper(EntityMapper):
    def to_dto(self, user: User) -> UserDTO:
        return UserDTO(id=user.id, chat_id= user.chat_id, name=user.name, comics=user.comics if user.comics else [])

    def to_entity(self, dto: UserDTO) -> User:
        return User(_id=dto.id, chat_id=dto.chat_id, name=dto.name, comics=dto.comics if dto.comics else [])