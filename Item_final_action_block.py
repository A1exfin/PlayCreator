from PyQt5.Qt import *


class FinalActionBlock(QGraphicsPolygonItem):
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
        # self.hover = False
        # self.setAcceptHoverEvents(True)
        self.object_name = f'{self.player.position}_{self.action}_{self.action_number}'

    def boundingRect(self):  # Если не переопределить этот метод, при приближенном зуме итем не отображается
        return QRectF(self.x, self.y, self.w, self.h)

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        # painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        # painter.setBrush(QBrush(QColor(self.color)))
        painter.translate(self.pos)
        painter.setPen(self.pen)
        painter.rotate(-self.angle)
        painter.translate(-self.pos)
        painter.drawLine(self.line)