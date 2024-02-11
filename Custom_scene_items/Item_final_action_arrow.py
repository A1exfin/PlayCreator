from PySide6.QtWidgets import QGraphicsPolygonItem
from PySide6.QtGui import QColor, QPen, QPainter, QBrush, QPolygonF
from PySide6.QtCore import QPointF, QRectF
from Custom_scene_items.Item_player import Player
from Enum_flags import Modes


class FinalActionArrow(QGraphicsPolygonItem):
    pen_hover_color = QColor('#ffcb30')
    brush_hover_color = QColor('#ffcb30')

    def __init__(self, angle: float, pos: QPointF, pen: QPen, player: Player, mode: Modes):
        super().__init__()
        self.id = None
        self.player = player
        self.action_number = player.current_action_number
        self.action = mode
        self.pen = pen
        self.angle = angle
        self.x = pos.x() - 10
        self.y = pos.y() - 4
        self.w = 10
        self.h = 8
        self.pos = pos
        self.polygon = QPolygonF([QPointF(pos + QPointF(0, 0)), QPointF(pos + QPointF(-10, 4)), QPointF(pos + QPointF(-10, -4))])
        self.setAcceptHoverEvents(True)
        self.hover = False
        self.setZValue(1)
        self.object_name = f'{self.player.position}_{self.action}_{self.action_number}'

    def boundingRect(self):  # Если не переопределить этот метод, при приближенном зуме итем не отображается
        return QRectF(self.x, self.y, self.w, self.h)

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)
        # painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        if self.hover:
            painter.setPen(QPen(self.pen_hover_color, self.pen.width(), self.pen.style(), self.pen.capStyle(), self.pen.joinStyle()))
            painter.setBrush(self.brush_hover_color)
        else:
            painter.setPen(self.pen)
            painter.setBrush(QBrush(self.pen.color()))
        painter.translate(self.pos)
        painter.rotate(-self.angle)
        painter.translate(-self.pos)
        painter.drawPolygon(self.polygon)

    # def hoverEnterEvent(self, event):
    #     for action in self.player.actions[f'action_number:{self.action_number}']:
    #         action.hover = True
    #
    # def hoverLeaveEvent(self, event):
    #     for action in self.player.actions[f'action_number:{self.action_number}']:
    #         action.hover = False

    def return_data(self):
        return self.id, self.action_number, self.angle, self.pen.width(), self.pen.color().name(), self.action, self.x, self.y