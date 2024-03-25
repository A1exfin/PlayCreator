from typing import TYPE_CHECKING, Union
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt, QPointF
from DB_offline.models import SchemeORM
from Graphics import Field

if TYPE_CHECKING:
    from PySide6.QtWidgets import QMainWindow
    from Enums import TeamType, PlaybookType

__all__ = ['Scheme']


class Scheme(QListWidgetItem):
    def __init__(self, main_window: 'QMainWindow', playbook_type: 'PlaybookType', scheme_name: str,
                 view_point_x: float | None = None, view_point_y: float | None = None,
                 first_team_placed: Union['TeamType', None] = None, second_team_placed: Union['TeamType', None] = None,
                 first_team_position: int | None = None,
                 scheme_id_pk: int = None, playbook_id_fk: int = None):
        super().__init__(scheme_name)
        self.scheme_id_pk = scheme_id_pk
        self.playbook_id_fk = playbook_id_fk
        self.scene = Field(main_window, playbook_type)
        # При инициализации сцены, точка обзора устанавливается на середину поля.
        # Если переданы коардинаты точки обзора, точка обзора меняется с середины поля на переданную точку обзора.
        if view_point_x and view_point_y:
            self.scene.view_point = QPointF(view_point_x, view_point_y)
        self.scene.first_team_placed = first_team_placed
        self.scene.second_team_placed = second_team_placed
        self.scene.first_team_position = first_team_position
        self.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.is_deleted = False

    def __eq__(self, other):
        return self.scheme_id_pk == other.scheme_id_pk if isinstance(other, SchemeORM) else super().__eq__(other)

    def __repr__(self):
        return f'\n\t<{self.__class__.__name__} (id_pk: {self.scheme_id_pk}; playbook_id_fk: {self.playbook_id_fk};' \
               f' row_number: {self.listWidget().row(self)}; text: {self.text()};' \
               f' view_point_x/view_point_y: {self.scene.view_point.x()}/{self.scene.view_point.y()};' \
               f' first_team: {self.scene.first_team_placed}; second_team: {self.scene.second_team_placed};' \
               f' first_team_pos: {self.scene.first_team_position}; deleted: {self.is_deleted}) at {hex(id(self))}>'

    def return_data(self):
        return self.scheme_id_pk, self.playbook_id_fk, self.text(), self.listWidget().row(self),\
               self.scene.view_point.x(), self.scene.view_point.y(),\
               self.scene.first_team_placed, self.scene.second_team_placed, self.scene.first_team_position