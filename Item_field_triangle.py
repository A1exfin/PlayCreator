from PyQt5.Qt import *


class FieldTriangle(QGraphicsPolygonItem):
    def __init__(self, polygon, color, x, y):
        super().__init__()
        self.color = color
        self.setPos(x, y)
        self.polygon = polygon
        self.setOpacity(0.6)

    def paint(self, painter, option, widget=None):
        painter.setRenderHints(QPainter.Antialiasing, True)
        painter.setRenderHints(QPainter.HighQualityAntialiasing, True)
        painter.setBrush(QBrush(QColor(*self.color)))
        painter.setPen(QPen(QColor(*self.color), 1, Qt.SolidLine, cap=Qt.RoundCap, join=Qt.RoundJoin))
        painter.drawPolygon(self.polygon)
