from PySide6.QtWidgets import QGraphicsLineItem
from PySide6.QtGui import QColor, QPen, QPainter, QCursor, QPixmap
from PySide6.QtCore import QLineF, Qt
from Item_player import Player


class ActionLine(QGraphicsLineItem):
    pen_hover_color = QColor('#ffcb30')

    def __init__(self, line: QLineF, pen: QPen, player: Player, mode: str):
        super().__init__(line)
        self.player = player
        if False:
            self.pen = QPen()
        self.pen = pen
        self.setAcceptHoverEvents(True)
        self.action_number = player.current_action_number
        self.action = mode
        self.hover = False
        self.setZValue(0)
        self.object_name = f'{self.player.position}_{self.action}_{self.action_number}'

    def mousePressEvent(self, event):
        self.ungrabMouse()
        if self.scene().mode == 'route' and (self.action == 'route' or self.action == 'motion') and event.button() == Qt.LeftButton:
            self.scene().allow_painting = True
            self.scene().start_pos = event.scenePos()
            self.player.setSelected(True)
            self.scene().current_player = self.player
            self.scene().action_number_temp = self.action_number
            self.scene().action_number_temp, self.player.current_action_number \
                = self.player.current_action_number, self.scene().action_number_temp
        elif self.scene().mode == 'block' and self.action == 'motion' and event.button() == Qt.LeftButton:
            self.scene().allow_painting = True
            self.scene().start_pos = event.scenePos()
            self.player.setSelected(True)
            self.scene().current_player = self.player
            self.scene().action_number_temp = self.action_number
            self.scene().action_number_temp, self.player.current_action_number \
                = self.player.current_action_number, self.scene().action_number_temp
        elif self.scene().mode == 'erase':
            self.setCursor(Qt.ArrowCursor)  # Возврат стандартного курсора сразу после клика
            group = self.scene().createItemGroup(self.player.actions[f'action_number:{self.action_number}'])
            self.scene().removeItem(group)
            self.player.hover = False
            self.player.actions.pop(f'action_number:{self.action_number}')

    def mouseDoubleClickEvent(self, event):
        '''обязательно переопределить чтобы не срабатывал двойной клик за пределами сцены,
        который считается кликом по линии (не знаю почему так работает)'''
        self.ungrabMouse()

    def paint(self, painter, option, widget=None):
        painter.setRenderHints(QPainter.Antialiasing)
        if self.hover:
            self.setPen(QPen(self.pen_hover_color, self.pen.width(), self.pen.style(), self.pen.capStyle(), self.pen.joinStyle()))
        else:
            self.setPen(QPen(self.pen))
        super().paint(painter, option, widget)
        self.scene().update()  # Нужно для полного удаления действия со сцены СРАЗУ после клика по линии

    def hoverEnterEvent(self, event):
        if (self.action == 'route' and self.scene().mode == 'route') or\
                (self.action == 'motion' and (self.scene().mode == 'route' or self.scene().mode == 'block')) or\
                self.scene().mode == 'erase':
            for action in self.player.actions[f'action_number:{self.action_number}']:
                action.hover = True
            self.player.hover = True
        if self.scene().mode == 'erase':
            self.setCursor(QCursor(QPixmap('Interface/Cursors/eraser.cur'), 0, 0))

    def hoverMoveEvent(self, event):
        if (self.action == 'route' and self.scene().mode == 'route') or\
                (self.action == 'motion' and (self.scene().mode == 'route' or self.scene().mode == 'block')) or\
                self.scene().mode == 'erase':
            for action in self.player.actions[f'action_number:{self.action_number}']:
                action.hover = True
            self.player.hover = True
        else:
            for action in self.player.actions[f'action_number:{self.action_number}']:
                action.hover = False
            self.player.hover = False
        if self.scene().mode == 'erase':
            self.setCursor(QCursor(QPixmap('Interface/Cursors/eraser.cur'), 0, 0))
        else:
            self.setCursor(Qt.ArrowCursor)

    def hoverLeaveEvent(self, event):
        for action in self.player.actions[f'action_number:{self.action_number}']:
            action.hover = False
        self.player.hover = False
        self.setCursor(Qt.ArrowCursor)
