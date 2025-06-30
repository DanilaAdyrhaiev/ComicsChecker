from ..entities import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from ..logger import Logger


class Databese:
    __sqlite_database = "sqlite:///users.db"
    __engine = create_engine(__sqlite_database)
    __logger = Logger.get_logger(__name__)  # корректный вызов логгера

    def __init__(self):
        Base.metadata.create_all(bind=self.__engine)
        self.__logger.debug("База данных инициализирована")

    @classmethod
    def get_session(cls):
        cls.__logger.debug("Создание сессии БД")
        return Session(autoflush=False, bind=cls.__engine)
