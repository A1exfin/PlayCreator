from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Player(QGraphicsItem):
    '''Класс для отрисовки игроков'''
    border_width = 2

    def __init__(self, team, number, position, x, y, w, h):
        super().__init__()
        self.team = team
        if self.team == 'defence':
            self.w = w + 4  # w должна быть равна h
            self.h = h + 4  # w должна быть равна h
        else:
            self.w = w  # w должна быть равна h
            self.h = h  # w должна быть равна h
        self.position = position
        self.start_pos = None
        self.object_name = f'{team}_player_{number}_{position}'
        self.actions = {}
        self.current_action_number = 0
        self.setZValue(1)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setPos(x, y)

    def boundingRect(self):
        return QRectF(0, 0, self.w, self.h)

    def paint(self, painter, option, widget=None):
        rec = self.boundingRect().adjusted(self.border_width, self.border_width, -self.border_width, -self.border_width)
        if False:
            painter = QPainter()
        # Треугольник вершиной вверх
        # poligon_top = (QPointF(self.w / 2 - 1.5, 3),  # Вершина
        #                QPointF(0, self.h),  # Основание левая точка
        #                QPointF(self.w - 3, self.h),)  # Основание правая точка
        # Треугольник вершиной вниз
        poligon_bot = (QPointF(self.w / 2 - 1.5, self.h - 3),  # Вершниа
                       QPointF(0, 0),  # Основание левая точка
                       QPointF(self.w - 3, 0),)  # Основание правая точка
        # Крест
        # line1 = QLineF(QPointF(3, 3), QPointF(self.w - 3, self.h - 3))
        # line2 = QLineF(QPointF(self.w - 3, 3), QPointF(3, self.h - 3))
        painter.setFont(QFont('Times New Roman', 11))
        painter.setRenderHints(QPainter.HighQualityAntialiasing)

        if self.team == 'offence' or self.team == 'kickoff' \
                or self.team == 'punt_kick' or self.team == 'field_goal_off':
            painter.setPen(QPen(Qt.black, self.border_width))
            if self.isSelected():
                painter.setBrush(Qt.gray)
            else:
                painter.setBrush(Qt.white)
            if self.position == 'center':
                painter.drawRect(rec)
            else:
                painter.drawEllipse(rec)
        elif self.team == 'defence':
            if self.isSelected():
                painter.setPen(QPen(Qt.black, self.border_width))
                painter.setBrush(Qt.gray)
                painter.drawEllipse(rec)
                painter.drawText(rec, Qt.AlignCenter, self.position)
            else:
                # painter.setPen(QPen(Qt.black, self.border_width))
                # painter.setBrush(Qt.white)
                painter.drawText(rec, Qt.AlignCenter, self.position)
        elif self.team == 'kick_ret' or self.team == 'punt_ret' or self.team == 'field_goal_def':
            painter.setPen(QPen(Qt.black, self.border_width))
            if self.isSelected():
                painter.setBrush(Qt.gray)
            else:
                painter.setBrush(Qt.white)
            # painter.drawLines(line1, line2)
            # painter.drawPolygon(QPolygonF(poligon_top))
            painter.drawPolygon(QPolygonF(poligon_bot))
            # painter.drawRect(self.rec)

    def mousePressEvent(self, event):
        self.setZValue(20)
        if self.scene().mode == 'move':
            self.start_pos = event.scenePos()
            super().mousePressEvent(event)
            self.setSelected(True)
        elif (self.scene().mode == 'route' or self.scene().mode == 'block' or self.scene().mode == 'motion') and not self.scene().allow_painting and event.button() == Qt.LeftButton:
            self.setSelected(True)
            self.scene().allow_painting = True
            self.scene().current_player = self
            self.scene().player_center_pos = self.get_start_pos_for_action()
        elif event.button() == Qt.RightButton:  # Для того чтобы маршрут не рисовался от игрока по которому кликнули правой кнопкой
            self.ungrabMouse()

    def mouseMoveEvent(self, event):
        self.delete_actions()
        if self.scene().mode == 'move':
            if self.start_pos:
                delta_x = event.scenePos().x() - self.start_pos.x()
                delta_y = event.scenePos().y() - self.start_pos.y()
                self.moveBy(delta_x, delta_y)
                self.start_pos = QPointF(event.scenePos())
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.setZValue(1)
        if self.scene().mode == 'move':
            self.start_pos = None
            super().mouseReleaseEvent(event)
            self.setSelected(False)

    def mouseDoubleClickEvent(self, event):
        '''обязательно переопределить чтобы не срабатывал двойной клик за пределами сцены,
        который считается кликом по игроку (не знаю почему так работает)'''
        self.ungrabMouse()

    def hoverEnterEvent(self, event):
        super().hoverEnterEvent(event)

    def hoverMoveEvent(self, event):
        # print(self.hasFocus())
        super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event):
        super().hoverLeaveEvent(event)

    def get_start_pos_for_action(self):
        return QPointF(self.scenePos().x() + self.w / 2, self.scenePos().y() + self.h / 2)

    def delete_actions(self):
        actions = self.actions.copy()
        for action in actions.keys():
            self.scene().removeItem(self.scene().createItemGroup(self.actions[f'{action}']))
            self.actions.pop(f'{action}')
        actions.clear()
        self.scene().update()