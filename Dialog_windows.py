from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QRadioButton, QDialogButtonBox, QFormLayout, QVBoxLayout,\
    QHBoxLayout, QGridLayout, QLayout, QSpacerItem, QSizePolicy, QPushButton, QButtonGroup, QGroupBox
from PySide6.QtGui import QFont, QPixmap, QPainter, QPen, QBrush, QPolygonF, QColor, QLinearGradient
from PySide6.QtCore import Qt, QLineF, QPointF, QRectF


class DialogLogIn(QDialog):
    def __init__(self, text_color: str, parent=None, flags=Qt.WindowFlags(), wrong_login_pass=False):
        super().__init__(parent, flags)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowTitle('Вход')
        self.setFixedSize(480, 580)
        self.setStyleSheet(f'color: {text_color}')

        font = QFont()
        font.setPointSize(10)
        font.setBold(True)

        label_login_title = QLabel('Вход')
        label_login_title.setFont(font)
        label_login_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_login = QLabel('Логин: ')
        label_login.setFont(font)
        label_login.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        label_password = QLabel('Пароль: ')
        label_password.setFont(font)
        label_password.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.button_login = QPushButton('Войти')
        self.button_login.setFont(font)
        self.button_login.setFixedSize(130, 30)

        self.button_sign_up = QPushButton('Зарегистрироваться')
        self.button_sign_up.setFont(font)
        self.button_sign_up.setFixedSize(266, 30)

        self.button_offline = QPushButton('Оффлайн')
        self.button_offline.setFont(font)
        self.button_offline.setFixedSize(130, 30)

        font.setPointSize(14)
        label_wrong_login_or_password = QLabel()
        label_wrong_login_or_password.setFont(font)
        label_wrong_login_or_password.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if wrong_login_pass:
            label_wrong_login_or_password.setText('Неверный логин или пароль')
        # label_wrong_login_or_password.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        font.setBold(False)
        self.line_edit_login = QLineEdit()
        self.line_edit_login.setMinimumSize(250, 30)
        self.line_edit_login.setFont(font)
        self.line_edit_login.setText('admin')

        self.line_edit_password = QLineEdit()
        self.line_edit_password.setMinimumSize(250, 30)
        self.line_edit_password.setFont(font)
        self.line_edit_password.setText('admin')
        self.line_edit_password.setEchoMode(QLineEdit.Password)

        horizontal_layout_buttons = QHBoxLayout()
        horizontal_layout_buttons.addWidget(self.button_login)
        horizontal_layout_buttons.addWidget(self.button_offline)

        vertical_layout_all = QVBoxLayout()
        # vertical_layout_all.addWidget(label_wrong_login_or_password)
        vertical_layout_all.addWidget(label_login)
        vertical_layout_all.addWidget(self.line_edit_login)
        vertical_layout_all.addWidget(label_password)
        vertical_layout_all.addWidget(self.line_edit_password)
        vertical_layout_all.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))  # отступ кнопок от полей ввода
        vertical_layout_all.addLayout(horizontal_layout_buttons)
        vertical_layout_all.addWidget(self.button_sign_up, 0, Qt.AlignmentFlag.AlignHCenter)

        horizontal_layout_main = QHBoxLayout()
        horizontal_layout_main.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))
        horizontal_layout_main.addLayout(vertical_layout_all)
        horizontal_layout_main.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))

        vertical_layout_main = QVBoxLayout(self)
        vertical_layout_main.addWidget(label_wrong_login_or_password)
        vertical_layout_main.addSpacerItem(QSpacerItem(40, 80, QSizePolicy.Expanding, QSizePolicy.Fixed))  # отступ сверху окна
        vertical_layout_main.addLayout(horizontal_layout_main)
        vertical_layout_main.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.button_login.clicked.connect(self.accept)
        self.button_offline.clicked.connect(self.reject)
        self.button_sign_up.clicked.connect(lambda: self.done(2))

        # self.button_sign_up.setEnabled(False)#############
        # self.button_login.setEnabled(False)##############
        # self.line_edit_login.setEnabled(False)##################
        # self.line_edit_password.setEnabled(False)##############################


class DialogSignUp(QDialog):
    def __init__(self, color: str, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowTitle('Вход')
        self.setFixedSize(339, 132)
        self.setStyleSheet(f'color: {color}')

        font = QFont()
        font.setPointSize(14)
        font.setBold(True)

        label_sign_up_title = QLabel('Регистрация')
        label_sign_up_title.setFont(font)
        label_sign_up_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # label_sign_up_title.setStyleSheet('color: #27c727')

        label_login = QLabel('Логин: ')
        label_login.setFont(font)
        # label_login.setStyleSheet('color: #27c727')

        label_email = QLabel('Email: ')
        label_email.setFont(font)
        # label_email.setStyleSheet('color: #27c727')

        label_password = QLabel('Пароль: ')
        label_password.setFont(font)
        # label_password.setStyleSheet('color: #27c727')

        self.line_edit_login = QLineEdit()
        self.line_edit_login.setFont(font)

        self.line_edit_email = QLineEdit()
        self.line_edit_email.setFont(font)

        self.line_edit_password = QLineEdit()
        self.line_edit_password.setFont(font)

        self.button_sign_up = QPushButton('Зарегистрироваться')
        self.button_sign_up.setFont(font)
        self.button_sign_up.setStyleSheet('min-width: 150px; min-height: 25px;')

        form_layout = QFormLayout()
        form_layout.setWidget(0, QFormLayout.LabelRole, label_login)
        form_layout.setWidget(0, QFormLayout.FieldRole, self.line_edit_login)
        form_layout.setWidget(1, QFormLayout.LabelRole, label_email)
        form_layout.setWidget(1, QFormLayout.FieldRole, self.line_edit_email)
        form_layout.setWidget(2, QFormLayout.LabelRole, label_password)
        form_layout.setWidget(2, QFormLayout.FieldRole, self.line_edit_password)
        form_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        form_layout.setRowWrapPolicy(QFormLayout.WrapLongRows)

        vertical_layout_main = QVBoxLayout(self)
        vertical_layout_main.addWidget(label_sign_up_title)
        vertical_layout_main.addLayout(form_layout)
        vertical_layout_main.addWidget(self.button_sign_up)


class DialogNewPlaybook(QDialog):
    def __init__(self, text_color: str, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowTitle('Новый плейбук')
        self.setFixedSize(339, 132)
        self.setStyleSheet(f'color: {text_color}')

        font = QFont()
        font.setPointSize(10)

        label_scheme_name = QLabel('Название плейбука:')
        label_scheme_name.setFont(font)

        label_scheme_type = QLabel('Тип плейбука:')
        label_scheme_type.setFont(font)

        self.line_edit = QLineEdit()
        self.line_edit.setFont(font)

        self.radio_button_football = QRadioButton('Футбол')
        self.radio_button_football.setFont(font)
        self.radio_button_football.setChecked(True)
        self.radio_button_flag = QRadioButton('Флаг-футбол')
        self.radio_button_flag.setFont(font)
        self.radio_button_flag.setChecked(False)

        button_ok = QPushButton('ОК')
        button_ok.setFont(font)
        button_ok.setFixedSize(100, 25)

        button_cancel = QPushButton('Отмена')
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


class DialogAbout(QDialog):
    def __init__(self, version: str, ico: str, text_color: str, parent=None, flags=Qt.WindowFlags()):
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
        label_text_pc.setStyleSheet(f'color: {text_color}; margin-bottom: 20px')

        font = QFont()
        font.setPointSize(12)

        label_text_version = QLabel(f'Версия: {version}', self)
        label_text_version.setFont(font)
        label_text_version.setStyleSheet('margin-bottom: 20px')

        label_text_developer = QLabel('Разработчик: Халеев Александр', self)
        label_text_developer.setFont(font)
        label_text_developer.setStyleSheet('margin-bottom: 5px')

        text = 'Обратная связь. Email: alexfin16@gmail.com;\tVK: <a href=https://vk.com/alexn11>Халеев Александр</a>'
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


class DialogPlayerSettings(QDialog):
    COLORS = ('#000000', '#800000', '#400080', '#0004ff', '#8d8b9a', '#22b14c',
              '#ff0000', '#ff00ea', '#ff80ff', '#ff8000', '#dcdc00', '#00ff00')

    def __init__(self, window_text_color: str, player_text: str, player_text_color: str, player_color: str, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(390, 400)
        self.setWindowTitle('Настройки игрока')
        self.setStyleSheet(f'color: {window_text_color};')

        self.font = QFont()

        self.font.setPointSize(14)
        self.font.setBold(True)
        self.line_edit_player_position = QLineEdit()
        self.line_edit_player_position.setFont(self.font)
        self.line_edit_player_position.setMaxLength(2)
        self.line_edit_player_position.setText(player_text)
        self.line_edit_player_position.setContentsMargins(5, 5, 5, 0)
        self.line_edit_player_position.setStyleSheet('QLineEdit:disabled{color: #334e3a;}')

        groupbox_stylesheet = '''
        QGroupBox {border: 2px solid gray; border-radius: 5px; padding-top: 3px; margin-top: 8px;}
        QGroupBox::title {subcontrol-origin: margin; subcontrol-position: top left; left: 15px;}'''

        self.font.setPointSize(10)
        self.font.setBold(False)
        self.group_box_position = QGroupBox('Позиция игрока')
        self.group_box_position.setFont(self.font)
        self.group_box_position.setFixedSize(244, 73)
        self.group_box_position.setStyleSheet(groupbox_stylesheet)

        self.group_box_text_color = QGroupBox('Цвет текста')
        self.group_box_text_color.setFont(self.font)
        self.group_box_text_color.setFixedSize(244, 73)
        self.group_box_text_color.setStyleSheet(groupbox_stylesheet)

        self.group_box_player_color = QGroupBox()
        self.group_box_player_color.setFont(self.font)
        self.group_box_player_color.setFixedSize(244, 73)
        self.group_box_player_color.setStyleSheet(groupbox_stylesheet)

        self.group_box_fill_symbol_type = QGroupBox()
        self.group_box_fill_symbol_type.setFont(self.font)
        self.group_box_fill_symbol_type.setFixedSize(244, 73)
        self.group_box_fill_symbol_type.setStyleSheet(groupbox_stylesheet)

        self.button_group_fill_symbol_type = QButtonGroup(self)
        self.button_group_fill_symbol_type.setExclusive(True)

        button_ok = QPushButton('ОК')
        button_ok.setFont(self.font)
        button_ok.setFixedSize(100, 25)

        button_cancel = QPushButton('Отмена')
        button_cancel.setFont(self.font)
        button_cancel.setFixedSize(100, 25)

        self.push_button_current_text_color = QPushButton()
        self.push_button_current_text_color.setFixedSize(40, 40)
        self.push_button_current_text_color.setStyleSheet(f'background-color: {player_text_color}')

        self.push_button_current_player_color = QPushButton()
        self.push_button_current_player_color.setFixedSize(40, 40)
        self.push_button_current_player_color.setStyleSheet(f'background-color: {player_color}')

        horizontal_layout_position = QVBoxLayout(self.group_box_position)
        horizontal_layout_position.addWidget(self.line_edit_player_position)

        grid_layout_text_colors = QGridLayout()
        grid_layout_text_colors.setSpacing(2)
        for i, color in enumerate(self.COLORS):
            setattr(self, f'button_text_color_{i}', QPushButton())
            getattr(self, f'button_text_color_{i}').setFixedSize(18, 18)
            getattr(self, f'button_text_color_{i}').setStyleSheet(f'background-color: {color}')
            if i < len(self.COLORS) / 2:
                row = 0
                column = i + 1
            else:
                row = 1
                column = i + 1 - len(self.COLORS) / 2
            grid_layout_text_colors.addWidget(getattr(self, f'button_text_color_{i}'), row, column, 1, 1)

        grid_layout_player_colors = QGridLayout()
        grid_layout_player_colors.setSpacing(2)
        for i, color in enumerate(self.COLORS):
            setattr(self, f'button_player_color_{i}', QPushButton())
            getattr(self, f'button_player_color_{i}').setFixedSize(18, 18)
            getattr(self, f'button_player_color_{i}').setStyleSheet(f'background-color: {color}')
            if i < len(self.COLORS) / 2:
                row = 0
                column = i + 1
            else:
                row = 1
                column = i + 1 - len(self.COLORS) / 2
            grid_layout_player_colors.addWidget(getattr(self, f'button_player_color_{i}'), row, column, 1, 1)

        horizontal_layout_text_color = QHBoxLayout(self.group_box_text_color)
        horizontal_layout_text_color.addWidget(self.push_button_current_text_color)
        horizontal_layout_text_color.addLayout(grid_layout_text_colors)

        horizontal_layout_player_colors = QHBoxLayout(self.group_box_player_color)
        horizontal_layout_player_colors.addWidget(self.push_button_current_player_color)
        horizontal_layout_player_colors.addLayout(grid_layout_player_colors)

        self.horizontal_layout_fill_symbol_type = QHBoxLayout(self.group_box_fill_symbol_type)

        horizontal_layout_buttons = QHBoxLayout()
        horizontal_layout_buttons.addWidget(button_ok)
        horizontal_layout_buttons.addWidget(button_cancel)

        vertical_layout_main = QVBoxLayout()
        vertical_layout_main.addWidget(self.group_box_position)
        vertical_layout_main.addWidget(self.group_box_text_color)
        vertical_layout_main.addWidget(self.group_box_player_color)
        vertical_layout_main.addWidget(self.group_box_fill_symbol_type)
        vertical_layout_main.addLayout(horizontal_layout_buttons)

        grid_layout_global = QGridLayout(self)
        # grid_layout_global.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding), 0, 0)
        grid_layout_global.addLayout(vertical_layout_main, 0, 1, Qt.AlignCenter)
        # grid_layout_global.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding), 0, 2)

        button_ok.clicked.connect(self.accept)
        button_cancel.clicked.connect(self.reject)


class DialogFirstTeamPlayerSettings(DialogPlayerSettings):
    class CustomPushButton(QPushButton):
        def __init__(self, position: str, text: str, text_color: str, player_color: str, fill_type: str, parent=None):
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
            if self.fill_type == 'white':
                self.gradient = QLinearGradient()
                self.gradient.setStart(0, 0)
                self.gradient.setFinalStop(self.rect().right(), 0)
                self.gradient.setColorAt(0, QColor(f'#afffffff'))
            elif self.fill_type == 'full':
                self.gradient = QLinearGradient()
                self.gradient.setStart(0, 0)
                self.gradient.setFinalStop(self.rect().right(), 0)
                self.gradient.setColorAt(0, QColor(f'#9f{player_color[1:]}'))
            elif self.fill_type == 'left':
                self.gradient = QLinearGradient()
                self.gradient.setStart(self.rect().center().x(), 0)
                self.gradient.setFinalStop(self.rect().center().x() + 0.001, 0)
                self.gradient.setColorAt(0, QColor(f'#9f{player_color[1:]}'))
                self.gradient.setColorAt(1, QColor('#afffffff'))
            elif self.fill_type == 'right':
                self.gradient = QLinearGradient()
                self.gradient.setStart(self.rect().center().x(), 0)
                self.gradient.setFinalStop(self.rect().center().x() + 0.001, 0)
                self.gradient.setColorAt(0, QColor('#afffffff'))
                self.gradient.setColorAt(1, QColor(f'#af{player_color[1:]}'))
            elif self.fill_type == 'mid':
                self.gradient = QLinearGradient()
                self.gradient.setStart(0, 0)
                self.gradient.setFinalStop(self.rect().right() + 0.001, 0)
                self.gradient.setColorAt(0, QColor('#afffffff'))
                self.gradient.setColorAt(0.355, QColor('#afffffff'))
                self.gradient.setColorAt(0.356, QColor(f'#af{player_color[1:]}'))
                self.gradient.setColorAt(0.650, QColor(f'#af{player_color[1:]}'))
                self.gradient.setColorAt(0.651, QColor('#afffffff'))
                self.gradient.setColorAt(1, QColor('#afffffff'))

    def __init__(self, window_text_color: str, player_position: str, player_text: str, player_color: str, player_text_color: str, player_fill_type: str, parent=None, flags=Qt.WindowFlags()):
        super().__init__(window_text_color, player_text, player_text_color, player_color, parent, flags)
        self.player_text = player_text
        self.player_text_color = player_text_color
        self.player_color = player_color

        self.group_box_player_color.setTitle('Цвет контура и заливки')
        self.group_box_fill_symbol_type.setTitle('Тип заливки')
        self.push_button_white_fill = self.CustomPushButton(player_position, self.player_text, self.player_text_color, self.player_color, 'white', parent=None)
        self.push_button_white_fill.setObjectName('white')
        self.push_button_full_fill = self.CustomPushButton(player_position, self.player_text, self.player_text_color, self.player_color, 'full', parent=None)
        self.push_button_full_fill.setObjectName('full')
        self.push_button_left_fill = self.CustomPushButton(player_position, self.player_text, self.player_text_color, self.player_color, 'left', parent=None)
        self.push_button_left_fill.setObjectName('left')
        self.push_button_right_fill = self.CustomPushButton(player_position, self.player_text, self.player_text_color, self.player_color, 'right', parent=None)
        self.push_button_right_fill.setObjectName('right')
        self.push_button_mid_fill = self.CustomPushButton(player_position, self.player_text, self.player_text_color, self.player_color, 'mid', parent=None)
        self.push_button_mid_fill.setObjectName('mid')

        self.button_group_fill_symbol_type.addButton(self.push_button_white_fill)
        self.button_group_fill_symbol_type.addButton(self.push_button_full_fill)
        self.button_group_fill_symbol_type.addButton(self.push_button_left_fill)
        self.button_group_fill_symbol_type.addButton(self.push_button_right_fill)
        self.button_group_fill_symbol_type.addButton(self.push_button_mid_fill)

        self.horizontal_layout_fill_symbol_type.addWidget(self.push_button_white_fill)
        self.horizontal_layout_fill_symbol_type.addWidget(self.push_button_full_fill)
        self.horizontal_layout_fill_symbol_type.addWidget(self.push_button_left_fill)
        self.horizontal_layout_fill_symbol_type.addWidget(self.push_button_right_fill)
        self.horizontal_layout_fill_symbol_type.addWidget(self.push_button_mid_fill)

        getattr(self, f'push_button_{player_fill_type}_fill').setChecked(True)

        self.line_edit_player_position.textChanged.connect(lambda text: self.set_text(text))

        for i, color in enumerate(self.COLORS):
            getattr(self, f'button_text_color_{i}').pressed.connect(lambda color=color: self.set_text_color(color))

        for i, color in enumerate(self.COLORS):
            getattr(self, f'button_player_color_{i}').pressed.connect(lambda color=color: self.set_player_color(color))

        self.set_text(player_text)
        self.set_text_color(player_text_color)
        self.set_player_color(player_color)

    def set_text(self, text):
        self.player_text = text
        self.push_button_white_fill.text = text
        self.push_button_full_fill.text = text
        self.push_button_left_fill.text = text
        self.push_button_right_fill.text = text
        self.push_button_mid_fill.text = text

    def set_text_color(self, color):
        self.player_text_color = color
        self.push_button_current_text_color.setStyleSheet(f'background-color: {color};')
        self.push_button_white_fill.text_color = color
        self.push_button_full_fill.text_color = color
        self.push_button_left_fill.text_color = color
        self.push_button_right_fill.text_color = color
        self.push_button_mid_fill.text_color = color

    def set_player_color(self, color):
        self.player_color = color
        self.push_button_current_player_color.setStyleSheet(f'background-color: {color};')
        self.push_button_white_fill.set_gradient(color)
        self.push_button_full_fill.set_gradient(color)
        self.push_button_left_fill.set_gradient(color)
        self.push_button_right_fill.set_gradient(color)
        self.push_button_mid_fill.set_gradient(color)


class DialogSecondTeamPlayerSettings(DialogPlayerSettings):
    class CustomPushButton(QPushButton):

        def __init__(self, player_text: str, player_text_color: str, player_color: str,  symbol: str, parent=None):
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
            if self.symbol == 'letter':
                painter.setPen(QPen(QColor(self.player_text_color)))
                painter.setFont(self.font_letter)
                painter.drawText(self.rec, Qt.AlignCenter, self.player_text)
            elif self.symbol == 'x':
                painter.setPen(QPen(QColor(self.player_color), 2, s=Qt.SolidLine, c=Qt.RoundCap, j=Qt.RoundJoin))
                painter.drawLines([self.line1, self.line2])
            elif self.symbol == 'triangle_bot':
                painter.setPen(QPen(QColor(self.player_color), 2, s=Qt.SolidLine, c=Qt.RoundCap, j=Qt.RoundJoin))
                painter.drawPolygon(QPolygonF(self.poligon_bot))
                painter.setPen(QPen(QColor(self.player_text_color)))
                painter.setFont(self.font_triangle)
                painter.drawText(QRectF(0, -12, self.width(), self.height() + 12), Qt.AlignCenter, self.player_text)
            elif self.symbol == 'triangle_top':
                painter.setPen(QPen(QColor(self.player_color), 2, s=Qt.SolidLine, c=Qt.RoundCap, j=Qt.RoundJoin))
                painter.drawPolygon(QPolygonF(self.poligon_top))
                painter.setPen(QPen(QColor(self.player_text_color)))
                painter.setFont(self.font_triangle)
                painter.drawText(QRectF(0, 10, self.width(), self.height() - 10), Qt.AlignCenter, self.player_text)
            self.update()

    def __init__(self, window_text_color: str, player_text: str, player_text_color: str, player_color: str, player_symbol: str, parent=None, flags=Qt.WindowFlags()):
        super().__init__(window_text_color, player_text, player_text_color, player_color, parent=parent)
        self.player_text = player_text
        self.player_color = player_color
        self.player_text_color = player_text_color
        self.player_symbol = player_symbol

        self.group_box_player_color.setTitle('Цвет контура')
        self.group_box_fill_symbol_type.setTitle('Символ')
        self.line_edit_player_position.setMaxLength(1)

        self.push_button_letter_symbol = self.CustomPushButton(self.player_text, self.player_text_color, self.player_color, 'letter')
        self.push_button_letter_symbol.pressed.connect(lambda symbol='letter': self.set_symbol(symbol))

        self.push_button_x_symbol = self.CustomPushButton(self.player_text, self.player_text_color, self.player_color, 'x')
        self.push_button_x_symbol.pressed.connect(lambda symbol='x': self.set_symbol(symbol))

        self.push_button_triangle_bot_symbol = self.CustomPushButton(self.player_text, self.player_text_color, self.player_color, 'triangle_bot')
        self.push_button_triangle_bot_symbol.pressed.connect(lambda symbol='triangle_bot': self.set_symbol(symbol))

        self.push_button_triangle_top_symbol = self.CustomPushButton(self.player_text, self.player_text_color, self.player_color, 'triangle_top')
        self.push_button_triangle_top_symbol.pressed.connect(lambda symbol='triangle_top': self.set_symbol(symbol))

        self.button_group_fill_symbol_type.addButton(self.push_button_letter_symbol)
        self.button_group_fill_symbol_type.addButton(self.push_button_x_symbol)
        self.button_group_fill_symbol_type.addButton(self.push_button_triangle_bot_symbol)
        self.button_group_fill_symbol_type.addButton(self.push_button_triangle_top_symbol)

        self.horizontal_layout_fill_symbol_type.addWidget(self.push_button_letter_symbol)
        self.horizontal_layout_fill_symbol_type.addWidget(self.push_button_x_symbol)
        self.horizontal_layout_fill_symbol_type.addWidget(self.push_button_triangle_bot_symbol)
        self.horizontal_layout_fill_symbol_type.addWidget(self.push_button_triangle_top_symbol)

        getattr(self, f'push_button_{player_symbol}_symbol').setChecked(True)

        self.line_edit_player_position.textChanged.connect(lambda text: self.set_text(text))

        for i, color in enumerate(self.COLORS):
            getattr(self, f'button_text_color_{i}').pressed.connect(lambda color=color: self.set_text_color(color))

        for i, color in enumerate(self.COLORS):
            getattr(self, f'button_player_color_{i}').pressed.connect(lambda color=color: self.set_player_color(color))

        self.set_symbol(self.player_symbol)

    def set_text(self, text):
        self.player_text = text
        self.push_button_letter_symbol.player_text = self.line_edit_player_position.text()
        self.push_button_triangle_bot_symbol.player_text = self.line_edit_player_position.text()
        self.push_button_triangle_top_symbol.player_text = self.line_edit_player_position.text()

    def set_player_color(self, color):
        self.player_color = color
        self.push_button_current_player_color.setStyleSheet(f'background-color: {self.player_color};')
        self.push_button_triangle_bot_symbol.player_color = color
        self.push_button_triangle_top_symbol.player_color = color
        self.push_button_x_symbol.player_color = color

    def set_text_color(self, color):
        self.player_text_color = color
        self.push_button_current_text_color.setStyleSheet(f'background-color: {self.player_text_color};')
        self.push_button_letter_symbol.player_text_color = color
        self.push_button_triangle_bot_symbol.player_text_color = color
        self.push_button_triangle_top_symbol.player_text_color = color

    def set_symbol(self, symbol):
        self.player_symbol = symbol
        if symbol == 'letter':
            self.group_box_position.setEnabled(True)
            self.group_box_text_color.setEnabled(True)
            self.group_box_player_color.setEnabled(False)
        elif symbol == 'x':
            self.group_box_position.setEnabled(False)
            self.group_box_text_color.setEnabled(False)
            self.group_box_player_color.setEnabled(True)
        elif symbol == 'triangle_bot':
            self.group_box_position.setEnabled(True)
            self.group_box_text_color.setEnabled(True)
            self.group_box_player_color.setEnabled(True)
        elif symbol == 'triangle_top':
            self.group_box_position.setEnabled(True)
            self.group_box_text_color.setEnabled(True)
            self.group_box_player_color.setEnabled(True)

