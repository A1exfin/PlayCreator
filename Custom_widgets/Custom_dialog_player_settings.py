from PySide6.QtWidgets import QDialog, QColorDialog, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,\
    QButtonGroup, QGroupBox
from PySide6.QtGui import QFont, QPainter, QPen, QBrush, QPolygonF, QColor, QLinearGradient
from PySide6.QtCore import Qt, QLineF, QPointF, QRectF
from Custom_widgets.Custom_buttons_for_player_settings import CustomPushButtonFillType
from Custom_widgets.Custom_buttons_for_player_settings import CustomPushButtonSymbolType
from Enum_flags import FillType, SymbolType


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

        groupbox_stylesheet = '''
        QGroupBox {border: 2px solid gray; border-radius: 5px; padding-top: 3px; margin-top: 8px;}
        QGroupBox::title {subcontrol-origin: margin; subcontrol-position: top left; left: 15px;}'''
        # self.setStyleSheet('''QDialog {color: %s;}
        # QGroupBox {border: 2px solid gray; border-radius: 5px; padding-top: 3px; margin-top: 8px;}
        # QGroupBox::title {subcontrol-origin: margin; subcontrol-position: top left; left: 15px;}''' % window_text_color)
        self.font.setPointSize(10)
        self.font.setBold(False)
        self.group_box_position = QGroupBox('Позиция игрока')  # , parent=self
        self.group_box_position.setFont(self.font)
        self.group_box_position.setFixedSize(244, 73)
        self.group_box_position.setStyleSheet(groupbox_stylesheet)

        self.group_box_text_color = QGroupBox('Цвет текста')  # , parent=self
        self.group_box_text_color.setFont(self.font)
        self.group_box_text_color.setFixedSize(244, 73)
        self.group_box_text_color.setStyleSheet(groupbox_stylesheet)

        self.group_box_player_color = QGroupBox()  # parent=self
        self.group_box_player_color.setFont(self.font)
        self.group_box_player_color.setFixedSize(244, 73)
        self.group_box_player_color.setStyleSheet(groupbox_stylesheet)

        self.group_box_fill_symbol_type = QGroupBox()  # parent=self
        self.group_box_fill_symbol_type.setFont(self.font)
        self.group_box_fill_symbol_type.setFixedSize(244, 73)
        self.group_box_fill_symbol_type.setStyleSheet(groupbox_stylesheet)

        self.button_group_fill_symbol_type = QButtonGroup(parent=self)
        self.button_group_fill_symbol_type.setExclusive(True)

        self.font.setPointSize(14)
        self.font.setBold(True)
        self.line_edit_player_position = QLineEdit(parent=self.group_box_position)
        self.line_edit_player_position.setFont(self.font)
        self.line_edit_player_position.setMaxLength(2)
        self.line_edit_player_position.setText(player_text)
        self.line_edit_player_position.setContentsMargins(5, 5, 5, 0)
        self.line_edit_player_position.setStyleSheet('QLineEdit:disabled{color: #334e3a;}')

        self.font.setPointSize(10)
        self.font.setBold(False)
        button_ok = QPushButton('ОК', parent=self)
        button_ok.setFont(self.font)
        button_ok.setFixedSize(100, 25)
        button_cancel = QPushButton('Отмена', parent=self)
        button_cancel.setFont(self.font)
        button_cancel.setFixedSize(100, 25)

        self.push_button_current_text_color = QPushButton(parent=self.group_box_text_color)
        self.push_button_current_text_color.setFixedSize(40, 40)
        self.push_button_current_text_color.setStyleSheet(f'background-color: {player_text_color}')

        self.push_button_current_player_color = QPushButton(parent=self.group_box_player_color)
        self.push_button_current_player_color.setFixedSize(40, 40)
        self.push_button_current_player_color.setStyleSheet(f'background-color: {player_color}')

        horizontal_layout_position = QVBoxLayout(self.group_box_position)
        horizontal_layout_position.addWidget(self.line_edit_player_position)

        grid_layout_text_colors = QGridLayout()
        grid_layout_text_colors.setVerticalSpacing(4)
        grid_layout_text_colors.setHorizontalSpacing(2)
        for i, color in enumerate(self.COLORS):
            setattr(self, f'button_text_color_{i}', QPushButton(parent=self.group_box_text_color))
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
        grid_layout_player_colors.setVerticalSpacing(4)
        grid_layout_player_colors.setHorizontalSpacing(2)
        for i, color in enumerate(self.COLORS):
            setattr(self, f'button_player_color_{i}', QPushButton(parent=self.group_box_player_color))
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
    def __init__(self, window_text_color: str, player_position: str, player_text: str, player_color: str, player_text_color: str, player_fill_type: FillType, parent=None, flags=Qt.WindowFlags()):
        super().__init__(window_text_color, player_text, player_text_color, player_color, parent, flags)
        self.player_text = player_text
        self.player_text_color = player_text_color
        self.player_color = player_color

        self.group_box_player_color.setTitle('Цвет контура и заливки')
        self.group_box_fill_symbol_type.setTitle('Тип заливки')
        self.push_button_white_fill = CustomPushButtonFillType(player_position, self.player_text, self.player_text_color, self.player_color, FillType.white, parent=self.group_box_fill_symbol_type)
        self.push_button_white_fill.setObjectName('white')
        self.push_button_full_fill = CustomPushButtonFillType(player_position, self.player_text, self.player_text_color, self.player_color, FillType.full, parent=self.group_box_fill_symbol_type)
        self.push_button_full_fill.setObjectName('full')
        self.push_button_left_fill = CustomPushButtonFillType(player_position, self.player_text, self.player_text_color, self.player_color, FillType.left, parent=self.group_box_fill_symbol_type)
        self.push_button_left_fill.setObjectName('left')
        self.push_button_right_fill = CustomPushButtonFillType(player_position, self.player_text, self.player_text_color, self.player_color, FillType.right, parent=self.group_box_fill_symbol_type)
        self.push_button_right_fill.setObjectName('right')
        self.push_button_mid_fill = CustomPushButtonFillType(player_position, self.player_text, self.player_text_color, self.player_color, FillType.mid, parent=self.group_box_fill_symbol_type)
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

        getattr(self, f'push_button_{player_fill_type.name}_fill').setChecked(True)

        self.line_edit_player_position.textChanged.connect(lambda text: self.set_text(text))

        for i, color in enumerate(self.COLORS):
            getattr(self, f'button_text_color_{i}').pressed.connect(lambda color=color: self.set_text_color(color))

        for i, color in enumerate(self.COLORS):
            getattr(self, f'button_player_color_{i}').pressed.connect(lambda color=color: self.set_player_color(color))

        self.push_button_current_text_color.clicked.connect(self.set_user_text_color)
        self.push_button_current_player_color.clicked.connect(self.set_user_player_color)

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

    def set_user_text_color(self):
        user_color_dialog = QColorDialog(parent=self)
        if user_color_dialog.exec():
            self.set_text_color(user_color_dialog.selectedColor().name())

    def set_text_color(self, color):
        self.player_text_color = color
        self.push_button_current_text_color.setStyleSheet(f'background-color: {color};')
        self.push_button_white_fill.text_color = color
        self.push_button_full_fill.text_color = color
        self.push_button_left_fill.text_color = color
        self.push_button_right_fill.text_color = color
        self.push_button_mid_fill.text_color = color

    def set_user_player_color(self):
        user_color_dialog = QColorDialog(parent=self)
        if user_color_dialog.exec():
            self.set_player_color(user_color_dialog.selectedColor().name())

    def set_player_color(self, color):
        self.player_color = color
        self.push_button_current_player_color.setStyleSheet(f'background-color: {color};')
        self.push_button_white_fill.set_gradient(color)
        self.push_button_full_fill.set_gradient(color)
        self.push_button_left_fill.set_gradient(color)
        self.push_button_right_fill.set_gradient(color)
        self.push_button_mid_fill.set_gradient(color)


class DialogSecondTeamPlayerSettings(DialogPlayerSettings):
    def __init__(self, window_text_color: str, player_text: str, player_text_color: str, player_color: str, player_symbol: SymbolType, parent=None, flags=Qt.WindowFlags()):
        super().__init__(window_text_color, player_text, player_text_color, player_color, parent=parent)
        self.player_text = player_text
        self.player_color = player_color
        self.player_text_color = player_text_color
        self.player_symbol = player_symbol

        self.group_box_player_color.setTitle('Цвет контура')
        self.group_box_fill_symbol_type.setTitle('Символ')
        self.line_edit_player_position.setMaxLength(1)

        self.push_button_letter_symbol = CustomPushButtonSymbolType(self.player_text, self.player_text_color, self.player_color, SymbolType.letter, parent=self.group_box_fill_symbol_type)
        self.push_button_letter_symbol.pressed.connect(lambda symbol=SymbolType.letter: self.set_symbol(symbol))

        self.push_button_cross_symbol = CustomPushButtonSymbolType(self.player_text, self.player_text_color, self.player_color, SymbolType.cross, parent=self.group_box_fill_symbol_type)
        self.push_button_cross_symbol.pressed.connect(lambda symbol=SymbolType.cross: self.set_symbol(symbol))

        self.push_button_triangle_bot_symbol = CustomPushButtonSymbolType(self.player_text, self.player_text_color, self.player_color, SymbolType.triangle_bot, parent=self.group_box_fill_symbol_type)
        self.push_button_triangle_bot_symbol.pressed.connect(lambda symbol=SymbolType.triangle_bot: self.set_symbol(symbol))

        self.push_button_triangle_top_symbol = CustomPushButtonSymbolType(self.player_text, self.player_text_color, self.player_color, SymbolType.triangle_top, parent=self.group_box_fill_symbol_type)
        self.push_button_triangle_top_symbol.pressed.connect(lambda symbol=SymbolType.triangle_top: self.set_symbol(symbol))

        self.button_group_fill_symbol_type.addButton(self.push_button_letter_symbol)
        self.button_group_fill_symbol_type.addButton(self.push_button_cross_symbol)
        self.button_group_fill_symbol_type.addButton(self.push_button_triangle_bot_symbol)
        self.button_group_fill_symbol_type.addButton(self.push_button_triangle_top_symbol)

        self.horizontal_layout_fill_symbol_type.addWidget(self.push_button_letter_symbol)
        self.horizontal_layout_fill_symbol_type.addWidget(self.push_button_cross_symbol)
        self.horizontal_layout_fill_symbol_type.addWidget(self.push_button_triangle_bot_symbol)
        self.horizontal_layout_fill_symbol_type.addWidget(self.push_button_triangle_top_symbol)

        getattr(self, f'push_button_{player_symbol.name}_symbol').setChecked(True)

        self.line_edit_player_position.textChanged.connect(lambda text: self.set_text(text))

        for i, color in enumerate(self.COLORS):
            getattr(self, f'button_text_color_{i}').pressed.connect(lambda color=color: self.set_text_color(color))

        for i, color in enumerate(self.COLORS):
            getattr(self, f'button_player_color_{i}').pressed.connect(lambda color=color: self.set_player_color(color))

        self.push_button_current_text_color.clicked.connect(self.set_user_text_color)
        self.push_button_current_player_color.clicked.connect(self.set_user_player_color)

        self.set_symbol(self.player_symbol)

    def set_text(self, text):
        self.player_text = text
        self.push_button_letter_symbol.player_text = self.line_edit_player_position.text()
        self.push_button_triangle_bot_symbol.player_text = self.line_edit_player_position.text()
        self.push_button_triangle_top_symbol.player_text = self.line_edit_player_position.text()

    def set_user_text_color(self):
        user_color_dialog = QColorDialog(parent=self)
        if user_color_dialog.exec():
            self.set_text_color(user_color_dialog.selectedColor().name())

    def set_text_color(self, color):
        self.player_text_color = color
        self.push_button_current_text_color.setStyleSheet(f'background-color: {self.player_text_color};')
        self.push_button_letter_symbol.player_text_color = color
        self.push_button_triangle_bot_symbol.player_text_color = color
        self.push_button_triangle_top_symbol.player_text_color = color

    def set_user_player_color(self):
        user_color_dialog = QColorDialog(parent=self)
        if user_color_dialog.exec():
            self.set_player_color(user_color_dialog.selectedColor().name())

    def set_player_color(self, color):
        self.player_color = color
        self.push_button_current_player_color.setStyleSheet(f'background-color: {self.player_color};')
        self.push_button_triangle_bot_symbol.player_color = color
        self.push_button_triangle_top_symbol.player_color = color
        self.push_button_cross_symbol.player_color = color

    def set_symbol(self, symbol):
        self.player_symbol = symbol
        if symbol == SymbolType.letter:
            self.group_box_position.setEnabled(True)
            self.group_box_text_color.setEnabled(True)
            self.group_box_player_color.setEnabled(False)
        elif symbol == SymbolType.cross:
            self.group_box_position.setEnabled(False)
            self.group_box_text_color.setEnabled(False)
            self.group_box_player_color.setEnabled(True)
        elif symbol == SymbolType.triangle_bot:
            self.group_box_position.setEnabled(True)
            self.group_box_text_color.setEnabled(True)
            self.group_box_player_color.setEnabled(True)
        elif symbol == SymbolType.triangle_top:
            self.group_box_position.setEnabled(True)
            self.group_box_text_color.setEnabled(True)
            self.group_box_player_color.setEnabled(True)

