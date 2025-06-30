from ..repositories import UserRepository
from ..mappers import UserMapper
from ..DTOs import User_DTO
from ..logger import Logger
from sqlalchemy.exc import InvalidRequestError, OperationalError, DatabaseError
from typing import Optional, List


class UserService:
    __logger = Logger.get_logger(__name__)

    def __init__(self):
        self.__repo = UserRepository()
        self.__mapper = UserMapper()

    def create_user(self, user_dto: User_DTO) -> User_DTO:
        if not user_dto.telegram_id or not user_dto.name:
            raise ValueError("Обязательные поля telegram_id и name должны быть заполнены")

        try:
            mapped_user = self.__mapper.to_entity(user_dto)
            created_user = self.__repo.create_user(mapped_user)
            return self.__mapper.to_dto(created_user)

        except (InvalidRequestError, AttributeError, OperationalError, DatabaseError) as e:
            self.__logger.error(f"Ошибка при создании пользователя: {e}")
            raise

    def create_users(self, user_dtos: List[User_DTO]) -> List[User_DTO]:
        if not user_dtos:
            raise ValueError("Список пользователей не может быть пустым")

        valid_dtos = []
        for i, dto in enumerate(user_dtos):
            if dto.telegram_id and dto.name:
                valid_dtos.append(dto)
            else:
                self.__logger.warning(f"Пропущен некорректный пользователь под индексом {i}: {dto}")

        if not valid_dtos:
            raise ValueError("Нет ни одного корректного пользователя для создания")

        try:
            users = [self.__mapper.to_entity(dto) for dto in valid_dtos]
            created = self.__repo.create_users(users)
            return [self.__mapper.to_dto(user) for user in created]

        except (InvalidRequestError, AttributeError, OperationalError, DatabaseError) as e:
            self.__logger.error(f"Ошибка при создании нескольких пользователей: {e}")
            raise


    def get_user_by_id(self, user_id: int) -> Optional[User_DTO]:
        try:
            user = self.__repo.get_user_by_id(user_id)
            return self.__mapper.to_dto(user) if user else None

        except (InvalidRequestError, AttributeError, OperationalError, DatabaseError) as e:
            self.__logger.error(f"Ошибка при поиске пользователя по ID: {e}")
            raise

    def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User_DTO]:
        try:
            user = self.__repo.get_user_by_telegram_id(telegram_id)
            return self.__mapper.to_dto(user) if user else None

        except (InvalidRequestError, AttributeError, OperationalError, DatabaseError) as e:
            self.__logger.error(f"Ошибка при поиске по Telegram ID: {e}")
            raise

    def get_user_by_name(self, name: str) -> Optional[User_DTO]:
        try:
            user = self.__repo.get_user_by_name(name)
            return self.__mapper.to_dto(user) if user else None

        except (InvalidRequestError, AttributeError, OperationalError, DatabaseError) as e:
            self.__logger.error(f"Ошибка при поиске по имени: {e}")
            raise
