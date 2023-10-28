from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.Qt import *


class CustomGraphicsView(QGraphicsView):
    zoomChanged = pyqtSignal(int)

    def __init__(self, widget):
        super().__init__(widget)
        # self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        # self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setMinimumSize(QtCore.QSize(859, 741))
        self.zoom_factor = 1.25
        # self.set_current_zoom()
        self.current_zoom = 60
        self.zoom_min = 0
        self.zoom_max = 200

    def wheelEvent(self, event):
        """Увеличение или уменьшение масштаба."""
        zoomInFactor = self.zoom_factor
        zoomOutFactor = 1 / self.zoom_factor
        # Zoom
        if event.angleDelta().y() > 0 and event.modifiers() == Qt.ControlModifier:
            if self.current_zoom < self.zoom_max:
                zoomFactor = zoomInFactor
                # self.current_zoom += 20
                self.increase_zoom()
                self.scale(zoomFactor, zoomFactor)
        elif event.angleDelta().y() < 0 and event.modifiers() == Qt.ControlModifier:
            if self.current_zoom > self.zoom_min:
                zoomFactor = zoomOutFactor
                # self.current_zoom -= 20
                self.decrease_zoom()
                self.scale(zoomFactor, zoomFactor)
        else:
            super().wheelEvent(event)

    def increase_zoom(self):
        self.current_zoom += 20
        self.zoomChanged.emit(self.current_zoom)

    def decrease_zoom(self):
        self.current_zoom -= 20
        self.zoomChanged.emit(self.current_zoom)

    # def set_current_zoom(self):
    #     self.current_zoom = 60
    #     self.valueChanged.emit(self.current_zoom)
