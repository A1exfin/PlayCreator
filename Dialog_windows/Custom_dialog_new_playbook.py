from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QRadioButton, QFormLayout, QVBoxLayout, QHBoxLayout, QLayout,\
    QSpacerItem, QSizePolicy, QPushButton
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

__all__ = ['DialogNewPlaybook']


class DialogNewPlaybook(QDialog):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowTitle('Новый плейбук')
        self.setFixedSize(339, 132)

        font = QFont()
        font.setPointSize(10)

        label_scheme_name = QLabel('Название плейбука:', parent=self)
        label_scheme_name.setFont(font)

        label_scheme_type = QLabel('Тип плейбука:', parent=self)
        label_scheme_type.setFont(font)

        self.line_edit = QLineEdit(parent=self)
        self.line_edit.setFont(font)

        self.radio_button_football = QRadioButton('Футбол', parent=self)
        self.radio_button_football.setFont(font)
        self.radio_button_football.setChecked(True)
        self.radio_button_flag = QRadioButton('Флаг-футбол', parent=self)
        self.radio_button_flag.setFont(font)
        self.radio_button_flag.setChecked(False)

        button_ok = QPushButton('ОК', parent=self)
        button_ok.setFont(font)
        button_ok.setFixedSize(100, 25)

        button_cancel = QPushButton('Отмена', parent=self)
        button_cancel.setFont(font)
        button_cancel.setFixedSize(100, 25)

        horizontal_layout_buttons = QHBoxLayout()
        horizontal_layout_buttons.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))
        horizontal_layout_buttons.addWidget(button_ok)
        horizontal_layout_buttons.addWidget(button_cancel)
        horizontal_layout_buttons.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))

        form_layout = QFormLayout()
        form_layout.setWidget(0, QFormLayout.LabelRole, label_scheme_name)
        form_layout.setWidget(0, QFormLayout.FieldRole, self.line_edit)
        form_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        form_layout.setRowWrapPolicy(QFormLayout.WrapLongRows)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(label_scheme_type)
        horizontal_layout.addWidget(self.radio_button_football)
        horizontal_layout.addWidget(self.radio_button_flag)
        horizontal_layout.setContentsMargins(0, 10, 0, 10)

        vertical_layout = QVBoxLayout(self)
        vertical_layout.addLayout(form_layout)
        vertical_layout.addLayout(horizontal_layout)
        vertical_layout.addLayout(horizontal_layout_buttons)
        self.line_edit.setFocus()

        button_ok.clicked.connect(self.accept)
        button_cancel.clicked.connect(self.reject)

    # def accept(self):
