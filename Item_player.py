from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtGui import QColor, QPen, QPainter, QFont
from PySide6.QtCore import QPointF, QRectF, Qt


class Player(QGraphicsItem):
    '''Класс для отрисовки игроков'''
    border_width = 2
    brush_hover_color = QColor(200, 200, 200)
    brush_selected_color = QColor(130, 130, 130)

    def __init__(self, team, number, position, x, y, width, height):
        super().__init__()
        self.team = team
        if self.team == 'defence':
            self.width = width + 4  # w должна быть равна height
            self.height = height + 4  # w должна быть равна height
        else:
            self.width = width  # w должна быть равна height
            self.height = height  # w должна быть равна height
        self.position = position
        self.start_pos = None
        self.object_name = f'{team}_player_{number}_{position}'
        self.actions = {}
        self.hover = False
        self.current_action_number = 0
        # Треугольник вершиной вверх
        # self.poligon_top = (QPointF(self.width / 2 - 1.5, 3),  # Вершина
        #                     QPointF(0, self.height),  # Основание левая точка
        #                     QPointF(self.width - 3, self.height),)  # Основание правая точка
        # Треугольник вершиной вниз
        self.poligon_bot = (QPointF(self.width / 2 - 1.5, self.height - 3),  # Вершниа
                            QPointF(0, 0),  # Основание левая точка
                            QPointF(self.width - 3, 0),)  # Основание правая точка
        # Крест
        # self.line1 = QLineF(QPointF(3, 3), QPointF(self.w - 3, self.height - 3))
        # self.line2 = QLineF(QPointF(self.width - 3, 3), QPointF(3, self.height - 3))
        self.setZValue(1)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setPos(x, y)

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def paint(self, painter, option, widget=None):
        rec = self.boundingRect().adjusted(self.border_width, self.border_width, -self.border_width, -self.border_width)
        if False:
            painter = QPainter()
        painter.setFont(QFont('Times New Roman', 11))
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        if self.team == 'offence' or self.team == 'kickoff' \
                or self.team == 'punt_kick' or self.team == 'field_goal_off' or self.team == 'offence_additional':
            painter.setPen(QPen(Qt.black, self.border_width))
            if self.isSelected():
                painter.setBrush(self.brush_selected_color)
            elif self.hover:
                # painter.setPen(QPen(Qt.black, self.border_width, style=Qt.DotLine))
                painter.setBrush(self.brush_hover_color)
            else:
                painter.setBrush(Qt.white)
            if self.position == 'center':
                painter.drawRect(rec)
            else:
                painter.drawEllipse(rec)
                # painter.drawText(rec, Qt.AlignCenter, self.position)
        elif self.team == 'defence':
            if self.isSelected():
                painter.setPen(QPen(Qt.black, self.border_width))
                painter.setBrush(self.brush_selected_color)
                painter.drawEllipse(rec)
                painter.drawText(rec, Qt.AlignCenter, self.position)
            elif self.hover:
                painter.setPen(QPen(Qt.black, self.border_width))
                painter.setBrush(self.brush_hover_color)
                painter.drawEllipse(rec)
                painter.drawText(rec, Qt.AlignCenter, self.position)
            else:
                # painter.setPen(QPen(Qt.black, self.border_width))
                # painter.setBrush(Qt.white)
                painter.drawText(rec, Qt.AlignCenter, self.position)
        elif self.team == 'kick_ret' or self.team == 'punt_ret' or self.team == 'field_goal_def':
            painter.setPen(QPen(Qt.black, self.border_width))
            if self.isSelected():
                painter.setBrush(self.brush_selected_color)
            elif self.hover:
                painter.setBrush(self.brush_hover_color)
            else:
                painter.setBrush(Qt.white)
            # painter.drawLines(self.line1, self.line2)
            # painter.drawPolygon(QPolygonF(self.poligon_top))
            painter.drawPolygon(QPolygonF(self.poligon_bot))
            # painter.drawRect(self.rec)
        self.scene().update()

    def mousePressEvent(self, event):
        self.setZValue(20)
        if self.scene().mode == 'move':
            self.start_pos = event.scenePos()
            super().mousePressEvent(event)
            self.setSelected(True)
        elif (self.scene().mode == 'route' or self.scene().mode == 'block' or self.scene().mode == 'motion')\
                and not self.scene().allow_painting and event.button() == Qt.LeftButton:
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
        if self.scene().mode == 'move' or self.scene().mode == 'route' or\
                self.scene().mode == 'block' or self.scene().mode == 'motion':
            self.hover = True
        # super().hoverEnterEvent(event)

    def hoverMoveEvent(self, event):
        if self.scene().mode == 'move' or self.scene().mode == 'route' or\
                self.scene().mode == 'block' or self.scene().mode == 'motion':
            self.hover = True
        else:
            self.hover = False
        # super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event):
        self.hover = False
        # super().hoverLeaveEvent(event)

    def get_start_pos_for_action(self):
        return QPointF(self.scenePos().x() + self.width / 2, self.scenePos().y() + self.height / 2)

    def delete_actions(self):
        actions = self.actions.copy()
        for action in actions.keys():
            self.scene().removeItem(self.scene().createItemGroup(self.actions[f'{action}']))
            self.actions.pop(f'{action}')
        del actions
        self.scene().update()

    # def __del__(self):
    #     print(f'удаление {self.object_name}')