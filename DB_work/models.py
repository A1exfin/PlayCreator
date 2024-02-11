from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated
from enum import Enum
from DB_work.database import Base
from Enum_flags import PlaybookType, TeamType, FillType, SymbolType


id_pk = Annotated[int, mapped_column(primary_key=True)]


class Playbook(Base):
    __tablename__ = 'playbooks'

    playbook_id_pk: Mapped[id_pk]
    # team_id_fk: Mapped[int]??????????????????
    playbook_name: Mapped[str]
    playbook_type: Mapped[PlaybookType]
    # enabled: Mapped[bool]


class Scheme(Base):
    __tablename__ = 'schemes'

    scheme_id_pk: Mapped[id_pk]
    playbook_id_fk: Mapped[int] = mapped_column(ForeignKey('playbooks.playbook_id_pk', ondelete='CASCADE'))
    scheme_name: Mapped[str]
    row_number: Mapped[int]
    view_point_x: Mapped[float]
    view_point_y: Mapped[float]
    first_team_placed: Mapped[TeamType | None]
    second_team_placed: Mapped[TeamType | None]
    additional_offence_player: Mapped[bool | None]
    first_team_position: Mapped[float | None]


class Player(Base):
    __tablename__ = 'players'

    player_id_pk: Mapped[id_pk]
    scheme_id_fk: Mapped[int] = mapped_column(ForeignKey('schemes.scheme_id_pk', ondelete='CASCADE'))
    team: Mapped[TeamType]
    player_position: Mapped[str]
    player_text: Mapped[str]
    text_color: Mapped[str]
    player_color: Mapped[str]
    fill_type: Mapped[FillType]
    symbol_type: Mapped[SymbolType]
    x: Mapped[float]
    y: Mapped[float]
    current_action_number: Mapped[int]


class Line(Base):
    __tablename__ = 'lines'

    line_id_pk: Mapped[id_pk]
    player_id_fk: Mapped[int] = mapped_column(ForeignKey('players.player_id_pk', ondelete='CASCADE'))
    action_number: Mapped[int]
    line_thickness: Mapped[int]
    line_color: Mapped[str]
    action_type: Mapped[str]  # ENUM
    x1: Mapped[float]
    y1: Mapped[float]
    x2: Mapped[float]
    y2: Mapped[float]


class ActionFinish(Base):
    __tablename__ = 'action_finishes'

    action_id_pk: Mapped[id_pk]
    player_id_fk: Mapped[int] = mapped_column(ForeignKey('players.player_id_pk', ondelete='CASCADE'))
    action_number: Mapped[int]
    line_thickness: Mapped[int]
    line_color: Mapped[str]
    action_type: Mapped[str]  # ENUM
    x: Mapped[float]
    y: Mapped[float]
    angle: Mapped[float]


class Ellipse(Base):
    __tablename__ = 'ellipses'

    ellipse_id_pk: Mapped[id_pk]
    scheme_id_fk: Mapped[int] = mapped_column(ForeignKey('schemes.scheme_id_pk', ondelete='CASCADE'))
    x: Mapped[float]
    y: Mapped[float]
    width: Mapped[float]
    height: Mapped[float]
    border_thickness: Mapped[int]
    color: Mapped[str]


class Rectangle(Base):
    __tablename__ = 'rectangles'

    rectangle_id_pk: Mapped[id_pk]
    scheme_id_fk: Mapped[int] = mapped_column(ForeignKey('schemes.scheme_id_pk', ondelete='CASCADE'))
    x: Mapped[float]
    y: Mapped[float]
    width: Mapped[float]
    height: Mapped[float]
    border_thickness: Mapped[int]
    color: Mapped[str]


class Label(Base):
    __tablename__ = 'labels'

    label_id_pk: Mapped[id_pk]
    scheme_id_fk: Mapped[int] = mapped_column(ForeignKey('schemes.scheme_id_pk', ondelete='CASCADE'))
    x: Mapped[float]
    y: Mapped[float]
    width: Mapped[float]
    # height: Mapped[float]
    text: Mapped[str]
    font_type: Mapped[str]
    font_point_size: Mapped[int]
    font_color: Mapped[str]
    font_bold: Mapped[bool]
    font_italic: Mapped[bool]
    font_underline: Mapped[bool]


class PencilLine(Base):
    __tablename__ = 'pencil_lines'

    line_id_pk: Mapped[id_pk]
    scheme_id_fk: Mapped[int] = mapped_column(ForeignKey('schemes.scheme_id_pk', ondelete='CASCADE'))
    line_thickness: Mapped[int]
    line_color: Mapped[str]
    x1: Mapped[float]
    y1: Mapped[float]
    x2: Mapped[float]
    y2: Mapped[float]