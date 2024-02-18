from PySide6.QtWidgets import QDialog, QColorDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,\
    QGroupBox, QSlider, QLabel, QComboBox, QSpacerItem, QSizePolicy
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from Custom_widgets.Custom_widget_for_figure_settings import CustomWidget
from Enum_flags import Modes


class DialogFigureSettings(QDialog):
    COLORS = ('#000000', '#800000', '#400080', '#0004ff', '#8d8b9a', '#22b14c',
              '#ff0000', '#ff00ea', '#ff80ff', '#ff8000', '#dcdc00', '#00ff00')

    def __init__(self, window_text_color: str, figure_type: Modes,
                 border: bool, border_color: str, border_width: int,
                 fill: bool, fill_color: str, fill_opacity: str,
                 parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.border = border
        self.border_color = border_color
        self.border_width = border_width
        self.fill = fill
        self.fill_color = fill_color
        self.fill_opacity = fill_opacity
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(572, 322)
        self.setWindowTitle('Настройки фигуры')
        self.setStyleSheet(f'color: {window_text_color};')

        self.font = QFont()

        groupbox_stylesheet = '''
        QGroupBox {border: 2px solid gray; border-radius: 5px; padding-top: 3px; margin-top: 8px;}
        QGroupBox::title {subcontrol-origin: margin; subcontrol-position: top left; left: 15px}
        QGroupBox::indicator {}'''
        # QGroupBox {border: 2px solid gray; border-radius: 5px; padding-top: 3px; margin-top: 8px;}
        # QGroupBox::title {subcontrol-origin: margin; subcontrol-position: top left; left: 15px;}''' % window_text_color)
        self.font.setPointSize(10)
        self.font.setBold(False)
        self.group_box_border = QGroupBox('Граница')  # , parent=self
        self.group_box_border.setFont(self.font)
        self.group_box_border.setFixedSize(244, 73)
        self.group_box_border.setStyleSheet(groupbox_stylesheet)
        self.group_box_border.setCheckable(True)
        self.group_box_border.setChecked(border)
        self.group_box_border.toggled.connect(self.set_border)

        self.group_box_fill = QGroupBox('Заливка')  # parent=self
        self.group_box_fill.setFont(self.font)
        self.group_box_fill.setFixedSize(244, 111)
        self.group_box_fill.setStyleSheet(groupbox_stylesheet)
        self.group_box_fill.setCheckable(True)
        self.group_box_fill.setChecked(fill)
        self.group_box_fill.toggled.connect(self.set_fill)

        self.font.setPointSize(10)
        self.font.setBold(False)
        self.combo_box_border_width = QComboBox(parent=self.group_box_border)
        self.combo_box_border_width.addItems(['2', '3', '4', '5', '6'])
        self.combo_box_border_width.setCurrentText(str(border_width))
        self.combo_box_border_width.setFixedSize(40, 25)
        self.combo_box_border_width.currentTextChanged.connect(self.set_border_width)

        self.label_opacity = QLabel()
        self.label_opacity.setFont(self.font)
        self.label_opacity.setFixedSize(40, 40)
        self.label_opacity.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.slider_fill_opacity = QSlider(Qt.Orientation.Horizontal, parent=self.group_box_fill)
        self.slider_fill_opacity.setMinimum(0)
        self.slider_fill_opacity.setMaximum(255)
        self.slider_fill_opacity.setValue(int(fill_opacity[1:], 16))
        self.slider_fill_opacity.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.slider_fill_opacity.setTickInterval(10)
        self.slider_fill_opacity.valueChanged.connect(self.set_opacity)

        # self.font.setPointSize(10)
        # self.font.setBold(False)
        button_ok = QPushButton('ОК', parent=self)
        button_ok.setFont(self.font)
        button_ok.setFixedSize(100, 25)
        button_cancel = QPushButton('Отмена', parent=self)
        button_cancel.setFont(self.font)
        button_cancel.setFixedSize(100, 25)

        self.push_button_current_border_color = QPushButton(parent=self.group_box_border)
        self.push_button_current_border_color.setFixedSize(40, 40)
        self.push_button_current_border_color.setStyleSheet(f'background-color: {border_color}')
        self.push_button_current_border_color.clicked.connect(self.set_user_border_color)

        self.push_button_current_fill_color = QPushButton(parent=self.group_box_fill)
        self.push_button_current_fill_color.setFixedSize(40, 40)
        self.push_button_current_fill_color.setStyleSheet(f'background-color: {fill_color}')
        self.push_button_current_fill_color.clicked.connect(self.set_user_fill_color)

        grid_layout_border_colors = QGridLayout()
        grid_layout_border_colors.setVerticalSpacing(4)
        grid_layout_border_colors.setHorizontalSpacing(2)
        for i, color in enumerate(self.COLORS):
            setattr(self, f'button_border_color_{i}', QPushButton(parent=self.group_box_border))
            getattr(self, f'button_border_color_{i}').setFixedSize(18, 18)
            getattr(self, f'button_border_color_{i}').setStyleSheet(f'background-color: {color}')
            getattr(self, f'button_border_color_{i}').pressed.connect(lambda color=color: self.set_border_color(color))
            row, column = (0, i + 1) if i < len(self.COLORS) / 2 else (1, i + 1 - len(self.COLORS) / 2)
            grid_layout_border_colors.addWidget(getattr(self, f'button_border_color_{i}'), row, column, 1, 1)

        grid_layout_fill_colors = QGridLayout()
        grid_layout_fill_colors.setVerticalSpacing(4)
        grid_layout_fill_colors.setHorizontalSpacing(2)
        for i, color in enumerate(self.COLORS):
            setattr(self, f'button_fill_color_{i}', QPushButton(parent=self.group_box_fill))
            getattr(self, f'button_fill_color_{i}').setFixedSize(18, 18)
            getattr(self, f'button_fill_color_{i}').setStyleSheet(f'background-color: {color}')
            getattr(self, f'button_fill_color_{i}').pressed.connect(lambda color=color: self.set_fill_color(color))
            row, column = (0, i + 1) if i < len(self.COLORS) / 2 else (1, i + 1 - len(self.COLORS) / 2)
            grid_layout_fill_colors.addWidget(getattr(self, f'button_fill_color_{i}'), row, column, 1, 1)

        self.pix = CustomWidget(figure_type, border_color, border_width, fill_color, fill_opacity, parent)

        horizontal_layout_border = QHBoxLayout(self.group_box_border)
        horizontal_layout_border.addWidget(self.combo_box_border_width)
        horizontal_layout_border.addWidget(self.push_button_current_border_color)
        horizontal_layout_border.addLayout(grid_layout_border_colors)
        horizontal_layout_border.addSpacerItem(QSpacerItem(40, 40, QSizePolicy.Expanding, QSizePolicy.Expanding))

        horizontal_layout_fill_colors = QHBoxLayout()
        horizontal_layout_fill_colors.addWidget(self.label_opacity)
        horizontal_layout_fill_colors.addWidget(self.push_button_current_fill_color)
        horizontal_layout_fill_colors.addLayout(grid_layout_fill_colors)
        horizontal_layout_fill_colors.addSpacerItem(QSpacerItem(40, 40, QSizePolicy.Expanding, QSizePolicy.Expanding))

        vertical_layout_fill = QVBoxLayout(self.group_box_fill)
        vertical_layout_fill.addLayout(horizontal_layout_fill_colors)
        vertical_layout_fill.addWidget(self.slider_fill_opacity)

        horizontal_layout_buttons = QHBoxLayout()
        horizontal_layout_buttons.addWidget(button_ok)
        horizontal_layout_buttons.addWidget(button_cancel)

        vertical_layout_main = QVBoxLayout()
        vertical_layout_main.addSpacerItem(QSpacerItem(40, 40, QSizePolicy.Expanding, QSizePolicy.Expanding))
        vertical_layout_main.addWidget(self.group_box_border)
        vertical_layout_main.addWidget(self.group_box_fill)
        vertical_layout_main.addLayout(horizontal_layout_buttons)
        vertical_layout_main.addSpacerItem(QSpacerItem(40, 40, QSizePolicy.Expanding, QSizePolicy.Expanding))

        horizontal_layout_main = QHBoxLayout()
        horizontal_layout_main.addLayout(vertical_layout_main)
        horizontal_layout_main.addWidget(self.pix)

        grid_layout_global = QGridLayout(self)
        # grid_layout_global.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding), 0, 0)
        # grid_layout_global.addLayout(vertical_layout_main, 0, 1, Qt.AlignCenter)
        grid_layout_global.addLayout(horizontal_layout_main, 0, 1, Qt.AlignCenter)
        # grid_layout_global.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding), 0, 2)

        self.set_border(border)
        self.set_fill(fill)
        self.set_opacity(int(fill_opacity[1:], 16))

        button_ok.clicked.connect(self.accept)
        button_cancel.clicked.connect(self.reject)

    def set_border(self, value):
        if value == 0:
            self.border = False
            self.pix.pen.setWidthF(0.0000001)
            self.group_box_fill.setChecked(True)
        else:
            self.border = True
            self.pix.pen.setWidth(int(self.combo_box_border_width.currentText()))
        self.pix.update()

    def set_border_width(self, value):
        self.border_width = int(value)
        self.pix.pen.setWidth(int(value))
        self.pix.update()

    def set_border_color(self, color):
        self.border_color = color
        self.pix.pen.setColor(color)
        self.push_button_current_border_color.setStyleSheet(f'background-color: {color};')
        self.pix.update()

    def set_user_border_color(self):
        user_color_dialog = QColorDialog(parent=self)
        if user_color_dialog.exec():
            self.set_border_color(user_color_dialog.selectedColor().name())

    def set_fill(self, value):
        if value == 0:
            self.fill = False
            self.pix.brush.setColor(Qt.transparent)
            self.group_box_border.setChecked(True)
        else:
            self.fill = True
            self.pix.brush.setColor(f'{self.fill_opacity}{self.fill_color[1:]}')
        self.pix.update()

    def set_fill_color(self, color):
        self.fill_color = color
        self.pix.set_brush(self.fill_opacity, color)
        self.push_button_current_fill_color.setStyleSheet(f'background-color: {color};')
        self.pix.update()

    def set_user_fill_color(self):
        user_color_dialog = QColorDialog(parent=self)
        if user_color_dialog.exec():
            self.set_fill_color(user_color_dialog.selectedColor().name())

    def set_opacity(self, opacity):
        opacity_str = f'#{str(hex(opacity))[2:].zfill(2)}'
        opacity_percent = opacity / 255 * 100
        self.label_opacity.setText(f'{int(opacity_percent)} %')
        self.fill_opacity = opacity_str
        self.pix.set_brush(opacity_str, self.fill_color)
        self.pix.update()
