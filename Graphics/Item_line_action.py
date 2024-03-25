from typing import TYPE_CHECKING
import os
from PySide6.QtWidgets import QGraphicsLineItem
from PySide6.QtGui import QColor, QPen, QPainter, QCursor, QPixmap
from PySide6.QtCore import QLineF, Qt
from Enums import Modes
import Graphics
from DB_offline.models import LineORM

if TYPE_CHECKING:
    from Graphics import Player

__all__ = ['ActionLine']


class ActionLine(QGraphicsLineItem):
    pen_hover_color = QColor('#ffcb30')

    def __init__(self, player: 'Player', x1: float, y1: float, x2: float, y2: float,
                 action_number: int, line_thickness: int, line_color: str, action_type: Modes,
                 line_id_pk: int = None, player_id_fk: int = None):
        super().__init__(QLineF(x1, y1, x2, y2))
        self.line_id_pk = line_id_pk
        self.player_id_fk = player_id_fk
        self.player = player
        self.action_type = action_type
        self.pen = QPen(QColor(line_color), line_thickness, s=Qt.SolidLine, c=Qt.RoundCap, j=Qt.RoundJoin)
        if self.action_type == Modes.route or self.action_type == Modes.block:
            self.pen.setStyle(Qt.PenStyle.SolidLine)
        elif self.action_type == Modes.motion:
            self.pen.setStyle(Qt.PenStyle.DashLine)
        self.setAcceptHoverEvents(True)
        self.action_number = action_number
        self.hover = False
        self.setZValue(1)
        self.object_name = f'{self.player.player_position}_{self.action_type}_{self.action_number}'

    def paint(self, painter, option, widget=None):
        painter.setRenderHints(QPainter.Antialiasing)
        if self.hover:
            self.setPen(QPen(self.pen_hover_color, self.pen.width(), self.pen.style(), self.pen.capStyle(), self.pen.joinStyle()))
        else:
            self.setPen(QPen(self.pen))
        super().paint(painter, option, widget)
        # self.scene().update()  # Нужно для полного удаления действия со сцены СРАЗУ после клика по линии
        # self.update()

    def mouseDoubleClickEvent(self, event):
        self.ungrabMouse()

    def mousePressEvent(self, event):
        # print(self)
        self.ungrabMouse()
        if self.scene().mode == Modes.route and (self.action_type == Modes.route or self.action_type == Modes.motion) and event.button() == Qt.LeftButton:
            self.scene().allow_painting = True
            self.scene().start_pos = event.scenePos()
            self.player.setSelected(True)
            self.scene().current_player = self.player
            self.scene().action_number_temp = self.action_number
            self.scene().action_number_temp, self.player.current_action_number \
                = self.player.current_action_number, self.scene().action_number_temp
        elif self.scene().mode == Modes.block and self.action_type == Modes.motion and event.button() == Qt.LeftButton:
            self.scene().allow_painting = True
            self.scene().start_pos = event.scenePos()
            self.player.setSelected(True)
            self.scene().current_player = self.player
            self.scene().action_number_temp = self.action_number
            self.scene().action_number_temp, self.player.current_action_number \
                = self.player.current_action_number, self.scene().action_number_temp
        elif self.scene().mode == Modes.erase and event.button() == Qt.LeftButton:
            self.setCursor(Qt.ArrowCursor)  # Возврат стандартного курсора сразу после клика
            actions_lst = self.player.actions[f'action_number:{self.action_number}']
            group = self.scene().createItemGroup(actions_lst)
            self.scene().removeItem(group)
            self.player.hover = False
            for action_part in actions_lst:
                if isinstance(action_part, ActionLine) and action_part.line_id_pk:
                    self.player.deleted_action_parts.append(action_part)
                elif isinstance(action_part, Graphics.FinalActionLine) and action_part.f_line_action_id_pk:
                    self.player.deleted_action_parts.append(action_part)
                elif isinstance(action_part, Graphics.FinalActionArrow) and action_part.f_arr_action_id_pk:
                    self.player.deleted_action_parts.append(action_part)
            self.player.actions.pop(f'action_number:{self.action_number}')

    def hoverEnterEvent(self, event):
        if (self.action_type == Modes.route and self.scene().mode == Modes.route) or\
                (self.action_type == Modes.motion and (self.scene().mode == Modes.route or self.scene().mode == Modes.block)) or\
                self.scene().mode == Modes.erase:
            for action in self.player.actions[f'action_number:{self.action_number}']:
                action.hover = True
            self.player.hover = True
        if self.scene().mode == Modes.erase:
            self.setCursor(QCursor(QPixmap('://Cursors/Cursors/eraser.cur'), 0, 0))

    def hoverMoveEvent(self, event):
        if (self.action_type == Modes.route and self.scene().mode == Modes.route) or\
                (self.action_type == Modes.motion and (self.scene().mode == Modes.route or self.scene().mode == Modes.block)) or\
                self.scene().mode == Modes.erase:
            for action in self.player.actions[f'action_number:{self.action_number}']:
                action.hover = True
            self.player.hover = True
        else:
            for action in self.player.actions[f'action_number:{self.action_number}']:
                action.hover = False
            self.player.hover = False
        if self.scene().mode == Modes.erase:
            self.setCursor(QCursor(QPixmap('://Cursors/Cursors/eraser.cur'), 0, 0))
        else:
            self.setCursor(Qt.ArrowCursor)

    def hoverLeaveEvent(self, event):
        for action in self.player.actions[f'action_number:{self.action_number}']:
            action.hover = False
        self.player.hover = False
        self.setCursor(Qt.ArrowCursor)

    def __eq__(self, other):
        return self.line_id_pk == other.line_id_pk if isinstance(other, LineORM) else super().__eq__(other)

    def __repr__(self):
        return f'\n\t<{self.__class__.__name__} (id_pk: {self.line_id_pk}; player_id_fk: {self.player_id_fk}; ' \
               f'x1/y1: {self.line().x1()}/{self.line().y1()}; x2/y2: {self.line().x2()}/{self.line().y2()};' \
               f' action_type: {self.action_type}; action_number: {self.action_number};' \
               f' color: {self.pen.color().name()}; player: {self.player.text}) at {hex(id(self))}>'

    def return_data(self):
        return self.line_id_pk, self.player_id_fk, self.line().x1(), self.line().y1(), self.line().x2(), self.line().y2(), \
               self.action_number, self.pen.width(), self.pen.color().name(), self.action_type
