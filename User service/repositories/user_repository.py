from ..database import Databese
from ..entities import User
from typing import List, Optional
from ..logger import Logger
from sqlalchemy.exc import InvalidRequestError, OperationalError, DatabaseError


class UserRepository:
    __logger = Logger.get_logger(__name__)

    def create_user(self, user: User) -> User:
        self.__logger.debug(f"Создание пользователя: {user}")
        try:
            with Databese.get_session() as db:
                db.add(user)
                db.commit()
                db.refresh(user)
                self.__logger.info(f"Пользователь создан: {user}")
                return user

        except InvalidRequestError as e:
            self.__logger.error(f"Ошибка запроса SQLAlchemy: {e}")
            raise
        except AttributeError as e:
            self.__logger.error(f"Ошибка структуры объекта User: {e}")
            raise
        except (OperationalError, DatabaseError) as e:
            self.__logger.critical(f"Ошибка базы данных при создании пользователя: {e}")
            raise

    def create_users(self, users: List[User]) -> List[User]:
        self.__logger.debug(f"Создание нескольких пользователей: {[u.name for u in users]}")
        try:
            with Databese.get_session() as db:
                db.add_all(users)
                db.commit()
                for user in users:
                    db.refresh(user)
                self.__logger.info(f"Создано {len(users)} пользователей")
                return users

        except InvalidRequestError as e:
            self.__logger.error(f"Ошибка запроса при массовом добавлении: {e}")
            raise
        except AttributeError as e:
            self.__logger.error(f"Ошибка в структуре одного из пользователей: {e}")
            raise
        except (OperationalError, DatabaseError) as e:
            self.__logger.critical(f"Ошибка базы данных при массовом добавлении пользователей: {e}")
            raise

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        self.__logger.debug(f"Поиск пользователя по ID: {user_id}")
        try:
            with Databese.get_session() as db:
                user = db.query(User).filter(User.id == user_id).first()
                self.__logger.info(f"Результат поиска по ID: {user}")
                return user

        except InvalidRequestError as e:
            self.__logger.error(f"Ошибка запроса при поиске по ID: {e}")
            raise
        except AttributeError as e:
            self.__logger.error(f"Ошибка структуры User при поиске по ID: {e}")
            raise
        except (OperationalError, DatabaseError) as e:
            self.__logger.critical(f"Ошибка базы данных при поиске по ID: {e}")
            raise

    def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        self.__logger.debug(f"Поиск пользователя по Telegram ID: {telegram_id}")
        try:
            with Databese.get_session() as db:
                user = db.query(User).filter(User.telegram_id == telegram_id).first()
                self.__logger.info(f"Результат поиска по Telegram ID: {user}")
                return user

        except InvalidRequestError as e:
            self.__logger.error(f"Ошибка запроса при поиске по Telegram ID: {e}")
            raise
        except AttributeError as e:
            self.__logger.error(f"Ошибка структуры User при поиске по Telegram ID: {e}")
            raise
        except (OperationalError, DatabaseError) as e:
            self.__logger.critical(f"Ошибка базы данных при поиске по Telegram ID: {e}")
            raise

    def get_user_by_name(self, name: str) -> Optional[User]:
        self.__logger.debug(f"Поиск пользователя по имени: {name}")
        try:
            with Databese.get_session() as db:
                user = db.query(User).filter(User.name == name).first()
                self.__logger.info(f"Результат поиска по имени: {user}")
                return user

        except InvalidRequestError as e:
            self.__logger.error(f"Ошибка запроса при поиске по имени: {e}")
            raise
        except AttributeError as e:
            self.__logger.error(f"Ошибка структуры User при поиске по имени: {e}")
            raise
        except (OperationalError, DatabaseError) as e:
            self.__logger.critical(f"Ошибка базы данных при поиске по имени: {e}")
            raise