import datetime
from PySide6.QtCore import Qt
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Annotated
from DB_offline.database import Base
from Enums import PlaybookType, TeamType, FillType, SymbolType, Modes, AppTheme


id_pk = Annotated[int, mapped_column(primary_key=True)]


class UserSettingsORM(Base):
    __tablename__ = 'user_settings'

    settings_id_pk: Mapped[id_pk]
    maximized: Mapped[bool]
    toolbar_condition: Mapped[bool]
    toolbar_area: Mapped[Qt.ToolBarArea]
    theme: Mapped[AppTheme]

    def __repr__(self):
        return f'<{self.__class__.__name__} (id_pk: {self.settings_id_pk}, maximized: {self.maximized},' \
               f'toolbar_condition: {self.toolbar_condition}, toolbar_area: {self.toolbar_area},' \
               f' theme: {self.theme}) at {hex(id(self))}>'


class PlaybookORM(Base):
    __tablename__ = 'playbooks'

    playbook_id_pk: Mapped[id_pk]
    # team_id_fk: Mapped[int]??????????????????
    playbook_name: Mapped[str]
    playbook_type: Mapped[PlaybookType]
    # enabled: Mapped[bool]
    created_at: Mapped[str]
    updated_at: Mapped[str]

    schemes: Mapped[list['SchemeORM']] = relationship(back_populates='playbook',
                                                      cascade='all, delete-orphan',
                                                      order_by='SchemeORM.row_number.asc()')

    # created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    # updated_at: Mapped[datetime.datetime] = mapped_column(default=func.now(),
    #                                                       onupdate=datetime.datetime.now())

    def __repr__(self):
        return f'<{self.__class__.__name__} (id_pk: {self.playbook_id_pk}; name: {self.playbook_name};' \
               f' type: {self.playbook_type}) at {hex(id(self))}>'

    def return_data(self):
        return self.playbook_name, self.playbook_type, self.playbook_id_pk


class SchemeORM(Base):
    __tablename__ = 'schemes'

    scheme_id_pk: Mapped[id_pk]
    playbook_id_fk: Mapped[int] = mapped_column(ForeignKey('playbooks.playbook_id_pk', ondelete='CASCADE'))
    row_number: Mapped[int]
    scheme_name: Mapped[str]
    view_point_x: Mapped[float]
    view_point_y: Mapped[float]
    first_team_placed: Mapped[TeamType | None]
    second_team_placed: Mapped[TeamType | None]
    first_team_position: Mapped[int | None]

    playbook: Mapped['PlaybookORM'] = relationship(back_populates='schemes')

    players: Mapped[list['PlayerORM']] = relationship(back_populates='scheme', cascade='all, delete-orphan')
    ellipses: Mapped[list['EllipseORM']] = relationship(back_populates='scheme', cascade='all, delete-orphan')
    rectangles: Mapped[list['RectangleORM']] = relationship(back_populates='scheme', cascade='all, delete-orphan')
    labels: Mapped[list['LabelORM']] = relationship(back_populates='scheme', cascade='all, delete-orphan')
    pencil_lines: Mapped[list['PencilLineORM']] = relationship(back_populates='scheme', cascade='all, delete-orphan')

    def return_data(self):
        return self.row_number, self.scheme_name, self.view_point_x, self.view_point_y,\
               self.first_team_placed, self.second_team_placed, self.first_team_position, self.scheme_id_pk, self.playbook_id_fk


class PlayerORM(Base):
    __tablename__ = 'players'

    player_id_pk: Mapped[id_pk]
    scheme_id_fk: Mapped[int] = mapped_column(ForeignKey('schemes.scheme_id_pk', ondelete='CASCADE'))
    x: Mapped[float]
    y: Mapped[float]
    team_type: Mapped[TeamType]
    player_position: Mapped[str]
    current_action_number: Mapped[int]
    text: Mapped[str]
    text_color: Mapped[str]
    player_color: Mapped[str]
    fill_type: Mapped[FillType | None]
    symbol_type: Mapped[SymbolType | None]

    scheme: Mapped['SchemeORM'] = relationship(back_populates='players')

    lines: Mapped[list['LineORM']] = relationship(back_populates='player', cascade='all, delete-orphan')
    action_finishes_arr: Mapped[list['FinalActionArrowORM']] = relationship(back_populates='player', cascade='all, delete-orphan')
    action_finishes_line: Mapped[list['FinalActionLineORM']] = relationship(back_populates='player', cascade='all, delete-orphan')

    def return_data(self):
        if self.team_type == TeamType.offence or self.team_type == TeamType.kickoff\
                or self.team_type == TeamType.punt_kick or self.team_type == TeamType.field_goal_off\
                or self.team_type == TeamType.offence_add:
            return self.team_type, self.player_position, self.text, self.text_color, self.player_color,\
                   self.fill_type, self.x, self.y, self.current_action_number, self.player_id_pk, self.scheme_id_fk
        elif self.team_type == TeamType.defence or self.team_type == TeamType.kick_ret or self.team_type == TeamType.punt_ret or self.team_type == TeamType.field_goal_def:
            return self.team_type, self.player_position, self.text, self.text_color, self.player_color,\
                   self.symbol_type, self.x, self.y, self.current_action_number, self.player_id_pk, self.scheme_id_fk


class LineORM(Base):
    __tablename__ = 'lines'

    line_id_pk: Mapped[id_pk]
    player_id_fk: Mapped[int] = mapped_column(ForeignKey('players.player_id_pk', ondelete='CASCADE'))
    x1: Mapped[float]
    y1: Mapped[float]
    x2: Mapped[float]
    y2: Mapped[float]
    action_number: Mapped[int]
    line_thickness: Mapped[int]
    line_color: Mapped[str]
    action_type: Mapped[Modes]

    player: Mapped['PlayerORM'] = relationship(back_populates='lines')

    def return_data(self):
        return self.x1, self.y1, self.x2, self.y2, self.action_number, self.line_thickness, self.line_color,\
               self.action_type, self.line_id_pk, self.player_id_fk


class FinalActionArrowORM(Base):
    __tablename__ = 'action_finishes_arrow'

    arr_finish_id_pk: Mapped[id_pk]
    player_id_fk: Mapped[int] = mapped_column(ForeignKey('players.player_id_pk', ondelete='CASCADE'))
    x: Mapped[float]
    y: Mapped[float]
    angle: Mapped[float]
    line_thickness: Mapped[int]
    line_color: Mapped[str]
    action_number: Mapped[int]
    action_type: Mapped[Modes]

    player: Mapped['PlayerORM'] = relationship(back_populates='action_finishes_arr')

    def return_data(self):
        return self.x, self.y, self.angle, self.line_thickness, self.line_color, self.action_number, self.action_type,\
               self.arr_finish_id_pk, self.player_id_fk


class FinalActionLineORM(Base):
    __tablename__ = 'action_finishes_line'

    line_finish_id_pk: Mapped[id_pk]
    player_id_fk: Mapped[int] = mapped_column(ForeignKey('players.player_id_pk', ondelete='CASCADE'))
    x: Mapped[float]
    y: Mapped[float]
    angle: Mapped[float]
    line_thickness: Mapped[int]
    line_color: Mapped[str]
    action_number: Mapped[int]
    action_type: Mapped[Modes]

    player: Mapped['PlayerORM'] = relationship(back_populates='action_finishes_line')

    def return_data(self):
        return self.x, self.y, self.angle, self.line_thickness, self.line_color, self.action_number, self.action_type,\
               self.line_finish_id_pk, self.player_id_fk


class EllipseORM(Base):
    __tablename__ = 'ellipses'

    ellipse_id_pk: Mapped[id_pk]
    scheme_id_fk: Mapped[int] = mapped_column(ForeignKey('schemes.scheme_id_pk', ondelete='CASCADE'))
    x: Mapped[float]
    y: Mapped[float]
    width: Mapped[float]
    height: Mapped[float]
    border: Mapped[bool]
    border_thickness: Mapped[int]
    border_color: Mapped[str]
    fill: Mapped[bool]
    fill_opacity: Mapped[str]
    fill_color: Mapped[str]

    scheme: Mapped['SchemeORM'] = relationship(back_populates='ellipses')

    def return_data(self):
        return self.x, self.y, self.width, self.height, self.border, self.border_thickness, self.border_color,\
               self.fill, self.fill_opacity, self.fill_color, self.ellipse_id_pk, self.scheme_id_fk


class RectangleORM(Base):
    __tablename__ = 'rectangles'

    rect_id_pk: Mapped[id_pk]
    scheme_id_fk: Mapped[int] = mapped_column(ForeignKey('schemes.scheme_id_pk', ondelete='CASCADE'))
    x: Mapped[float]
    y: Mapped[float]
    width: Mapped[float]
    height: Mapped[float]
    border: Mapped[bool]
    border_thickness: Mapped[int]
    border_color: Mapped[str]
    fill: Mapped[bool]
    fill_opacity: Mapped[str]
    fill_color: Mapped[str]

    scheme: Mapped['SchemeORM'] = relationship(back_populates='rectangles')

    def return_data(self):
        return self.x, self.y, self.width, self.height, self.border, self.border_thickness, self.border_color,\
               self.fill, self.fill_opacity, self.fill_color, self.rect_id_pk, self.scheme_id_fk


class LabelORM(Base):
    __tablename__ = 'labels'

    label_id_pk: Mapped[id_pk]
    scheme_id_fk: Mapped[int] = mapped_column(ForeignKey('schemes.scheme_id_pk', ondelete='CASCADE'))
    text: Mapped[str]
    font_type: Mapped[str]
    font_size: Mapped[int]
    font_bold: Mapped[bool]
    font_italic: Mapped[bool]
    font_underline: Mapped[bool]
    font_color: Mapped[str]
    x: Mapped[float]
    y: Mapped[float]
    width: Mapped[float]
    height: Mapped[float]

    scheme: Mapped['SchemeORM'] = relationship(back_populates='labels')

    def return_data(self):
        return self.text, self.font_type, self.font_size, self.font_bold, self.font_italic, self.font_underline, self.font_color,\
               self.x, self.y, self.width, self.height, self.label_id_pk, self.scheme_id_fk


class PencilLineORM(Base):
    __tablename__ = 'pencil_lines'

    line_id_pk: Mapped[id_pk]
    scheme_id_fk: Mapped[int] = mapped_column(ForeignKey('schemes.scheme_id_pk', ondelete='CASCADE'))
    x1: Mapped[float]
    y1: Mapped[float]
    x2: Mapped[float]
    y2: Mapped[float]
    line_thickness: Mapped[int]
    line_color: Mapped[str]

    scheme: Mapped['SchemeORM'] = relationship(back_populates='pencil_lines')

    def return_data(self):
        return self.x1, self.y1, self.x2, self.y2, self.line_thickness, self.line_color,\
               self.line_id_pk, self.scheme_id_fk
