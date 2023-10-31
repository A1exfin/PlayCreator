from PySide6.QtWidgets import QGraphicsPolygonItem
from PySide6.QtGui import QColor, QPen, QPainter
from PySide6.QtCore import QPointF, QRectF, QLineF


class FinalActionBlock(QGraphicsPolygonItem):
    pen_hover_color = QColor('#ffcb30')

    def __init__(self, angle, pos, pen, player, mode):
        super().__init__()
        self.player = player
        self.action_number = player.current_action_number
        self.action = mode
        if False:
            self.pen = QPen()
        self.pen = pen
        self.angle = angle
        self.x = pos.x() - 15
        self.y = pos.y() + 7
        self.w = 15
        self.h = 14
        self.pos = pos
        self.line = QLineF(QPointF(pos + QPointF(0, -7)), QPointF(pos + QPointF(0, 7)))
        self.setAcceptHoverEvents(True)
        self.hover = False
        self.setZValue(0)
        self.object_name = f'{self.player.position}_{self.action}_{self.action_number}'

    def boundingRect(self):  # Если не переопределить этот метод, при приближенном зуме итем не отображается
        return QRectF(self.x, self.y, self.w, self.h)

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)
        # painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        if self.hover:
            painter.setPen(QPen(self.pen_hover_color, self.pen.width(), self.pen.style(), self.pen.capStyle(), self.pen.joinStyle()))
        else:
            painter.setPen(self.pen)
        painter.translate(self.pos)
        painter.rotate(-self.angle)
        painter.translate(-self.pos)
        painter.drawLine(self.line)