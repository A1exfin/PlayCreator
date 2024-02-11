from PySide6.QtWidgets import QGraphicsPolygonItem, QGraphicsTextItem
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QFont
from PySide6.QtCore import Qt


class FieldTriangle(QGraphicsPolygonItem):
    def __init__(self, polygon, color, x, y):
        super().__init__()
        self.color = color
        self.setPos(x, y)
        self.polygon = polygon
        self.setOpacity(0.6)

    def paint(self, painter, option, widget=None):
        painter.setRenderHints(QPainter.Antialiasing, True)
        painter.setBrush(QBrush(QColor(*self.color)))
        painter.setPen(QPen(QColor(*self.color), 1, Qt.SolidLine, c=Qt.RoundCap, j=Qt.RoundJoin))
        painter.drawPolygon(self.polygon)


class FieldNumber(QGraphicsTextItem):
    def __init__(self, text, angle, color, x, y):
        super().__init__(text)
        font = QFont('Times New Roman', 40)
        font.setBold(True)
        self.setFont(font)
        self.setDefaultTextColor(QColor(*color))
        self.setRotation(angle)
        self.setPos(x, y)
        self.setOpacity(0.6)
