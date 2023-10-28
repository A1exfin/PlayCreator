from PyQt5 import QtWidgets
from PyQt5.Qt import *
from Custom_scene import Field


class CustomListItem(QListWidgetItem):
    def __init__(self, scene: Field, text: str):
        super().__init__(text)
        self.scene = scene
        self.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)