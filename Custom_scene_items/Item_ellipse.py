from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtGui import QColor, QPainter, QPen, QCursor, QPixmap
from PySide6.QtCore import Qt, QRectF
from Enum_flags import Modes
import os


class Ellipse(QGraphicsEllipseItem):
    pen_hover_color = QColor('#ffcb30')
    eraser_cursor_path = f'{os.getcwd()}//Interface/Cursors/eraser.cur'

    def __init__(self, rect: QRectF, pen: QPen):
        super().__init__(rect)
        # self.setPen(pen)
        self.id = None
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
        if self.scene().mode == Modes.erase:
            self.setCursor(Qt.ArrowCursor)  # Возврат стандартного курсора сразу после клика
            self.scene().figures.remove(self)
            self.scene().removeItem(self)

    def hoverEnterEvent(self, event):
        if self.scene().mode == Modes.erase:
            self.hover = True
            self.setCursor(QCursor(QPixmap(self.eraser_cursor_path), 0, 0))

    def hoverMoveEvent(self, event):
        if self.scene().mode == Modes.erase:
            self.hover = True
            self.setCursor(QCursor(QPixmap(self.eraser_cursor_path), 0, 0))
        else:
            self.hover = False
            self.setCursor(Qt.ArrowCursor)

    def hoverLeaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self.hover = False

    def return_data(self):
        return self.id, self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height(), self.pen.width(), self.pen.color().name()