import os.path
from PlayCreator_ui import *
from PyQt5.Qt import *
import sys
from Custom_graphics_view import CustomGraphicsView
from Custom_scene import Field
from Players_data import PlayersData
from Item_player import Player
from datetime import datetime

# style = os.path.join(os.path.dirname(__file__), 'PlayCreator_dark_theme.css')


def timeit(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        print(datetime.now() - start)
        return result
    return wrapper


MODES = ('move', 'erase', 'route', 'block', 'motion', 'rectangle', 'ellipse', 'pencil', 'label')
COLORS = ('#000000',  '#800000', '#400080', '#0004ff', '#8d8b9a', '#22b14c',
          '#ff0000', '#ff00ea', '#ff80ff', '#ff8000', '#dcdc00', '#00ff00')


class PlayCreator(QMainWindow, Ui_MainWindow):
    colorChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.field = Field(self)
        self.graphics_view = CustomGraphicsView(self.centralwidget)
        self.graphics_view.setScene(self.field)
        # self.graphics_view.setGeometry(QRect(10, 10, int(self.field.football_field_width * self.graphics_view.zoom_factor ** 2) + 25,
        #                                int(self.field.flag_field_length * (1 / self.graphics_view.zoom_factor) ** 3) + 25))  ###########
        self.gridLayout.addWidget(self.graphics_view, 0, 0, 1, 1)
        self.set_game_type(self.tabWidget_game_type.currentIndex())
        self.players = PlayersData(self.field)
        self.reset_settings()
        self.set_zoom(self.graphics_view.current_zoom)

        self.fontComboBox.setCurrentFont(self.field.config['font_type'])
        self.comboBox_font_size.setCurrentText(str(self.field.config['font_size']))
        self.pushButton_bold.setChecked(self.field.config['bold'])
        self.pushButton_bold.setShortcut(QKeySequence.Bold)
        self.pushButton_italic.setChecked(self.field.config['italic'])
        self.pushButton_italic.setShortcut(QKeySequence.Italic)
        self.pushButton_underline.setChecked(self.field.config['underline'])
        self.pushButton_underline.setShortcut(QKeySequence.Underline)
        self.comboBox_line_thickness.setCurrentText(str(self.field.config['line_thickness']))
        self.pushButton_current_color.setStyleSheet(f'background-color: {self.field.config["color"]};')

        action_theme_group = QActionGroup(self)
        action_theme_group.addAction(self.action_dark_theme)
        action_theme_group.addAction(self.action_light_theme)
        action_theme_group.setExclusive(True)
        self.action_dark_theme.setChecked(True)
        self.set_dark_theme()

        mode_group = QButtonGroup(self)
        mode_group.setExclusive(True)
        for mode in MODES:
            btn = getattr(self, f'pushButton_{mode}')
            btn.pressed.connect(lambda mode=mode: self.field.set_mode(mode))
            mode_group.addButton(btn)
        for i, color in enumerate(COLORS):
            btn = getattr(self, f'pushButton_color_{i}')
            btn.setStyleSheet(f'background-color: {color};')
            btn.pressed.connect(lambda color=color: self.set_color(color))

        self.graphics_view.zoomChanged.connect(self.set_zoom)
        self.tabWidget_game_type.currentChanged.connect(self.set_game_type)
        self.comboBox_team_type_football.currentIndexChanged.connect(self.team_type_changed)
        self.pushButton_place_first_team_football.clicked.connect(self.place_first_team_football)
        self.pushButton_add_additional_off_football.clicked.connect(self.place_additional_offence_player_football)
        self.pushButton_del_additional_off_football.clicked.connect(self.delete_additional_offence_player_football)
        self.pushButton_place_second_team_football.clicked.connect(self.place_second_team_football)
        self.pushButton_delete_second_team_football.clicked.connect(self.delete_second_team_football)
        self.pushButton_delete_all_players_football.clicked.connect(self.delete_teams_football)

        self.lineEdit_yards_flag.textChanged.connect(self.check_max_yards_flag)
        self.pushButton_place_off_team_flag.clicked.connect(self.place_off_team_flag)
        self.pushButton_place_def_team_flag.clicked.connect(self.place_def_team_flag)
        self.pushButton_delete_all_players_flag.clicked.connect(self.delete_teams_flag)
        self.pushButton_add_additional_off_flag.clicked.connect(self.place_additional_player_flag)
        self.pushButton_del_additional_off_flag.clicked.connect(self.delete_additional_offence_player_flag)
        self.pushButton_delete_def_team_flag.clicked.connect(self.delete_def_team_flag)

        self.comboBox_line_thickness.currentTextChanged.connect(lambda thickness: self.field.set_config('line_thickness', int(thickness)))
        self.fontComboBox.currentFontChanged.connect(self.combobox_font_changed)
        self.comboBox_font_size.currentTextChanged.connect(self.font_size_changed)
        self.pushButton_bold.toggled.connect(self.bold_changed)
        self.pushButton_italic.toggled.connect(self.italic_changed)
        self.pushButton_underline.toggled.connect(self.underline_changed)
        self.pushButton_current_color.clicked.connect(self.set_user_color)########################
        self.colorChanged.connect(self.color_changed)


        self.pushButton_delete_actions.clicked.connect(self.delete_actions)
        self.pushButton_delete_figures.clicked.connect(self.field.delete_figures)
        self.pushButton_delete_labels.clicked.connect(self.field.delete_labels)
        self.pushButton_delete_pencil.clicked.connect(self.field.delete_pencil)

        self.field.modeChanged.connect(lambda mode: getattr(self, f'pushButton_{mode}').setChecked(True))

        self.field.labelDoubleClicked.connect(self.update_window_font_config)
        self.field.labelEditingFinished.connect(self.label_editing_finished)

        self.action_save.triggered.connect(self.save_on_picture)
        self.action_presentation.toggled.connect(self.presentation_mode)
        self.action_dark_theme.toggled.connect(self.set_dark_theme)
        self.action_light_theme.toggled.connect(self.set_light_theme)

        self.action_exit.triggered.connect(lambda: sys.exit(app.exec_()))  ######################
        # self.test_func.clicked.connect(self.test_fn)############################## тестовая функция
        self.test_func.clicked.connect(self.set_dark_theme)############################## тестовая функция
        # self.test_func.setEnabled(False)
        # self.test_func.setVisible(False)

    def set_dark_theme(self):
        for mode in MODES:
            btn = getattr(self, f'pushButton_{mode}')
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(f'Interface/Dark_theme/{mode}(dark_theme).png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            btn.setIcon(icon)
            btn.setIconSize(QtCore.QSize(35, 35))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('Interface/Dark_theme/delete_actions(dark_theme).png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_delete_actions.setIcon(icon)
        self.pushButton_delete_actions.setIconSize(QtCore.QSize(35, 35))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('Interface/Dark_theme/delete_figures(dark_theme).png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_delete_figures.setIcon(icon)
        self.pushButton_delete_figures.setIconSize(QtCore.QSize(35, 35))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('Interface/Dark_theme/delete_pencil(dark_theme).png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_delete_pencil.setIcon(icon)
        self.pushButton_delete_pencil.setIconSize(QtCore.QSize(35, 35))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('Interface/Dark_theme/delete_labels(dark_theme).png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_delete_labels.setIcon(icon)
        self.pushButton_delete_labels.setIconSize(QtCore.QSize(35, 35))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('Interface/Dark_theme/save.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_save.setIcon(icon)

        self.setStyleSheet(open('Interface/Dark_theme\PlayCreator_dark_theme.css').read())

    def set_light_theme(self):
        for mode in MODES:
            btn = getattr(self, f'pushButton_{mode}')
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(f'Interface/Light_theme/{mode}(light_theme).png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            btn.setIcon(icon)
            btn.setIconSize(QtCore.QSize(35, 35))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('Interface/Light_theme/delete_actions(light_theme).png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_delete_actions.setIcon(icon)
        self.pushButton_delete_actions.setIconSize(QtCore.QSize(35, 35))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('Interface/Light_theme/delete_figures(light_theme).png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_delete_figures.setIcon(icon)
        self.pushButton_delete_figures.setIconSize(QtCore.QSize(35, 35))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('Interface/Light_theme/delete_pencil(light_theme).png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_delete_pencil.setIcon(icon)
        self.pushButton_delete_pencil.setIconSize(QtCore.QSize(35, 35))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('Interface/Light_theme/delete_labels(light_theme).png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_delete_labels.setIcon(icon)
        self.pushButton_delete_labels.setIconSize(QtCore.QSize(35, 35))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('Interface/Light_theme/save.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_save.setIcon(icon)

        self.setStyleSheet('')

    def test_fn(self):
        print('--------------------------------------')
        print(f'МОД: {self.field.mode}')
        # print(f'ТЕКУЩИЙ ЛЭЙБЛ: {self.field.current_label}')
        # print(f'КОНФИГ: {self.field.config}')
        # print(f'ФИГУРЫ: {self.field.figures}')
        # print(f'ФОКУС: {self.field.focusItem()}')
        # print(f'ВЫБРАННЫЕ ИТЕМЫ: {self.field.selectedItems()}')
        # print(f'ЛЭЙБЛЫ: {self.field.labels}')
        # print(f'СПИСОК ИТЕМОВ: {self.field.items()}')
        # print(f'КОЛИЧЕСТВО ИТЕМОВ НА СЦЕНЕ: {len(self.field.items())}')
        # print(f'ИГРОКИ: {self.field.first_team_players}')

        # print(f'current_action_lines: {self.field.current_action_lines}')
        print(f'allow_painting: {self.field.allow_painting}')
        # print(f'painting: {self.field.painting}')
        # print(f'mouse_pressed_painting: {self.field.mouse_pressed_painting}')
        # print(f'current_player: {self.field.current_player}')
        # print(f'start_pos: {self.field.start_pos}')
        # print(f'last_start_pos: {self.field.last_start_pos}')
        # print(f'current_line: {self.field.current_line}')
        # print(f'current_action_lines: {self.field.current_action_lines}')
        # print(f'action_number_temp: {self.field.action_number_temp}')
        # print(f'figures: {self.field.figures}')
        # print(f'current_figure: {self.field.current_figure}')
        # print(f'labels: {self.field.labels}')
        # print(f'current_label: {self.field.current_label')
        # print(f'pencil: {self.field.pencil}')

    def save_on_picture(self):
        save_window = QFileDialog()
        save_window.setDefaultSuffix('.jpg')
        save_window.setOption(QFileDialog.Option.DontConfirmOverwrite, False)
        filters = 'JPEG (*.jpg *.jpeg *.jpe *.jfif);; TIFF (*.tif *.tiff);; PNG (*.png)'
        url_filter = save_window.getSaveFileName(self, 'Сохранить', filter=filters, initialFilter='PNG (*.png)')
        if len(url_filter[0]) >= 1:
            poly = self.graphics_view.mapToScene(
                QRect(0, 0, self.graphics_view.width() - 14, self.graphics_view.height() - 13))
            rect = poly.boundingRect()
            if rect.x() < 0:
                rect.setWidth(rect.width() + rect.x())
                rect.setX(- self.field.border_width / 2)
            if rect.y() <= 0:
                rect.setHeight(rect.height() + rect.y())
                rect.setY(- self.field.border_width / 2)
            img = QImage(int(rect.width()), int(rect.height()), QImage.Format_ARGB8565_Premultiplied)
            img.fill(QColor(Qt.white))
            painter = QPainter(img)
            painter.setRenderHints(QPainter.HighQualityAntialiasing)
            self.field.render(painter, source=rect)
            img.save(f'{url_filter[0]}')
            painter.end()

    def set_user_color(self):
        color_dialog = QColorDialog()
        if color_dialog.exec():
            self.set_color(color_dialog.selectedColor().name())

    def presentation_mode(self):
        self.tabWidget_game_type.setVisible(not self.action_presentation.isChecked())
        self.label_current_zoom.setVisible(not self.action_presentation.isChecked())

    def combobox_font_changed(self, font):
        if self.field.current_label is not None:
            self.field.current_label.font.setFamily(font.family())
            self.field.current_label.setFont(self.field.current_label.font)
            self.fontComboBox.clearFocus()
            self.field.setFocusItem(self.field.current_label.proxy)
            self.field.current_label.grabKeyboard()
        else:
            self.field.set_config('font_type', font)

    def font_size_changed(self, font_size):
        if self.field.current_label:
            self.field.current_label.font.setPointSize(int(font_size))
            self.field.current_label.setFont(self.field.current_label.font)
            self.comboBox_font_size.clearFocus()
            self.field.setFocusItem(self.field.current_label.proxy)
            self.field.current_label.grabKeyboard()
        else:
            self.field.set_config('font_size', int(font_size))

    def bold_changed(self, bold_condition):
        if self.field.current_label:
            self.field.current_label.font.setBold(bold_condition)
            self.field.current_label.setFont(self.field.current_label.font)
            self.pushButton_bold.clearFocus()
            self.field.setFocusItem(self.field.current_label.proxy)
            self.field.current_label.grabKeyboard()
        else:
            self.field.set_config('bold', bold_condition)

    def italic_changed(self, italic_condition):
        if self.field.current_label:
            self.field.current_label.font.setItalic(italic_condition)
            self.field.current_label.setFont(self.field.current_label.font)
            self.pushButton_italic.clearFocus()
            self.field.setFocusItem(self.field.current_label.proxy)
            self.field.current_label.grabKeyboard()
        else:
            self.field.set_config('bold', italic_condition)

    def underline_changed(self, underline_condition):
        if self.field.current_label:
            self.field.current_label.font.setUnderline(underline_condition)
            self.field.current_label.setFont(self.field.current_label.font)
            self.pushButton_underline.clearFocus()
            self.field.setFocusItem(self.field.current_label.proxy)
            self.field.current_label.grabKeyboard()
        else:
            self.field.set_config('underline', underline_condition)

    def color_changed(self, color):
        if self.field.current_label:
            self.field.current_label.color = color
            self.field.current_label.setStyleSheet(f'''background-color: transparent;\n
                                                             Border:0px dashed black;\n
                                                             color:{self.field.current_label.color};\n''')
            self.field.setFocusItem(self.field.current_label.proxy)
            self.field.current_label.grabKeyboard()
        else:
            self.field.set_config('color', color)

    def label_editing_finished(self):
        self.fontComboBox.setCurrentFont(self.field.config['font_type'])
        self.comboBox_font_size.setCurrentText(str(self.field.config['font_size']))
        self.pushButton_bold.setChecked(self.field.config['bold'])
        self.pushButton_italic.setChecked(self.field.config['italic'])
        self.pushButton_underline.setChecked(self.field.config['underline'])
        self.pushButton_current_color.setStyleSheet(f'background-color: {self.field.config["color"]};')

    def update_window_font_config(self):
        self.fontComboBox.setCurrentFont(self.field.current_label.font)
        self.comboBox_font_size.setCurrentText(str(self.field.current_label.font.pointSize()))
        self.pushButton_bold.setChecked(self.field.current_label.font.bold())
        self.pushButton_italic.setChecked(self.field.current_label.font.italic())
        self.pushButton_underline.setChecked(self.field.current_label.font.underline())
        self.pushButton_current_color.setStyleSheet(f'background-color: {self.field.current_label.color};')

    def reset_settings(self):
        self.comboBox_team_type_football.setEnabled(True)
        if self.comboBox_team_type_football.currentIndex() == 1:
            self.lineEdit_yards_football.setEnabled(False)
        else:
            self.lineEdit_yards_football.setEnabled(True)
        self.pushButton_place_first_team_football.setEnabled(True)
        self.pushButton_add_additional_off_football.setEnabled(True)
        self.pushButton_add_additional_off_football.setVisible(False)
        self.pushButton_del_additional_off_football.setEnabled(False)
        self.pushButton_del_additional_off_football.setVisible(False)
        self.pushButton_place_second_team_football.setEnabled(False)
        self.pushButton_delete_second_team_football.setEnabled(False)
        self.pushButton_delete_all_players_football.setEnabled(False)
        self.lineEdit_yards_flag.setEnabled(True)
        self.pushButton_place_off_team_flag.setEnabled(True)
        self.pushButton_add_additional_off_flag.setEnabled(True)
        self.pushButton_add_additional_off_flag.setVisible(False)
        self.pushButton_del_additional_off_flag.setEnabled(False)
        self.pushButton_del_additional_off_flag.setVisible(False)
        self.pushButton_place_def_team_flag.setEnabled(False)
        self.pushButton_delete_def_team_flag.setEnabled(False)
        self.pushButton_delete_all_players_flag.setEnabled(False)

        self.field.first_team_placed = None
        self.field.first_team_players.clear()
        self.field.additional_offence_player = None
        self.field.second_team_placed = None
        self.field.second_team_players.clear()

        self.field.allow_painting = False
        self.field.painting = False
        self.field.mouse_pressed_painting = False
        self.field.current_player = None
        self.field.player_center_pos = None
        self.field.start_pos = None
        self.field.last_start_pos = None
        self.field.current_line = None
        self.field.current_action_lines.clear()
        self.field.action_number_temp = None

        # self.field.current_figure = None
        # self.field.figures.clear()

        # self.field.current_label = None
        # self.field.labels.clear()

        # self.field.pencil.clear()

        self.field.mode = 'move'
        getattr(self, f'pushButton_{self.field.mode}').setChecked(True)

    def set_color(self, color):
        self.pushButton_current_color.setStyleSheet(f'background-color: {color};')
        self.colorChanged.emit(color)

    def set_game_type(self, value):
        self.field.clear()
        self.reset_settings()
        if value == 0:
            self.field.create_football_field_full()
            self.field.setSceneRect(
                QRectF(0, 0, self.field.football_field_width, self.field.football_field_length))
        elif value == 1:
            self.field.create_flag_field_full()
            self.field.setSceneRect(
                QRectF(0, 0, self.field.flag_field_width, self.field.flag_field_length))

    def team_type_changed(self):
        if self.comboBox_team_type_football.currentIndex() == 1:
            self.lineEdit_yards_football.setEnabled(False)
        else:
            self.lineEdit_yards_football.setEnabled(True)

    def set_zoom(self, value):
        self.label_current_zoom.setText(f'Приближение: {value}%')

    def place_first_team_football(self):
        if not self.field.first_team_placed:
            if self.comboBox_team_type_football.currentIndex() == 0:
                self.create_first_team_players_football('offence', self.players.offence_football, self.players.offence_football_coordinates)
                self.field.first_team_placed = 'offence'
                self.pushButton_add_additional_off_football.setVisible(True)
                self.pushButton_add_additional_off_football.setEnabled(True)
                self.pushButton_del_additional_off_football.setVisible(True)
                self.pushButton_del_additional_off_football.setEnabled(False)
                self.set_gui_first_team_placed()
            elif self.comboBox_team_type_football.currentIndex() == 1:
                self.create_first_team_players_football('kick', self.players.kickoff_football, self.players.kickoff_football_coordinates)
                self.field.first_team_placed = 'kick'
                self.set_gui_first_team_placed()
            elif self.comboBox_team_type_football.currentIndex() == 2:
                if int(self.lineEdit_yards_football.text()) >= 30:
                    self.create_first_team_players_football('punt', self.players.punt_football, self.players.punt_coordinates)
                    self.field.first_team_placed = 'punt'
                    self.set_gui_first_team_placed()
                else:
                    self.lineEdit_yards_football.setText('30')
            elif self.comboBox_team_type_football.currentIndex() == 3:
                if int(self.lineEdit_yards_football.text()) <= 50:
                    self.create_first_team_players_football('field_goal', self.players.field_goal_off_football, self.players.field_goal_off_coordinates)
                    self.field.first_team_placed = 'field_goal'
                    self.set_gui_first_team_placed()
                else:
                    self.lineEdit_yards_football.setText('50')
            # self.field.set_players_flags()

    def set_gui_first_team_placed(self):
        self.pushButton_place_first_team_football.setEnabled(False)
        self.pushButton_place_second_team_football.setEnabled(True)
        self.lineEdit_yards_football.setEnabled(False)
        self.comboBox_team_type_football.setEnabled(False)
        self.pushButton_delete_all_players_football.setEnabled(True)

    def create_first_team_players_football(self, team_type, players, players_coordinates):
        if team_type == 'offence' or team_type == 'punt' or team_type == 'field_goal':
            for i, team_number in enumerate(players):
                if i == 10 and team_type == 'punt' and int(self.lineEdit_yards_football.text()) >= 95:
                    item = Player(*team_number,
                                  players_coordinates[i][0],
                                  players_coordinates[i][1],
                                  119 * self.field.football_one_yard - self.players.player_size / 2,
                                  players_coordinates[i][3],
                                  players_coordinates[i][4], )
                else:
                    item = Player(*team_number,
                                  players_coordinates[i][0],
                                  players_coordinates[i][1],
                                  players_coordinates[i][2] + self.get_yards_to_end_zone(),
                                  players_coordinates[i][3],
                                  players_coordinates[i][4], )
                self.field.addItem(item)
                self.field.first_team_players.append(item)
        else:
            for i, team_number in enumerate(players):
                item = Player(*team_number, *players_coordinates[i])
                self.field.addItem(item)
                self.field.first_team_players.append(item)

    def place_second_team_football(self):
        if not self.field.second_team_placed:
            if self.field.first_team_placed == 'offence':
                self.create_second_team_football('defence', self.players.defence_football, self.players.defence_football_coordinates)
                self.field.second_team_placed = 'defence'
            elif self.field.first_team_placed == 'kick':
                self.create_second_team_football('kick_ret', self.players.kickoff_return_football, self.players.kickoff_return_coordinates)
                self.field.second_team_placed = 'kick_ret'
            elif self.field.first_team_placed == 'punt':
                self.create_second_team_football('punt_ret', self.players.punt_return_football, self.players.punt_return_coordinates)
                self.field.second_team_placed = 'punt_ret'
            elif self.field.first_team_placed == 'field_goal':
                self.create_second_team_football('field_goal_def', self.players.field_goal_def_football, self.players.field_goal_def_coordinates)
                self.field.second_team_placed = 'field_goal_def'
            self.pushButton_place_second_team_football.setEnabled(False)
            self.pushButton_delete_second_team_football.setEnabled(True)
            # self.field.set_players_flags()

    def create_second_team_football(self, team_type, players, players_coordinates):
        for i, team_number in enumerate(players):
            if (team_type == 'punt_ret' and i == 10) or (team_type == 'kick_ret'):
                item = Player(*team_number, *players_coordinates[i])
            elif team_type == 'field_goal_def' and i == 10 and int(self.lineEdit_yards_football.text()) > 20:
                item = Player(*team_number,
                              players_coordinates[i][0],
                              players_coordinates[i][1],
                              self.field.football_five_yard,
                              players_coordinates[i][3],
                              players_coordinates[i][4], )
            elif team_type == 'defence' and i == 10 and int(self.lineEdit_yards_football.text()) < 3:
                item = Player(*team_number,
                              players_coordinates[i][0],
                              players_coordinates[i][1],
                              players_coordinates[i][2] + self.get_yards_to_end_zone() + 3 * self.field.football_one_yard,
                              players_coordinates[i][3],
                              players_coordinates[i][4], )
            else:
                item = Player(*team_number,
                              players_coordinates[i][0],
                              players_coordinates[i][1],
                              players_coordinates[i][2] + self.get_yards_to_end_zone(),
                              players_coordinates[i][3],
                              players_coordinates[i][4], )
            self.field.addItem(item)
            self.field.second_team_players.append(item)

    def place_additional_offence_player_football(self):
        if self.field.first_team_placed == 'offence' and not self.field.additional_offence_player:
            self.field.additional_offence_player = Player(self.players.additional_player_football[0],
                                                          self.players.additional_player_football[1],
                                                          self.players.additional_player_football[2],
                                                          self.players.additional_player_football[3],
                                                          self.players.additional_player_football[4] + self.get_yards_to_end_zone(),
                                                          self.players.additional_player_football[5],
                                                          self.players.additional_player_football[6], )
            self.field.addItem(self.field.additional_offence_player)
            self.pushButton_add_additional_off_football.setEnabled(False)
            self.pushButton_del_additional_off_football.setEnabled(True)
            # self.field.set_players_flags()

    def delete_first_team_actions(self):
        if self.field.first_team_placed:
            for player in self.field.first_team_players:
                player.delete_actions()
        if self.field.additional_offence_player:
            self.field.additional_offence_player.delete_actions()

    def delete_second_team_actions(self):
        if self.field.second_team_placed:
            for player in self.field.second_team_players:
                player.delete_actions()

    def delete_actions(self):
        self.delete_first_team_actions()
        self.delete_second_team_actions()
        self.field.update()

    def delete_second_team_football(self):
        if self.field.second_team_placed:
            self.delete_second_team_actions()
            group = self.field.createItemGroup(self.field.second_team_players)
            self.field.removeItem(group)
            self.field.second_team_players.clear()
            self.field.second_team_placed = None
            self.pushButton_place_second_team_football.setEnabled(True)
            self.pushButton_delete_second_team_football.setEnabled(False)
            self.field.update()

    def delete_additional_offence_player_football(self):
        if self.field.additional_offence_player:
            self.field.additional_offence_player.delete_actions()
            self.field.removeItem(self.field.additional_offence_player)
            self.field.additional_offence_player = None
            self.pushButton_add_additional_off_football.setEnabled(True)
            self.pushButton_del_additional_off_football.setEnabled(False)
            self.field.update()

    def delete_teams_football(self):
        if self.field.first_team_placed:
            self.delete_first_team_actions()
            group = self.field.createItemGroup(self.field.first_team_players)
            self.field.removeItem(group)
            self.field.first_team_players.clear()
            self.field.first_team_placed = None
            self.delete_additional_offence_player_football()
            self.pushButton_add_additional_off_football.setVisible(False)
            self.pushButton_del_additional_off_football.setVisible(False)
        self.delete_second_team_football()
        self.field.delete_figures()
        self.field.delete_labels()
        self.field.delete_pencil()
        self.field.update()
        self.reset_settings()

    def get_yards_to_end_zone(self):
        if self.tabWidget_game_type.currentIndex() == 0:
            yards = self.field.football_ten_yard + \
                    (self.field.football_field_length - 2 * self.field.football_ten_yard) \
                    / 100 * int(self.lineEdit_yards_football.text())
            return yards
        elif self.tabWidget_game_type.currentIndex() == 1:
            yards = self.field.flag_ten_yard + \
                    (self.field.flag_field_length - 2 * self.field.flag_ten_yard) \
                    / 50 * int(self.lineEdit_yards_flag.text())
            return yards

    def check_max_yards_flag(self, value):
        try:
            if int(value) >= 50:
                self.lineEdit_yards_flag.setText(str(49))
        except ValueError:
            pass

    def place_off_team_flag(self):
        if not self.field.first_team_placed:
            self.create_players_flag(self.players.offence_flag, self.players.offence_flag_coordinates)
            self.field.first_team_placed = True
            self.pushButton_add_additional_off_flag.setVisible(True)
            self.pushButton_add_additional_off_flag.setEnabled(True)
            self.pushButton_del_additional_off_flag.setVisible(True)
            self.pushButton_del_additional_off_flag.setEnabled(False)
            self.pushButton_place_off_team_flag.setEnabled(False)
            self.lineEdit_yards_flag.setEnabled(False)
            self.pushButton_place_def_team_flag.setEnabled(True)
            self.pushButton_delete_all_players_flag.setEnabled(True)
            # self.field.set_players_flags()

    def place_def_team_flag(self):
        if not self.field.second_team_placed:
            self.create_players_flag(self.players.defence_flag, self.players.defence_flag_coordinates)
            self.field.second_team_placed = True
            # self.field.set_players_flags()
            self.pushButton_place_def_team_flag.setEnabled(False)
            self.pushButton_delete_def_team_flag.setEnabled(True)

    def create_players_flag(self, players, players_coordinates):
        for i, team_number in enumerate(players):
            item = Player(*team_number,
                          players_coordinates[i][0],
                          players_coordinates[i][1],
                          players_coordinates[i][2] + self.get_yards_to_end_zone(),
                          players_coordinates[i][3],
                          players_coordinates[i][4], )
            self.field.addItem(item)
            if not self.field.first_team_placed:
                self.field.first_team_players.append(item)
            else:
                self.field.second_team_players.append(item)

    def place_additional_player_flag(self):
        if self.field.first_team_placed is True and not self.field.additional_offence_player:
            self.field.additional_offence_player = Player(self.players.additional_player_flag[0],
                                                          self.players.additional_player_flag[1],
                                                          self.players.additional_player_flag[2],
                                                          self.players.additional_player_flag[3],
                                                          self.players.additional_player_flag[4] + self.get_yards_to_end_zone(),
                                                          self.players.additional_player_flag[5],
                                                          self.players.additional_player_flag[6], )
            self.field.addItem(self.field.additional_offence_player)
            self.pushButton_add_additional_off_flag.setEnabled(False)
            self.pushButton_del_additional_off_flag.setEnabled(True)
            # self.field.set_players_flags()

    def delete_def_team_flag(self):
        if self.field.second_team_placed:
            self.delete_second_team_actions()
            group = self.field.createItemGroup(self.field.second_team_players)
            self.field.removeItem(group)
            self.field.second_team_players.clear()
            self.field.second_team_placed = None
            self.pushButton_place_def_team_flag.setEnabled(True)
            self.pushButton_delete_def_team_flag.setEnabled(False)
            self.field.update()

    def delete_additional_offence_player_flag(self):
        if self.field.additional_offence_player:
            self.field.additional_offence_player.delete_actions()
            self.field.removeItem(self.field.additional_offence_player)
            self.field.additional_offence_player = None
            self.pushButton_add_additional_off_flag.setEnabled(True)
            self.pushButton_del_additional_off_flag.setEnabled(False)
            self.field.update()

    def delete_teams_flag(self):
        if self.field.first_team_placed:
            self.delete_first_team_actions()
            group = self.field.createItemGroup(self.field.first_team_players)
            self.field.removeItem(group)
            self.field.first_team_players.clear()
            self.field.first_team_placed = None
            self.delete_additional_offence_player_flag()
        self.delete_def_team_flag()
        self.field.delete_figures()
        self.field.delete_labels()
        self.field.delete_pencil()
        self.field.update()
        self.reset_settings()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    play_creator = PlayCreator()
    play_creator.show()

    sys.exit(app.exec_())