from ...entities import User
from ...DTOs import User_DTO
from ..mapper import Mapper
from typing import Type

class UserMapper(Mapper[User, User_DTO]):
    def to_dto(self, entity: User) -> User_DTO:
        return User_DTO(
            id=entity.id,
            telegram_id=entity.telegram_id,
            name=entity.name
        )

    def to_entity(self, dto: User_DTO) -> User:
        return User(
            id=dto.id,
            telegram_id=dto.telegram_id,
            name=dto.name
        )