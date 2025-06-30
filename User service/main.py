from entities import Base
from sqlalchemy import create_engine


sqlite_database = "sqlite:///users.db"
engine = create_engine(sqlite_database)
Base.metadata.create_all(bind=engine)