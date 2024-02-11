from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QFont, QPainter, QPen, QBrush, QPolygonF, QColor, QLinearGradient
from PySide6.QtCore import Qt, QLineF, QPointF, QRectF
from Enum_flags import FillType, SymbolType


class CustomPushButtonFillType(QPushButton):
    def __init__(self, position: str, text: str, text_color: str, player_color: str, fill_type: FillType, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.position = position
        self.text = text
        self.text_color = text_color
        self.player_color = player_color
        self.fill_type = fill_type
        self.setFixedSize(40, 40)
        if self.position == 'C':
            self.rec = QRectF(7.5, 7.5, 25, 25)
        else:
            self.rec = QRectF(5, 5, 30, 30)
        self.font = QFont('Times New Roman', 9, QFont.Bold)
        self.gradient = None
        self.setStyleSheet('''
        QPushButton{
        background-color: white;}
        QPushButton:hover {
        border-color: #bbb}
        QPushButton:checked {
        border-color: red;}
        ''')
        self.set_gradient(player_color)

    def paintEvent(self, a0):
        super().paintEvent(a0)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        painter.setFont(self.font)
        painter.setBrush(QBrush(self.gradient))
        painter.setPen(QPen(QColor(self.player_color), 2))
        if self.position == 'C':
            painter.drawRect(self.rec)
        else:
            painter.drawEllipse(self.rec)
        painter.setPen(QPen(QColor(self.text_color), 2))
        painter.drawText(self.rec, Qt.AlignCenter, self.text)
        self.update()

    def set_gradient(self, player_color):
        self.player_color = player_color
        if self.fill_type == FillType.white:
            self.gradient = QLinearGradient()
            self.gradient.setStart(0, 0)
            self.gradient.setFinalStop(self.rect().right(), 0)
            self.gradient.setColorAt(0, QColor(f'#afffffff'))
        elif self.fill_type == FillType.full:
            self.gradient = QLinearGradient()
            self.gradient.setStart(0, 0)
            self.gradient.setFinalStop(self.rect().right(), 0)
            self.gradient.setColorAt(0, QColor(f'#9f{player_color[1:]}'))
        elif self.fill_type == FillType.left:
            self.gradient = QLinearGradient()
            self.gradient.setStart(self.rect().center().x(), 0)
            self.gradient.setFinalStop(self.rect().center().x() + 0.001, 0)
            self.gradient.setColorAt(0, QColor(f'#9f{player_color[1:]}'))
            self.gradient.setColorAt(1, QColor('#afffffff'))
        elif self.fill_type == FillType.right:
            self.gradient = QLinearGradient()
            self.gradient.setStart(self.rect().center().x(), 0)
            self.gradient.setFinalStop(self.rect().center().x() + 0.001, 0)
            self.gradient.setColorAt(0, QColor('#afffffff'))
            self.gradient.setColorAt(1, QColor(f'#af{player_color[1:]}'))
        elif self.fill_type == FillType.mid:
            self.gradient = QLinearGradient()
            self.gradient.setStart(0, 0)
            self.gradient.setFinalStop(self.rect().right() + 0.001, 0)
            self.gradient.setColorAt(0, QColor('#afffffff'))
            self.gradient.setColorAt(0.355, QColor('#afffffff'))
            self.gradient.setColorAt(0.356, QColor(f'#af{player_color[1:]}'))
            self.gradient.setColorAt(0.650, QColor(f'#af{player_color[1:]}'))
            self.gradient.setColorAt(0.651, QColor('#afffffff'))
            self.gradient.setColorAt(1, QColor('#afffffff'))


class CustomPushButtonSymbolType(QPushButton):
    def __init__(self, player_text: str, player_text_color: str, player_color: str,  symbol: SymbolType, parent=None):
        super().__init__(parent)
        self.player_text = player_text
        self.player_text_color = player_text_color
        self.player_color = player_color
        self.symbol = symbol
        self.setCheckable(True)
        self.setFixedSize(40, 40)
        self.rec = QRectF(0, 0, self.width(), self.height())
        self.font_letter = QFont('Times New Roman', 18)
        self.font_triangle = QFont('Times New Roman', 12)
        # Треугольник вершиной вверх
        self.poligon_top = (QPointF(self.width() / 2, 7),  # Вершина
                            QPointF(5, self.height() - 7),  # Основание левая точка
                            QPointF(self.width() - 5, self.height() - 7),)  # Основание правая точка
        # Треугольник вершиной вниз
        self.poligon_bot = (QPointF(self.width() / 2, self.height() - 7),  # Вершина
                            QPointF(5, 7),  # Основание левая точка
                            QPointF(self.width() - 5, 7),)  # Основание правая точка
        # Крест
        self.line1 = QLineF(QPointF(9, 9), QPointF(self.width() - 9, self.height() - 9))
        self.line2 = QLineF(QPointF(self.width() - 9, 9), QPointF(9, self.height() - 9))
        self.setStyleSheet('''
        QPushButton{
        background-color: white;}
        QPushButton:hover {
        border-color: #bbb}
        QPushButton:checked {
        border-color: red;}''')

    def paintEvent(self, a0):
        super().paintEvent(a0)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        painter.setBrush(Qt.white)
        if self.symbol == SymbolType.letter:
            painter.setPen(QPen(QColor(self.player_text_color)))
            painter.setFont(self.font_letter)
            painter.drawText(self.rec, Qt.AlignCenter, self.player_text)
        elif self.symbol == SymbolType.cross:
            painter.setPen(QPen(QColor(self.player_color), 2, s=Qt.SolidLine, c=Qt.RoundCap, j=Qt.RoundJoin))
            painter.drawLines([self.line1, self.line2])
        elif self.symbol == SymbolType.triangle_bot:
            painter.setPen(QPen(QColor(self.player_color), 2, s=Qt.SolidLine, c=Qt.RoundCap, j=Qt.RoundJoin))
            painter.drawPolygon(QPolygonF(self.poligon_bot))
            painter.setPen(QPen(QColor(self.player_text_color)))
            painter.setFont(self.font_triangle)
            painter.drawText(QRectF(0, -12, self.width(), self.height() + 12), Qt.AlignCenter, self.player_text)
        elif self.symbol == SymbolType.triangle_top:
            painter.setPen(QPen(QColor(self.player_color), 2, s=Qt.SolidLine, c=Qt.RoundCap, j=Qt.RoundJoin))
            painter.drawPolygon(QPolygonF(self.poligon_top))
            painter.setPen(QPen(QColor(self.player_text_color)))
            painter.setFont(self.font_triangle)
            painter.drawText(QRectF(0, 10, self.width(), self.height() - 10), Qt.AlignCenter, self.player_text)
        self.update()