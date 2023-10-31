from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsTextItem
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QCursor, QPixmap, QFont
from PySide6.QtCore import Qt


class Rect(QGraphicsRectItem):
    pen_hover_color = QColor('#ffcb30')

    def __init__(self, rect, pen):
        super().__init__(rect)
        # self.setPen(pen)
        self.pen = pen
        self.setAcceptHoverEvents(True)
        self.hover = False
        self.setZValue(0)
        # self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)

    def paint(self, painter, option, widget=None):
        painter.setRenderHints(QPainter.Antialiasing)
        if self.hover:
            self.setPen(QPen(self.pen_hover_color, self.pen.width(), self.pen.style(), self.pen.capStyle(), self.pen.joinStyle()))
        else:
            self.setPen(QPen(self.pen))
        super().paint(painter, option, widget)
        self.scene().update()

    def mousePressEvent(self, event):
        if self.scene().mode == 'erase':
            self.setCursor(Qt.ArrowCursor)  # Возврат стандартного курсора сразу после клика
            self.scene().figures.remove(self)
            self.scene().removeItem(self)

    def hoverEnterEvent(self, event):
        if self.scene().mode == 'erase':
            self.hover = True
            self.setCursor(QCursor(QPixmap('Interface/Cursors/eraser.cur'), 0, 0))

    def hoverMoveEvent(self, event):
        if self.scene().mode == 'erase':
            self.hover = True
            self.setCursor(QCursor(QPixmap('Interface/Cursors/eraser.cur'), 0, 0))
        else:
            self.hover = False
            self.setCursor(Qt.ArrowCursor)

    def hoverLeaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self.hover = False


class Ellipse(QGraphicsEllipseItem):
    pen_hover_color = QColor('#ffcb30')

    def __init__(self, rect, pen):
        super().__init__(rect)
        # self.setPen(pen)
        self.pen = pen
        self.setAcceptHoverEvents(True)
        self.hover = False
        self.setZValue(0)
        # self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)

    def paint(self, painter, option, widget=None):
        painter.setRenderHints(QPainter.Antialiasing)
        if self.hover:
            self.setPen(QPen(self.pen_hover_color, self.pen.width(), self.pen.style(), self.pen.capStyle(), self.pen.joinStyle()))
        else:
            self.setPen(QPen(self.pen))
        super().paint(painter, option, widget)
        self.scene().update()

    def mousePressEvent(self, event):
        if self.scene().mode == 'erase':
            self.setCursor(Qt.ArrowCursor)  # Возврат стандартного курсора сразу после клика
            self.scene().figures.remove(self)
            self.scene().removeItem(self)

    def hoverEnterEvent(self, event):
        if self.scene().mode == 'erase':
            self.hover = True
            self.setCursor(QCursor(QPixmap('Interface/Cursors/eraser.cur'), 0, 0))

    def hoverMoveEvent(self, event):
        if self.scene().mode == 'erase':
            self.hover = True
            self.setCursor(QCursor(QPixmap('Interface/Cursors/eraser.cur'), 0, 0))
        else:
            self.hover = False
            self.setCursor(Qt.ArrowCursor)

    def hoverLeaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self.hover = False


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
