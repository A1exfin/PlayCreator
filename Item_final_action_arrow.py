from PyQt5.Qt import *


class FinalActionArrow(QGraphicsPolygonItem):
    def __init__(self, angle, pos, pen, player, mode):
        super().__init__()
        self.player = player
        self.action_number = player.current_action_number
        self.action = mode
        if False:
            self.pen = QPen()
        self.pen = pen
        self.angle = angle
        self.x = pos.x() - 10
        self.y = pos.y() - 4
        self.w = 10
        self.h = 8
        self.pos = pos
        self.polygon = QPolygonF([QPointF(pos + QPointF(0, 0)), QPointF(pos + QPointF(-10, 4)), QPointF(pos + QPointF(-10, -4))])
        # self.setAcceptHoverEvents(True)
        # self.hover = False
        self.object_name = f'{self.player.position}_{self.action}_{self.action_number}'

    def boundingRect(self):  # Если не переопределить этот метод, при приближенном зуме итем не отображается
        return QRectF(self.x, self.y, self.w, self.h)

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        # painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setBrush(QBrush(self.pen.color()))
        painter.translate(self.pos)
        painter.setPen(self.pen)
        painter.rotate(-self.angle)
        painter.translate(-self.pos)
        painter.drawPolygon(self.polygon)
        # if self.hover:
        #     painter.setBrush(QBrush(QColor(Qt.red)))
        #     self.setPen(QPen(QColor(Qt.red), self.pen.width()))
        # else:
        #     self.setPen(QPen(self.pen))
        #     painter.setBrush(QBrush(self.pen.color()))

    # def hoverEnterEvent(self, event):
    #     for action in self.player.actions[f'action_number:{self.action_number}']:
    #         action.hover = True

    # def hoverLeaveEvent(self, event):
    #     for action in self.player.actions[f'action_number:{self.action_number}']:
    #         action.hover = False