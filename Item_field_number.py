from PyQt5.Qt import QGraphicsTextItem, QFont, QColor


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