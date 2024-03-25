from PySide6.QtWidgets import QGraphicsView, QFrame, QStyle, QAbstractSlider, QSizePolicy
from PySide6.QtCore import Signal, Qt

__all__ = ['CustomGraphicsView']


class CustomGraphicsView(QGraphicsView):
    zoomChanged = Signal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.verticalScrollBar().setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.horizontalScrollBar().setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.setFrameShape(QFrame.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(1000, 600)
        self.zoom_factor = 1.2
        self.current_zoom = 60
        self.zoom_min = 0
        self.zoom_max = 200
        self.verticalScrollBar().actionTriggered.connect(self.scene_set_current_view_point)
        self.horizontalScrollBar().actionTriggered.connect(self.scene_set_current_view_point)

    def wheelEvent(self, event):
        """Увеличение или уменьшение масштаба."""
        if event.angleDelta().y() < 0 and event.modifiers() == Qt.ShiftModifier:
            self.horizontalScrollBar().setSliderPosition(self.horizontalScrollBar().sliderPosition() + self.horizontalScrollBar().singleStep())
        elif event.angleDelta().y() > 0 and event.modifiers() == Qt.ShiftModifier:
            self.horizontalScrollBar().setSliderPosition(self.horizontalScrollBar().sliderPosition() - self.horizontalScrollBar().singleStep())
        elif event.angleDelta().y() > 0 and event.modifiers() == Qt.ControlModifier:
            if self.current_zoom < self.zoom_max:
                zoom_in_value = self.current_zoom + 20
                self.scene_set_current_view_point()
                self.set_current_zoom(zoom_in_value)
        elif event.angleDelta().y() < 0 and event.modifiers() == Qt.ControlModifier:
            if self.current_zoom > self.zoom_min:
                zoom_out_value = self.current_zoom - 20
                self.scene_set_current_view_point()
                self.set_current_zoom(zoom_out_value)
        else:
            super().wheelEvent(event)
            self.scene_set_current_view_point()

    def scene_set_current_view_point(self):
        if self.scene():  # У установка текущей точки обзора на сцене
            self.scene().view_point = self.mapToScene(self.width() / 2, self.height() / 2)

    def set_current_zoom(self, zoom_value):
        zoom_index = (zoom_value - self.current_zoom) / 20
        self.scale(self.zoom_factor ** zoom_index, self.zoom_factor ** zoom_index)
        self.current_zoom = zoom_value
        self.zoomChanged.emit(self.current_zoom)
        if self.scene():  # Установка текущего зума на сцене
            self.scene().zoom = zoom_value
