from PyQt5.Qt import QGraphicsRectItem, QPainter, QGraphicsItem


class Rect(QGraphicsRectItem):
    def __init__(self, rect, pen):
        super().__init__(rect)
        self.setPen(pen)
        self.setZValue(0)
        # self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)

    def paint(self, painter, option, widget=None):
        painter.setRenderHints(QPainter.HighQualityAntialiasing)
        super().paint(painter, option, widget)
        self.scene().update()

    def mousePressEvent(self, event):
        if self.scene().mode == 'erase':
            self.scene().figures.remove(self)
            self.scene().removeItem(self)