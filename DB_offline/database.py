import os
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine

DATABASE_NAME = 'PlayCreator.db'

engine = create_engine(
    url=f'sqlite:///{os.getcwd()}\{DATABASE_NAME}',
    # echo=True,
)

session_factory = sessionmaker(engine)


class Base(DeclarativeBase):
    pass