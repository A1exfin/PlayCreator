from PySide6.QtWidgets import QGraphicsPolygonItem, QGraphicsTextItem, QGraphicsItem
from PySide6.QtGui import QColor, QPen, QBrush, QFont
from PySide6.QtCore import Qt

__all__ = ['FieldTriangle', 'FieldNumber']


class FieldTriangle(QGraphicsPolygonItem):
    def __init__(self, polygon, color, x: float, y: float):
        super().__init__(polygon)
        self.setPos(x, y)
        self.setPen(QPen(QColor(*color), 1, s=Qt.SolidLine, c=Qt.RoundCap, j=Qt.RoundJoin))
        self.setBrush(QBrush(QColor(*color)))
        self.setOpacity(0.6)
        self.setEnabled(False)


class FieldNumber(QGraphicsTextItem):
    def __init__(self, text: str, angle: float, color, x: float, y: float):
        super().__init__(text)
        font = QFont('Times New Roman', 40)
        font.setBold(True)
        self.setFont(font)
        self.setDefaultTextColor(QColor(*color))
        self.setRotation(angle)
        self.setPos(x, y)
        self.setOpacity(0.6)
        self.setEnabled(False)
