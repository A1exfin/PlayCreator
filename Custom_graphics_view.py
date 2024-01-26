from PySide6.QtWidgets import QGraphicsView, QFrame
from PySide6.QtCore import Signal, QSize, Qt


class CustomGraphicsView(QGraphicsView):
    zoomChanged = Signal(int)

    def __init__(self, widget):
        super().__init__(widget)
        # self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        # self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setFrameShape(QFrame.NoFrame)
        self.setMinimumSize(1115, 780)
        self.zoom_factor = 1.2
        # self.set_current_zoom()
        self.current_zoom = 60
        self.zoom_min = 0
        self.zoom_max = 200

    def wheelEvent(self, event):
        """Увеличение или уменьшение масштаба."""
        if event.angleDelta().y() > 0 and event.modifiers() == Qt.ControlModifier:
            if self.current_zoom < self.zoom_max:
                zoom_in_value = self.current_zoom + 20
                self.set_current_zoom(zoom_in_value)
        elif event.angleDelta().y() < 0 and event.modifiers() == Qt.ControlModifier:
            if self.current_zoom > self.zoom_min:
                zoom_out_value = self.current_zoom - 20
                self.set_current_zoom(zoom_out_value)
        else:
            super().wheelEvent(event)

    def set_current_zoom(self, zoom_value):
        zoom_index = (zoom_value - self.current_zoom) / 20
        self.scale(self.zoom_factor ** zoom_index, self.zoom_factor ** zoom_index)
        self.current_zoom = zoom_value
        self.zoomChanged.emit(self.current_zoom)
