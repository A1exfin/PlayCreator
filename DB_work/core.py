from DB_work.database import engine
from DB_work.models import Playbook, Scheme, Player, Line, ActionFinish, Ellipse, Rectangle, Label, PencilLine
from DB_work.database import Base, session_factory


def create_tables():
    Base.metadata.drop_all(engine)  # для отладки
    Base.metadata.create_all(engine)


def insert_data():
    pass


