from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtGui import QColor, QPainter, QPen, QCursor, QPixmap, QBrush
from PySide6.QtCore import Qt, QRectF, QPointF
from Custom_widgets.Custom_dialog_figure_settings import DialogFigureSettings
from Enum_flags import Modes
import os


class Figure(QGraphicsItem):
    pen_hover_color = QColor('#ffcb30')
    eraser_cursor_path = f'{os.getcwd()}//Interface/Cursors/eraser.cur'

    def __init__(self, border: bool, border_color: str, border_width: int,
                 fill: bool, fill_color: str, fill_opacity: str,
                 x: float, y: float, width: float, height: float):
        super().__init__()
        self.id = None
        self.rect = QRectF(0, 0, width, height)  # Прямоугольник отрисовывается в локальных коардинатах графического итема,
        # а положение на сцене по осям X и Y задаётся для графического итема
        # self.width = width
        # self.height = height
        self.border = border
        self.border_color = border_color
        self.border_width = border_width
        self.fill = fill
        self.fill_color = fill_color
        self.fill_opacity = fill_opacity
        if self.border:
            self.pen = QPen(QColor(border_color), border_width, s=Qt.SolidLine, c=Qt.RoundCap, j=Qt.RoundJoin)
        else:
            self.pen = QPen(QColor(border_color), 0.0000001, s=Qt.SolidLine, c=Qt.RoundCap, j=Qt.RoundJoin)
        if self.fill:
            self.brush = QBrush(f'{fill_opacity}{fill_color[1:]}')
        else:
            self.brush = QBrush(Qt.transparent)
        self.__start_pos = None
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.hover = False
        self.setZValue(0)
        self.set_rect(x, y, width, height)

    def set_rect(self, x: float, y: float, width: float, height: float):
        self.setPos(x, y)
        self.rect.setRect(0, 0, width, height)

    def boundingRect(self):
        return QRectF(0, 0, self.rect.width(), self.rect.height()).adjusted(self.border_width, self.border_width, -self.border_width, -self.border_width)

    def mousePressEvent(self, event):
        print(f'{self.x() = }')
        print(f'{self.y() = }')
        print(f'{self.rect.width() = }')
        print(f'{self.rect.height() = }')
        if self.scene().mode == Modes.erase:
            self.setCursor(Qt.ArrowCursor)  # Возврат стандартного курсора сразу после клика
            self.scene().figures.remove(self)
            self.scene().removeItem(self)
        elif self.scene().mode == Modes.move:
            self.setZValue(20)
            self.__start_pos = event.scenePos()

    def mouseMoveEvent(self, event):
        if self.scene().mode == Modes.move:
            if self.__start_pos:
                delta = event.scenePos() - self.__start_pos
                self.moveBy(delta.x(), delta.y())
                self.__start_pos = event.scenePos()
        # super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.scene().mode == Modes.move:
            self.__start_pos = None
            self.setZValue(0)
        # super().mouseReleaseEvent(event)

    def hoverEnterEvent(self, event):
        if self.scene().mode == Modes.erase:
            self.hover = True
            self.setCursor(QCursor(QPixmap(self.eraser_cursor_path), 0, 0))
        elif self.scene().mode == Modes.move:
            self.hover = True

    def hoverMoveEvent(self, event):
        if self.scene().mode == Modes.erase:
            self.hover = True
            self.setCursor(QCursor(QPixmap(self.eraser_cursor_path), 0, 0))
        elif self.scene().mode == Modes.move:
            self.hover = True
            self.setCursor(Qt.ArrowCursor)
        else:
            self.hover = False
            self.setCursor(Qt.ArrowCursor)

    def hoverLeaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self.hover = False

    def mouseDoubleClickEvent(self, event):
        if self.scene().mode == Modes.move:
            dialog = DialogFigureSettings(self.scene().main_window.dialog_windows_text_color, Modes.rectangle,
                                          self.border, self.border_color, self.border_width,
                                          self.fill, self.fill_color, self.fill_opacity,
                                          parent=self.scene().main_window)
            result = dialog.exec()
            if result:
                self.border = dialog.border
                if self.border:
                    self.border_color = dialog.border_color
                    self.border_width = dialog.border_width
                    self.pen.setColor(self.border_color)
                    self.pen.setWidth(self.border_width)
                else:
                    self.pen.setWidthF(0.0000001)
                self.fill = dialog.fill
                if self.fill:
                    self.fill_color = dialog.fill_color
                    self.fill_opacity = dialog.fill_opacity
                    self.brush.setColor(QColor(f'{self.fill_opacity}{self.fill_color[1:]}'))
                else:
                    self.brush.setColor(Qt.transparent)


class Rectangle(Figure):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def paint(self, painter, option, widget=None):
        if self.scene().painting:
            rect = self.boundingRect()
        else:
            rect = self.boundingRect().adjusted(self.border_width / 2, self.border_width / 2, -self.border_width / 2, -self.border_width / 2)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setBrush(self.brush)
        if self.hover:
            painter.setPen(QPen(self.pen_hover_color, 4, self.pen.style(), self.pen.capStyle(), self.pen.joinStyle()))
        else:
            painter.setPen(self.pen)
        # painter.drawRect(self.rect)
        painter.drawRect(rect)
        self.scene().update()
