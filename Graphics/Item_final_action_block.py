from typing import TYPE_CHECKING
import os
from PySide6.QtWidgets import QGraphicsLineItem
from PySide6.QtGui import QColor, QPen, QPainter, QCursor, QPixmap
from PySide6.QtCore import QPointF, QLineF, Qt
from Enums import Modes
import Graphics
from DB_offline.models import FinalActionLineORM

if TYPE_CHECKING:
    from Graphics import Player

__all__ = ['FinalActionLine']


class FinalActionLine(QGraphicsLineItem):
    pen_hover_color = QColor('#ffcb30')

    def __init__(self, player: 'Player', x: float, y: float, angle: float,
                 line_thickness: int, line_color: str, action_number: int, action_type: Modes,
                 line_action_id_pk: int = None, player_id_fk: int = None):
        line = QLineF(QPointF(0, -7), QPointF(0, 7))
        super().__init__(line)
        self.f_line_action_id_pk = line_action_id_pk
        self.player_id_fk = player_id_fk
        self.player = player
        self.action_number = action_number
        self.action_type = action_type
        self.pen = QPen(QColor(line_color), line_thickness, s=Qt.SolidLine, c=Qt.RoundCap, j=Qt.RoundJoin)
        self.angle = angle
        self.setRotation(-self.angle)
        self.setPos(x, y)
        self.setAcceptHoverEvents(True)
        self.hover = False
        self.setZValue(1)
        self.object_name = f'{self.player.player_position}_{self.action_type}_{self.action_number}'

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)
        if self.hover:
            self.setPen(QPen(self.pen_hover_color, self.pen.width(), s=self.pen.style(), c=self.pen.capStyle(), j=self.pen.joinStyle()))
        else:
            self.setPen(self.pen)
        super().paint(painter, option, widget)

    def mouseDoubleClickEvent(self, event):
        self.ungrabMouse()

    def mousePressEvent(self, event):
        # print(self)
        if self.scene().mode == Modes.erase and event.button() == Qt.LeftButton:
            self.setCursor(Qt.ArrowCursor)  # Возврат стандартного курсора сразу после клика
            actions_lst = self.player.actions[f'action_number:{self.action_number}']
            group = self.scene().createItemGroup(actions_lst)
            self.scene().removeItem(group)
            self.player.hover = False
            for action in actions_lst:
                if isinstance(action, Graphics.ActionLine) and action.line_id_pk:
                    self.player.deleted_action_parts.append(action)
                elif isinstance(action, FinalActionLine) and action.f_line_action_id_pk:
                    self.player.deleted_action_parts.append(action)
                elif isinstance(action, Graphics.FinalActionArrow) and action.f_arr_action_id_pk:
                    self.player.deleted_action_parts.append(action)
            self.player.actions.pop(f'action_number:{self.action_number}')

    def hoverEnterEvent(self, event):
        if self.scene().mode == Modes.erase:
            self.setCursor(QCursor(QPixmap('://Cursors/Cursors/eraser.cur'), 0, 0))
            for action in self.player.actions[f'action_number:{self.action_number}']:
                action.hover = True
            self.player.hover = True
        else:
            self.setCursor(Qt.ArrowCursor)
            for action in self.player.actions[f'action_number:{self.action_number}']:
                action.hover = False
            self.player.hover = False

    def hoverMoveEvent(self, event):
        if self.scene().mode == Modes.erase:
            self.setCursor(QCursor(QPixmap('://Cursors/Cursors/eraser.cur'), 0, 0))
            for action in self.player.actions[f'action_number:{self.action_number}']:
                action.hover = True
            self.player.hover = True
        else:
            self.setCursor(Qt.ArrowCursor)
            for action in self.player.actions[f'action_number:{self.action_number}']:
                action.hover = False
            self.player.hover = False

    def hoverLeaveEvent(self, event):
        for action in self.player.actions[f'action_number:{self.action_number}']:
            action.hover = False
        self.player.hover = False
        self.setCursor(Qt.ArrowCursor)

    def __eq__(self, other):
        return self.f_line_action_id_pk == other.line_finish_id_pk if isinstance(other, FinalActionLineORM) else super().__eq__(other)

    def __repr__(self):
        return f'\n\t<{self.__class__.__name__} (id_pk: {self.f_line_action_id_pk}; player_id_fk: {self.player_id_fk};' \
               f' x/y: {self.x()}/{self.y()}; angle: {self.angle}; color: {self.pen.color().name()};' \
               f' action_number: {self.action_number}; action_type: {self.action_type}; player: {self.player.text}) at {hex(id(self))}>'

    def return_data(self):
        return self.f_line_action_id_pk, self.player_id_fk, self.x(), self.y(), self.angle, \
               self.pen.width(), self.pen.color().name(), self.action_number, self.action_type