from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QBrush, QPen, QColor
from PySide6.QtCore import Qt
from Enums import Modes


class CustomWidget(QWidget):
    def __init__(self, figure_type: Modes, border_color: str, border_width: int, fill_color: str, fill_opacity: str,
                 parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.figure_type = figure_type
        self.pen = QPen(QColor(border_color), border_width)
        self.brush = QBrush(QColor(f'{fill_opacity}{fill_color[1:]}'))
        self.setFixedSize(300, 300)

    def set_brush(self, opacity: str, color: str):
        self.brush.setColor(f'{opacity}{color[1:]}')

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QBrush(QColor(Qt.white)))
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        if self.figure_type == Modes.rectangle:
            painter.drawRect(50, 50, 200, 200)
        elif self.figure_type == Modes.ellipse:
            painter.drawEllipse(50, 50, 200, 200)

