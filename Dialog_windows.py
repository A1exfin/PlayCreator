from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QRadioButton, QDialogButtonBox, QFormLayout, QVBoxLayout,\
    QHBoxLayout, QLayout, QSpacerItem, QSizePolicy
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt


class DialogNewSchemeAction(QDialog):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowTitle('Новая схема')
        self.setFixedSize(339, 132)

        font = QFont()
        font.setPointSize(10)

        label_scheme_name = QLabel()
        label_scheme_name.setFont(font)
        label_scheme_name.setText('Название схемы:')

        label_scheme_type = QLabel()
        label_scheme_type.setFont(font)
        label_scheme_type.setText('Тип схемы:')

        self.line_edit = QLineEdit()
        self.line_edit.setFont(font)

        self.radio_button_football = QRadioButton('Футбол')
        self.radio_button_football.setFont(font)
        self.radio_button_football.setChecked(True)
        self.radio_button_flag = QRadioButton('Флаг-футбол')
        self.radio_button_flag.setFont(font)
        self.radio_button_flag.setChecked(False)

        button_box = QDialogButtonBox(self)
        button_box.setFont(font)
        button_box.setOrientation(Qt.Horizontal)
        button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        button_box.setCenterButtons(True)
        button_box.setFont(font)

        form_layout = QFormLayout()
        form_layout.setWidget(0, QFormLayout.LabelRole, label_scheme_name)
        form_layout.setWidget(0, QFormLayout.FieldRole, self.line_edit)
        form_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        form_layout.setRowWrapPolicy(QFormLayout.WrapLongRows)

        # group_box = QGroupBox(self)
        # horizontal_layout = QHBoxLayout(group_box)
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(label_scheme_type)
        horizontal_layout.addWidget(self.radio_button_football)
        horizontal_layout.addWidget(self.radio_button_flag)
        horizontal_layout.setContentsMargins(0, 10, 0, 10)
        # group_box.setStyleSheet('''margin-top: 10px;
        # margin-bottom: 10px''')

        vertical_layout = QVBoxLayout(self)
        vertical_layout.addLayout(form_layout)
        # vertical_layout.addWidget(group_box)
        vertical_layout.addLayout(horizontal_layout)
        vertical_layout.addWidget(button_box)
        self.line_edit.setFocus()

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)


class DialogAbout(QDialog):
    def __init__(self, version: str, ico: str, color: str, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowTitle('PlayCreator')

        label_ico = QLabel(self)
        label_ico.setPixmap(QPixmap(ico))

        font = QFont()
        font.setPointSize(14)
        font.setBold(True)

        label_text_pc = QLabel('PlayCreator')
        label_text_pc.setFont(font)
        label_text_pc.setStyleSheet(f'color: {color}; margin-bottom: 20px')

        font = QFont()
        font.setPointSize(12)

        label_text_version = QLabel(f'Версия: {version}', self)
        label_text_version.setFont(font)
        label_text_version.setStyleSheet('margin-bottom: 20px')

        label_text_developer = QLabel('Разработчик: Халеев Александр', self)
        label_text_developer.setFont(font)
        label_text_developer.setStyleSheet('margin-bottom: 5px')

        text = 'Обратная связь. Email: alexfin16@gmail.com;\tVK:<a href=https://vk.com/alexn11>Халеев Александр</a>'
        label_text_feedback = QLabel(text, self)
        label_text_feedback.setFont(font)
        label_text_feedback.setTextFormat(Qt.RichText)
        label_text_feedback.setTextInteractionFlags(Qt.TextBrowserInteraction)
        label_text_feedback.setOpenExternalLinks(True)
        label_text_feedback.setStyleSheet('margin-bottom: 5px')

        button_box = QDialogButtonBox(self)
        button_box.setFont(font)
        button_box.setOrientation(Qt.Horizontal)
        button_box.setStandardButtons(QDialogButtonBox.Ok)
        button_box.setCenterButtons(True)
        button_box.setFont(font)

        vertical_layout_ico = QVBoxLayout()
        vertical_layout_ico.addWidget(label_ico)
        vertical_layout_ico.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))

        horizontal_layout_pc_version = QHBoxLayout()
        horizontal_layout_pc_version.addWidget(label_text_pc)
        horizontal_layout_pc_version.addWidget(label_text_version)
        horizontal_layout_pc_version.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))

        vertical_layout_text = QVBoxLayout()
        vertical_layout_text.addLayout(horizontal_layout_pc_version)
        vertical_layout_text.addWidget(label_text_developer)
        vertical_layout_text.addWidget(label_text_feedback)
        vertical_layout_text.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addLayout(vertical_layout_ico)
        horizontal_layout.addLayout(vertical_layout_text)

        vertical_layout_3 = QVBoxLayout(self)
        vertical_layout_3.addLayout(horizontal_layout)
        vertical_layout_3.addWidget(button_box)

        button_box.accepted.connect(self.accept)