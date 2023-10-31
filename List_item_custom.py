from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt
from Custom_scene import *


class CustomListItem(QListWidgetItem):
    def __init__(self, scene: Field, text: str):
        super().__init__(text)
        self.scene = scene
        self.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)