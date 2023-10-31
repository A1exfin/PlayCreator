import os.path
from typing import Tuple, Any

from PlayCreator_ui import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import sys
from Custom_graphics_view import CustomGraphicsView
from Custom_scene import Field
from Data_players import PlayersData
from Data_field import FieldData
from Item_player import Player
from datetime import datetime
from Dialog_windows import DialogNewSchemeAction, DialogAbout
from List_item_custom import CustomListItem

from Item_line_action import ActionLine##########################

# style = os.path.join(os.path.dirname(__file__), 'PlayCreator_dark_theme.css')


def timeit(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        print(datetime.now() - start)
        return result
    return wrapper


MODES = ('move', 'erase', 'route', 'block', 'motion', 'rectangle', 'ellipse', 'pencil', 'label')
COLORS = ('#000000', '#800000', '#400080', '#0004ff', '#8d8b9a', '#22b14c',
          '#ff0000', '#ff00ea', '#ff80ff', '#ff8000', '#dcdc00', '#00ff00')


class PlayCreator(QMainWindow, Ui_MainWindow):
    colorChanged = Signal(str)
    version = '2.0'

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.chosen_list_item_football = None
        self.chosen_list_item_flag = None
        self.current_scene = None
        self.graphics_view = CustomGraphicsView(self.centralwidget)
        self.gridLayout_7.addWidget(self.graphics_view, 0, 0, 1, 1)
        self.field_data = FieldData()
        self.players = PlayersData(self.field_data)
        if False:
            self.current_scene = Field(self, self.field_data, 'football')
        # self.reset_settings()
        self.label_set_current_zoom(self.graphics_view.current_zoom)
        self.enable_disable_gui(False)

        action_theme_group = QActionGroup(self)
        action_theme_group.addAction(self.action_dark_theme)
        action_theme_group.addAction(self.action_light_theme)
        action_theme_group.setExclusive(True)
        self.action_dark_theme.setChecked(True)
        self.set_dark_theme()
        # self.action_light_theme.setChecked(True)
        # self.set_light_theme()

        self.toolBar_main.toggleViewAction().setText('Панель инструментов')
        self.toolBar_main.toggleViewAction().setStatusTip('Панель инструментов')
        self.menu_additional.insertAction(self.action_QB_Wrist, self.toolBar_main.toggleViewAction())

        mode_group = QButtonGroup(self)
        mode_group.setExclusive(True)
        for mode in MODES:
            button = getattr(self, f'pushButton_{mode}')
            button.pressed.connect(lambda mode=mode: self.current_scene.set_mode(mode))
            mode_group.addButton(button)
        for i, color in enumerate(COLORS):
            button = getattr(self, f'pushButton_color_{i}')
            button.setStyleSheet(f'background-color: {color};')
            button.pressed.connect(lambda color=color: self.set_color(color))

        self.graphics_view.zoomChanged.connect(self.label_set_current_zoom)
        self.tabWidget_game_type.currentChanged.connect(self.set_game_type)

        # self.lineEdit_yards_football.textChanged.connect(self.check_max_min_yards_football)
        self.comboBox_team_type_football.currentIndexChanged.connect(self.team_type_changed_football)
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

        self.comboBox_line_thickness.currentTextChanged.connect(lambda thickness: self.current_scene.set_config('line_thickness', int(thickness)))
        self.fontComboBox.currentFontChanged.connect(self.combobox_font_changed)
        self.comboBox_font_size.currentTextChanged.connect(self.font_size_changed)
        self.pushButton_bold.toggled.connect(self.bold_changed)
        self.pushButton_italic.toggled.connect(self.italic_changed)
        self.pushButton_underline.toggled.connect(self.underline_changed)
        self.pushButton_current_color.clicked.connect(self.set_user_color)
        self.colorChanged.connect(self.color_changed)

        self.action_exit.triggered.connect(lambda: sys.exit(app.exec()))
        self.action_save.triggered.connect(self.save_on_picture)
        self.action_save_all.triggered.connect(self.save_all_schemes_on_picture)
        self.action_about.triggered.connect(self.about_clicked)
        self.action_new_scheme.triggered.connect(self.new_scheme_dialog_action)
        self.action_presentation_mode.toggled.connect(self.presentation_mode)
        self.action_dark_theme.toggled.connect(self.set_dark_theme)
        self.action_light_theme.toggled.connect(self.set_light_theme)

        self.pushButton_add_scheme_football.clicked.connect(self.add_new_scheme_football)
        self.pushButton_delete_scheme_football.clicked.connect(self.delete_current_scheme_football)
        self.pushButton_scheme_move_up_football.clicked.connect(self.move_up_current_scheme_football)
        self.pushButton_scheme_move_down_football.clicked.connect(self.move_down_current_scheme_football)
        self.listWidget_schemes_football.itemDoubleClicked.connect(self.choose_current_scheme_football)
        self.pushButton_edit_scheme_football.clicked.connect(self.edit_current_scheme_football)

        self.pushButton_add_scheme_flag.clicked.connect(self.add_new_scheme_flag)
        self.pushButton_delete_scheme_flag.clicked.connect(self.delete_current_scheme_flag)
        self.pushButton_scheme_move_up_flag.clicked.connect(self.move_up_current_scheme_flag)
        self.pushButton_scheme_move_down_flag.clicked.connect(self.move_down_current_scheme_flag)
        self.listWidget_schemes_flag.itemDoubleClicked.connect(self.choose_current_scheme_flag)
        self.pushButton_edit_scheme_flag.clicked.connect(self.edit_current_scheme_flag)

        # self.test_func.clicked.connect(self.test_fn)############################## тестовая функция
        # self.test_func.clicked.connect(self.set_dark_theme)  ############################## тестовая функция
        # self.test_func.clicked.connect(self.set_light_theme)  ############################## тестовая функция
        self.test_func.clicked.connect(self.qwe)  ############################## тестовая функция
        # self.test_func.setEnabled(False)
        # self.test_func.setVisible(False)
        self.new_scheme_dialog_action()


    def qwe(self):
        if self.graphics_view.isVisible():
            self.graphics_view.setVisible(False)
        else:
            self.graphics_view.setVisible(True)


    # @timeit###################################################################################################
    def save_all_schemes_on_picture(self, checked=None):
        dialog = QFileDialog(parent=self, caption='Укажите путь для сохранения схем')
        url = dialog.getExistingDirectory()
        files_with_same_name_list = []
        if url:
            for item_number in range(self.listWidget_schemes_football.count()):
                url_files_list = list(map(str.lower, QDir(url).entryList(QDir.Files)))
                item = self.listWidget_schemes_football.item(item_number)
                if f'{item.text().lower()}.png' in url_files_list:
                    files_with_same_name_list.append(item.text())
                scheme_top_point, scheme_bot_point = self.get_top_bot_points_for_items_on_scene(item.scene)
                if scheme_top_point is not None and item.text() not in files_with_same_name_list:
                    scheme_top_point -= 30  # Отступ от крёв схемы
                    scheme_bot_point += 30  # Отступ от крёв схемы
                    if scheme_top_point < 0:  # Ограничение изображения размерами сцены
                        scheme_top_point = 0
                    if scheme_bot_point > self.field_data.football_field_length:  # Ограничение изображения размерами сцены
                        scheme_bot_point = self.field_data.football_field_length
                    rect = QRectF(0, scheme_top_point, item.scene.width(), scheme_bot_point - scheme_top_point)
                    image = QImage(int(rect.width()), int(rect.height()), QImage.Format_ARGB8565_Premultiplied)
                    image.fill(QColor(Qt.white))
                    painter = QPainter(image)
                    painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
                    item.scene.render(painter, source=rect)
                    image.save(f'{url}/{item.text()}.png')
                    painter.end()

            for item_number in range(self.listWidget_schemes_flag.count()):
                url_files_list = list(map(str.lower, QDir(url).entryList(QDir.Files)))
                item = self.listWidget_schemes_flag.item(item_number)
                if f'{item.text().lower()}.png' in url_files_list:
                    files_with_same_name_list.append(item.text())
                scheme_top_point, scheme_bot_point = self.get_top_bot_points_for_items_on_scene(item.scene)
                if scheme_top_point is not None and item.text() not in files_with_same_name_list:
                    scheme_top_point -= 30  # Отступ от крёв схемы
                    scheme_bot_point += 30  # Отступ от крёв схемы
                    if scheme_top_point < 0:  # Ограничение изображения размерами сцены
                        scheme_top_point = 0
                    if scheme_bot_point > self.field_data.flag_field_length:  # Ограничение изображения размерами сцены
                        scheme_bot_point = self.field_data.flag_field_length
                    rect = QRectF(0, scheme_top_point, item.scene.width(), scheme_bot_point - scheme_top_point)
                    image = QImage(int(rect.width()), int(rect.height()), QImage.Format_ARGB8565_Premultiplied)
                    image.fill(QColor(Qt.white))
                    painter = QPainter(image)
                    painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
                    item.scene.render(painter, source=rect)
                    image.save(f'{url}/{item.text()}.png')
                    painter.end()
            if files_with_same_name_list:
                if len(files_with_same_name_list) == 1:
                    message = f'Схема с названием: {f", ".join(files_with_same_name_list)} не была сохранена из-за совпадения с именами файлов в выбранной папке. Для сохранения измените её название.'
                else:
                    message = f'Схемы с названиями: {f", ".join(files_with_same_name_list)} не были сохранены из-за совпадения с именами файлов в выбранной папке. Для сохранения измените их названия.'
                dialog = QMessageBox().about(self, 'Совпадение названий схем', message)

    def get_top_bot_points_for_items_on_scene(self, scene: Field) -> tuple[None, None] | tuple[float | Any, float | Any]:###### Проверить ещё раз условие для низа итема
        if scene.first_team_placed:
            top_y = scene.first_team_players[0].y()
            bot_y = scene.first_team_players[0].y() + scene.first_team_players[0].height
        elif len(scene.figures) != 0:
            top_y = scene.figures[0].rect().y()
            bot_y = scene.figures[0].rect().bottom()
        elif len(scene.labels) != 0:
            top_y = scene.labels[0].y
            bot_y = scene.labels[0].y + scene.labels[0].height
        elif len(scene.pencil) != 0:
            top_y = scene.pencil[0].line().y1()
            bot_y = scene.pencil[0].line().y1()
        else:
            return None, None

        for player in scene.first_team_players:
            if player.y() < top_y:
                top_y = player.y()
            if player.y() + player.height > bot_y:
                bot_y = player.y() + player.height
            for action in player.actions.values():
                for line in action:
                    if isinstance(line, ActionLine):
                        if line.line().y1() < top_y:
                            top_y = line.line().y1()
                        if line.line().y1() > bot_y:
                            bot_y = line.line().y1()
                        if line.line().y2() < top_y:
                            top_y = line.line().y2()
                        if line.line().y2() > bot_y:
                            bot_y = line.line().y2()

        if scene.additional_offence_player:
            if scene.additional_offence_player.y() < top_y:
                top_y = scene.additional_offence_player.y()
            if scene.additional_offence_player.y() + scene.additional_offence_player.height > bot_y:
                bot_y = scene.additional_offence_player.y() + scene.additional_offence_player.height
            for action in scene.additional_offence_player.actions.values():
                for line in action:
                    if isinstance(line, ActionLine):
                        if line.line().y1() < top_y:
                            top_y = line.line().y1()
                        if line.line().y1() > bot_y:
                            bot_y = line.line().y1()
                        if line.line().y2() < top_y:
                            top_y = line.line().y2()
                        if line.line().y2() > bot_y:
                            bot_y = line.line().y2()

        for player in scene.second_team_players:
            if player.y() < top_y:
                top_y = player.y()
            if player.y() + player.height > bot_y:
                bot_y = player.y() + player.height
            for action in player.actions.values():
                for line in action:
                    if isinstance(line, ActionLine):
                        if line.line().y1() < top_y:
                            top_y = line.line().y1()
                        if line.line().y1() > bot_y:
                            bot_y = line.line().y1()
                        if line.line().y2() < top_y:
                            top_y = line.line().y2()
                        if line.line().y2() > bot_y:
                            bot_y = line.line().y2()

        for line in scene.pencil:
            if line.line().y1() < top_y:
                top_y = line.line().y1()
            if line.line().y1() > bot_y:
                bot_y = line.line().y1()
            if line.line().y2() < top_y:
                top_y = line.line().y2()
            if line.line().y2() > bot_y:
                bot_y = line.line().y2()

        for figure in scene.figures:
            if figure.rect().y() < top_y:
                top_y = figure.rect().y()
            if figure.rect().bottom() > bot_y:
                bot_y = figure.rect().bottom()

        for label in scene.labels:
            if label.y < top_y:
                top_y = label.y
            if label.y + label.height > bot_y:
                bot_y = label.y + label.height
        return top_y, bot_y

    '''-----------------------------------------------------------------------------------------------------------------
    --------------------------------------------Общие для полей методы--------------------------------------------------
    -----------------------------------------------------------------------------------------------------------------'''
    def connect_signals_to_current_scene(self):
        self.pushButton_delete_actions.clicked.connect(self.delete_actions)
        self.pushButton_delete_figures.clicked.connect(self.current_scene.delete_figures)
        self.pushButton_delete_labels.clicked.connect(self.current_scene.delete_labels)
        self.pushButton_delete_pencil.clicked.connect(self.current_scene.delete_pencil)
        self.current_scene.modeChanged.connect(lambda mode: getattr(self, f'pushButton_{mode}').setChecked(True))
        self.current_scene.labelDoubleClicked.connect(self.update_window_font_config)
        self.current_scene.labelEditingFinished.connect(self.label_editing_finished)

    def new_scheme_dialog_action(self):
        dialog = DialogNewSchemeAction(parent=self)
        dialog.exec()
        if dialog.result() == 1 and len(dialog.line_edit.text()) > 0:
            if dialog.radio_button_football.isChecked():
                if self.listWidget_schemes_football.count() == 0:
                    self.enable_disable_gui(True)
                item = CustomListItem(Field(self, self.field_data, 'football'), dialog.line_edit.text())
                self.listWidget_schemes_football.addItem(item)
                self.listWidget_schemes_football.setCurrentItem(item)
                self.choose_current_scheme_football()
                self.tabWidget_game_type.setCurrentIndex(0)
                self.connect_signals_to_current_scene()
            elif dialog.radio_button_flag.isChecked():
                if self.listWidget_schemes_flag.count() == 0:
                    self.enable_disable_gui(True)
                item = CustomListItem(Field(self, self.field_data, 'flag'), dialog.line_edit.text())
                self.listWidget_schemes_flag.addItem(item)
                self.listWidget_schemes_flag.setCurrentItem(item)
                self.choose_current_scheme_flag()
                self.tabWidget_game_type.setCurrentIndex(1)
                self.connect_signals_to_current_scene()

    def set_game_type(self, value: int):
        if self.current_scene:
            self.current_scene.view_point = self.graphics_view.mapToScene(QPoint(self.graphics_view.width() // 2, self.graphics_view.height() // 2))
            self.current_scene.zoom = self.graphics_view.current_zoom
            temp_scene = QGraphicsScene()
            self.graphics_view.setScene(temp_scene)
            temp_scene.deleteLater()
            del temp_scene
        if value == 0:
            if self.listWidget_schemes_football.count() != 0:
                if not self.pushButton_move.isEnabled():
                    self.enable_disable_gui(True)
                self.current_scene = self.chosen_list_item_football.scene
                # self.current_scene = self.listWidget_schemes_football.selectedItems()[0].scene
                self.graphics_view.setScene(self.current_scene)
                self.graphics_view.set_current_zoom(self.current_scene.zoom)
                self.graphics_view.centerOn(self.current_scene.view_point)
                self.set_gui_for_current_scene_football()
            else:
                self.enable_disable_gui(False)
                self.current_scene = None
        elif value == 1:
            if self.listWidget_schemes_flag.count() != 0:
                if not self.pushButton_move.isEnabled():
                    self.enable_disable_gui(True)
                self.current_scene = self.chosen_list_item_flag.scene
                self.graphics_view.setScene(self.current_scene)
                self.graphics_view.set_current_zoom(self.current_scene.zoom)
                self.graphics_view.centerOn(self.current_scene.view_point)
                self.set_gui_for_current_scene_flag()
            else:
                self.enable_disable_gui(False)
                self.current_scene = None

    def save_on_picture(self):
        save_window = QFileDialog(parent=self)
        save_window.setDefaultSuffix('.jpg')
        save_window.setOption(QFileDialog.Option.DontConfirmOverwrite, False)
        filters = 'JPEG (*.jpg *.jpeg *.jpe *.jfif);; TIFF (*.tif *.tiff);; PNG (*.png)'
        url, _ = save_window.getSaveFileName(self, 'Сохранить', filter=filters, selectedFilter='PNG (*.png)')
        if url:
            poly = self.graphics_view.mapToScene(QRect(0, 0, self.graphics_view.width() - 14, self.graphics_view.height() - 13))
            rect = poly.boundingRect()
            if rect.x() < 0:
                rect.setWidth(rect.width() + rect.x())
                rect.setX(- self.current_scene.field_data.border_width / 2)
            if rect.y() <= 0:
                rect.setHeight(rect.height() + rect.y())
                rect.setY(- self.current_scene.field_data.border_width / 2)
            img = QImage(int(rect.width()), int(rect.height()), QImage.Format_ARGB8565_Premultiplied)
            img.fill(QColor(Qt.white))
            painter = QPainter(img)
            painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
            self.current_scene.render(painter, source=rect)
            img.save(f'{url}')
            painter.end()

    def combobox_font_changed(self, font: QFont):
        if self.current_scene.current_label is not None:
            self.current_scene.current_label.font.setFamily(font.family())
            self.current_scene.current_label.setFont(self.current_scene.current_label.font)
            self.fontComboBox.clearFocus()
            self.current_scene.setFocusItem(self.current_scene.current_label.proxy)
            self.current_scene.current_label.grabKeyboard()
        else:
            self.current_scene.set_config('font_type', font)

    def font_size_changed(self, font_size: str):
        if self.current_scene.current_label:
            self.current_scene.current_label.font.setPointSize(int(font_size))
            self.current_scene.current_label.setFont(self.current_scene.current_label.font)
            self.comboBox_font_size.clearFocus()
            self.current_scene.setFocusItem(self.current_scene.current_label.proxy)
            self.current_scene.current_label.grabKeyboard()
        else:
            self.current_scene.set_config('font_size', int(font_size))

    def bold_changed(self, bold_condition: bool):
        if self.current_scene.current_label:
            self.current_scene.current_label.font.setBold(bold_condition)
            self.current_scene.current_label.setFont(self.current_scene.current_label.font)
            self.pushButton_bold.clearFocus()
            self.current_scene.setFocusItem(self.current_scene.current_label.proxy)
            self.current_scene.current_label.grabKeyboard()
        else:
            self.current_scene.set_config('bold', bold_condition)

    def italic_changed(self, italic_condition: bool):
        if self.current_scene.current_label:
            self.current_scene.current_label.font.setItalic(italic_condition)
            self.current_scene.current_label.setFont(self.current_scene.current_label.font)
            self.pushButton_italic.clearFocus()
            self.current_scene.setFocusItem(self.current_scene.current_label.proxy)
            self.current_scene.current_label.grabKeyboard()
        else:
            self.current_scene.set_config('italic', italic_condition)

    def underline_changed(self, underline_condition: bool):
        if self.current_scene.current_label:
            self.current_scene.current_label.font.setUnderline(underline_condition)
            self.current_scene.current_label.setFont(self.current_scene.current_label.font)
            self.pushButton_underline.clearFocus()
            self.current_scene.setFocusItem(self.current_scene.current_label.proxy)
            self.current_scene.current_label.grabKeyboard()
        else:
            self.current_scene.set_config('underline', underline_condition)

    def color_changed(self, color: str):
        if self.current_scene.current_label:
            self.current_scene.current_label.color = color
            self.current_scene.current_label.setStyleSheet(f'''background-color: transparent;\n
                                                             Border:0px dashed black;\n
                                                             color:{self.current_scene.current_label.color};\n''')
            self.current_scene.setFocusItem(self.current_scene.current_label.proxy)
            self.current_scene.current_label.grabKeyboard()
        else:
            self.current_scene.set_config('color', color)

    def label_editing_finished(self):
        self.fontComboBox.setCurrentFont(self.current_scene.config['font_type'])
        self.comboBox_font_size.setCurrentText(str(self.current_scene.config['font_size']))
        self.pushButton_bold.setChecked(self.current_scene.config['bold'])
        self.pushButton_italic.setChecked(self.current_scene.config['italic'])
        self.pushButton_underline.setChecked(self.current_scene.config['underline'])
        self.pushButton_current_color.setStyleSheet(f'background-color: {self.current_scene.config["color"]};')

    def update_window_font_config(self):
        self.fontComboBox.setCurrentFont(self.current_scene.current_label.font)
        self.comboBox_font_size.setCurrentText(str(self.current_scene.current_label.font.pointSize()))
        self.pushButton_bold.setChecked(self.current_scene.current_label.font.bold())
        self.pushButton_italic.setChecked(self.current_scene.current_label.font.italic())
        self.pushButton_underline.setChecked(self.current_scene.current_label.font.underline())
        self.pushButton_current_color.setStyleSheet(f'background-color: {self.current_scene.current_label.color};')

    def delete_first_team_actions(self):
        if self.current_scene.first_team_placed:
            for player in self.current_scene.first_team_players:
                player.delete_actions()
        if self.current_scene.additional_offence_player:
            self.current_scene.additional_offence_player.delete_actions()

    def delete_second_team_actions(self):
        if self.current_scene.second_team_placed:
            for player in self.current_scene.second_team_players:
                player.delete_actions()

    def delete_actions(self):
        self.delete_first_team_actions()
        self.delete_second_team_actions()
        if self.current_scene.allow_painting:
            self.delete_drawing_actions()
        self.current_scene.update()

    def delete_drawing_actions(self):
        self.current_scene.current_player.setSelected(False)
        self.current_scene.current_player.hover = False
        self.current_scene.allow_painting = False
        self.current_scene.painting = False
        self.current_scene.mouse_pressed_painting = False
        self.current_scene.current_player = None
        self.current_scene.player_center_pos = None
        self.current_scene.start_pos = None
        self.current_scene.last_start_pos = None
        self.current_scene.removeItem(self.current_scene.current_line)
        self.current_scene.current_line = None
        for line in self.current_scene.current_action_lines:
            self.current_scene.removeItem(line)
        self.current_scene.current_action_lines.clear()
        self.current_scene.action_number_temp = None

    def enable_disable_gui(self, condition: bool):
        for mode in MODES:
            button = getattr(self, f'pushButton_{mode}')
            button.setEnabled(condition)
        for i in range(12):
            button = getattr(self, f'pushButton_color_{i}')
            button.setEnabled(condition)
        self.pushButton_current_color.setEnabled(condition)
        self.pushButton_delete_actions.setEnabled(condition)
        self.pushButton_delete_figures.setEnabled(condition)
        self.pushButton_delete_labels.setEnabled(condition)
        self.pushButton_delete_pencil.setEnabled(condition)
        self.pushButton_bold.setEnabled(condition)
        self.pushButton_italic.setEnabled(condition)
        self.pushButton_underline.setEnabled(condition)
        self.comboBox_font_size.setEnabled(condition)
        self.comboBox_line_thickness.setEnabled(condition)
        self.fontComboBox.setEnabled(condition)
        self.action_save.setEnabled(condition)
        self.action_save_all.setEnabled(condition)
        self.pushButton_edit_scheme_football.setEnabled(condition)
        self.pushButton_edit_scheme_flag.setEnabled(condition)

        self.pushButton_delete_scheme_football.setEnabled(condition)
        self.pushButton_scheme_move_up_football.setEnabled(condition)
        self.pushButton_scheme_move_down_football.setEnabled(condition)

        self.pushButton_delete_scheme_flag.setEnabled(condition)
        self.pushButton_scheme_move_up_flag.setEnabled(condition)
        self.pushButton_scheme_move_down_flag.setEnabled(condition)

        if not condition:
            self.comboBox_team_type_football.setEnabled(condition)
            self.lineEdit_yards_football.setEnabled(condition)
            self.pushButton_place_first_team_football.setEnabled(condition)
            self.pushButton_add_additional_off_football.setEnabled(condition)
            self.pushButton_add_additional_off_football.setVisible(condition)
            self.pushButton_del_additional_off_football.setEnabled(condition)
            self.pushButton_del_additional_off_football.setVisible(condition)
            self.pushButton_place_second_team_football.setEnabled(condition)
            self.pushButton_delete_second_team_football.setEnabled(condition)
            self.pushButton_delete_all_players_football.setEnabled(condition)
            self.pushButton_delete_scheme_football.setEnabled(condition)
            self.pushButton_scheme_move_up_football.setEnabled(condition)
            self.pushButton_scheme_move_down_football.setEnabled(condition)

            self.lineEdit_yards_flag.setEnabled(condition)
            self.pushButton_place_off_team_flag.setEnabled(condition)
            self.pushButton_add_additional_off_flag.setEnabled(condition)
            self.pushButton_add_additional_off_flag.setVisible(condition)
            self.pushButton_del_additional_off_flag.setEnabled(condition)
            self.pushButton_del_additional_off_flag.setVisible(condition)
            self.pushButton_place_def_team_flag.setEnabled(condition)
            self.pushButton_delete_def_team_flag.setEnabled(condition)
            self.pushButton_delete_all_players_flag.setEnabled(condition)

    '''-----------------------------------------------------------------------------------------------------------------
    ----------------------------------------------Методы футбольного поля-----------------------------------------------
    -----------------------------------------------------------------------------------------------------------------'''
    def add_new_scheme_football(self):
        if self.listWidget_schemes_football.count() == 0:
            self.enable_disable_gui(True)
        item = CustomListItem(Field(self, self.field_data, 'football'), '')
        self.listWidget_schemes_football.addItem(item)
        self.listWidget_schemes_football.setCurrentItem(item)
        self.edit_current_scheme_football()
        self.choose_current_scheme_football()
        self.connect_signals_to_current_scene()

    def delete_current_scheme_football(self):
        item = self.listWidget_schemes_football.takeItem(self.listWidget_schemes_football.currentRow())
        if self.listWidget_schemes_football.count() > 0:
            if item is self.chosen_list_item_football:
            # if item is self.listWidget_schemes_football.selectedItems()[0]:
                self.chosen_list_item_football = None
                self.choose_current_scheme_football()
        else:
            if self.current_scene:
                self.current_scene.deleteLater()
                self.current_scene = None
            self.chosen_list_item_football = None
            # self.set_gui_for_current_scene_football()
            self.enable_disable_gui(False)
        del item

    def edit_current_scheme_football(self):
        item = self.listWidget_schemes_football.currentItem()
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
        self.listWidget_schemes_football.editItem(item)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    def choose_current_scheme_football(self):
        if self.listWidget_schemes_football.count() != 0:
            if self.current_scene:  # Запоминание точки обзора текущей сцены и зума, при смене на другую сцену
                self.current_scene.view_point = self.graphics_view.mapToScene(QPoint(self.graphics_view.width() // 2, self.graphics_view.height() // 2))
                self.current_scene.zoom = self.graphics_view.current_zoom
            for item_number in range(self.listWidget_schemes_football.count()):
                item = self.listWidget_schemes_football.item(item_number)
                if self.action_dark_theme.isChecked():
                    item.setForeground(QColor('#b1b1b1'))
                else:
                    item.setForeground(QColor(Qt.black))
            self.chosen_list_item_football = self.listWidget_schemes_football.currentItem()
            if self.action_dark_theme.isChecked():
                self.chosen_list_item_football.setForeground(QColor('#27c727'))
            else:
                self.chosen_list_item_football.setForeground(QColor('#1a6aa7'))
            self.chosen_list_item_football.setSelected(True)
            self.current_scene = self.chosen_list_item_football.scene
            # self.listWidget_schemes_football.currentItem().setSelected(True)
            # self.current_scene = self.listWidget_schemes_football.selectedItems()[0].scene
            self.graphics_view.setScene(self.current_scene)
            self.graphics_view.set_current_zoom(self.current_scene.zoom)
            self.graphics_view.centerOn(self.current_scene.view_point)
            self.set_gui_for_current_scene_football()

    def move_up_current_scheme_football(self):
        row = self.listWidget_schemes_football.currentRow()
        if row > 0:
            item = self.listWidget_schemes_football.takeItem(row)
            row -= 1
            self.listWidget_schemes_football.insertItem(row, item)
            self.listWidget_schemes_football.setCurrentItem(item)

    def move_down_current_scheme_football(self):
        row = self.listWidget_schemes_football.currentRow()
        if row < self.listWidget_schemes_football.count():
            item = self.listWidget_schemes_football.takeItem(row)
            row += 1
            self.listWidget_schemes_football.insertItem(row, item)
            self.listWidget_schemes_football.setCurrentItem(item)

    def team_type_changed_football(self):
        if self.comboBox_team_type_football.currentIndex() == 1:
            self.lineEdit_yards_football.setEnabled(False)
            self.lineEdit_yards_football.setText(str(65))
        else:
            self.lineEdit_yards_football.setEnabled(True)

    def get_yards_to_end_zone_football(self):
        yards = self.field_data.football_ten_yard + self.field_data.football_one_yard * int(self.lineEdit_yards_football.text())
        return yards

    # def check_max_min_yards_football(self, value: str):
    #     try:
    #         if self.comboBox_team_type_football.currentIndex() == 2 and int(value) < 20:
    #             self.lineEdit_yards_football.setText('20')
    #         elif self.comboBox_team_type_football.currentIndex() == 3 and int(value) > 60:
    #             self.lineEdit_yards_football.setText('60')
    #     except ValueError:
    #         pass

    def place_first_team_football(self):
        if not self.current_scene.first_team_placed:
            if self.comboBox_team_type_football.currentIndex() == 0:
                self.create_first_team_players_football('offence', self.players.offence_football, self.players.offence_football_coordinates)
                self.current_scene.first_team_placed = 'offence'
                self.current_scene.first_team_position = int(self.lineEdit_yards_football.text())
                self.pushButton_add_additional_off_football.setVisible(True)
                self.pushButton_add_additional_off_football.setEnabled(True)
                self.pushButton_del_additional_off_football.setVisible(True)
                self.pushButton_del_additional_off_football.setEnabled(False)
                self.set_gui_first_team_placed_football()
            elif self.comboBox_team_type_football.currentIndex() == 1:
                self.create_first_team_players_football('kick', self.players.kickoff_football, self.players.kickoff_football_coordinates)
                self.current_scene.first_team_placed = 'kick'
                self.current_scene.first_team_position = 65
                self.set_gui_first_team_placed_football()
            elif self.comboBox_team_type_football.currentIndex() == 2:
                if int(self.lineEdit_yards_football.text()) >= 20:
                    self.create_first_team_players_football('punt', self.players.punt_football, self.players.punt_coordinates)
                    self.current_scene.first_team_placed = 'punt'
                    self.current_scene.first_team_position = int(self.lineEdit_yards_football.text())
                    self.set_gui_first_team_placed_football()
                else:
                    self.lineEdit_yards_football.setText('20')
            elif self.comboBox_team_type_football.currentIndex() == 3:
                if int(self.lineEdit_yards_football.text()) <= 70:
                    self.create_first_team_players_football('field_goal', self.players.field_goal_off_football, self.players.field_goal_off_coordinates)
                    self.current_scene.first_team_placed = 'field_goal'
                    self.current_scene.first_team_position = int(self.lineEdit_yards_football.text())
                    self.set_gui_first_team_placed_football()
                else:
                    self.lineEdit_yards_football.setText('70')

    def create_first_team_players_football(self, team_type: str, players: list, players_coordinates: list):
        if team_type == 'offence' or team_type == 'punt' or team_type == 'field_goal':
            for i, team_number in enumerate(players):
                if i == 10 and team_type == 'punt' and int(self.lineEdit_yards_football.text()) >= 95:
                    item = Player(*team_number,
                                  players_coordinates[i][0],
                                  players_coordinates[i][1],
                                  119 * self.current_scene.field_data.football_one_yard - self.players.player_size / 2,
                                  players_coordinates[i][3],
                                  players_coordinates[i][4], )
                else:
                    item = Player(*team_number,
                                  players_coordinates[i][0],
                                  players_coordinates[i][1],
                                  players_coordinates[i][2] + self.get_yards_to_end_zone_football(),
                                  players_coordinates[i][3],
                                  players_coordinates[i][4], )
                self.current_scene.addItem(item)
                self.current_scene.first_team_players.append(item)
        else:
            for i, team_number in enumerate(players):
                item = Player(*team_number, *players_coordinates[i])
                self.current_scene.addItem(item)
                self.current_scene.first_team_players.append(item)

    def place_second_team_football(self):
        if not self.current_scene.second_team_placed:
            if self.current_scene.first_team_placed == 'offence':
                self.create_second_team_football('defence', self.players.defence_football, self.players.defence_football_coordinates)
                self.current_scene.second_team_placed = 'defence'
            elif self.current_scene.first_team_placed == 'kick':
                self.create_second_team_football('kick_ret', self.players.kickoff_return_football, self.players.kickoff_return_coordinates)
                self.current_scene.second_team_placed = 'kick_ret'
            elif self.current_scene.first_team_placed == 'punt':
                self.create_second_team_football('punt_ret', self.players.punt_return_football, self.players.punt_return_coordinates)
                self.current_scene.second_team_placed = 'punt_ret'
            elif self.current_scene.first_team_placed == 'field_goal':
                self.create_second_team_football('field_goal_def', self.players.field_goal_def_football, self.players.field_goal_def_coordinates)
                self.current_scene.second_team_placed = 'field_goal_def'
            self.set_gui_for_second_team_football(True)
            # self.pushButton_place_second_team_football.setEnabled(False)
            # self.pushButton_delete_second_team_football.setEnabled(True)

    def create_second_team_football(self, team_type: str, players: list, players_coordinates: list):
        for i, team_number in enumerate(players):
            if (team_type == 'punt_ret' and i == 10) or (team_type == 'kick_ret'):
                item = Player(*team_number, *players_coordinates[i])
            elif team_type == 'field_goal_def' and i == 10 and int(self.lineEdit_yards_football.text()) > 20:
                item = Player(*team_number,
                              players_coordinates[i][0],
                              players_coordinates[i][1],
                              self.current_scene.field_data.football_five_yard,
                              players_coordinates[i][3],
                              players_coordinates[i][4], )
            elif team_type == 'defence' and i == 10 and int(self.lineEdit_yards_football.text()) < 3:
                item = Player(*team_number,
                              players_coordinates[i][0],
                              players_coordinates[i][1],
                              players_coordinates[i][2] + self.get_yards_to_end_zone_football() + 3 * self.current_scene.field_data.football_one_yard,
                              players_coordinates[i][3],
                              players_coordinates[i][4], )
            else:
                item = Player(*team_number,
                              players_coordinates[i][0],
                              players_coordinates[i][1],
                              players_coordinates[i][2] + self.get_yards_to_end_zone_football(),
                              players_coordinates[i][3],
                              players_coordinates[i][4], )
            self.current_scene.addItem(item)
            self.current_scene.second_team_players.append(item)

    def place_additional_offence_player_football(self):
        if self.current_scene.first_team_placed == 'offence' and not self.current_scene.additional_offence_player:
            self.current_scene.additional_offence_player = Player(self.players.additional_player_football[0],
                                                                  self.players.additional_player_football[1],
                                                                  self.players.additional_player_football[2],
                                                                  self.players.additional_player_football[3],
                                                                  self.players.additional_player_football[4] + self.get_yards_to_end_zone_football(),
                                                                  self.players.additional_player_football[5],
                                                                  self.players.additional_player_football[6], )
            self.current_scene.addItem(self.current_scene.additional_offence_player)
            self.set_gui_for_additional_offence_player_football(True)
            # self.pushButton_add_additional_off_football.setEnabled(False)
            # self.pushButton_del_additional_off_football.setEnabled(True)

    def delete_second_team_football(self):
        if self.current_scene.second_team_placed:
            self.delete_second_team_actions()
            group = self.current_scene.createItemGroup(self.current_scene.second_team_players)
            self.current_scene.removeItem(group)
            self.current_scene.second_team_players.clear()
            self.current_scene.second_team_placed = None
            self.set_gui_for_second_team_football(False)
            # self.pushButton_place_second_team_football.setEnabled(True)
            # self.pushButton_delete_second_team_football.setEnabled(False)
            if self.current_scene.allow_painting and\
                    (self.current_scene.current_player.team == 'defence'
                     or self.current_scene.current_player.team == 'punt_ret'
                     or self.current_scene.current_player.team == 'kick_ret'
                     or self.current_scene.current_player.team == 'field_goal_def'):
                self.delete_drawing_actions()
            self.current_scene.update()

    def delete_additional_offence_player_football(self):
        if self.current_scene.additional_offence_player:
            self.current_scene.additional_offence_player.delete_actions()
            self.current_scene.removeItem(self.current_scene.additional_offence_player)
            self.current_scene.additional_offence_player = None
            self.set_gui_for_additional_offence_player_football(False)
            if self.current_scene.allow_painting and self.current_scene.current_player.team == 'offence_additional':
                self.delete_drawing_actions()
            # self.pushButton_add_additional_off_football.setEnabled(True)
            # self.pushButton_del_additional_off_football.setEnabled(False)
            self.current_scene.update()

    def delete_teams_football(self):
        if self.current_scene.first_team_placed:
            self.delete_first_team_actions()
            group = self.current_scene.createItemGroup(self.current_scene.first_team_players)
            self.current_scene.removeItem(group)
            self.current_scene.first_team_players.clear()
            self.current_scene.first_team_placed = None
            self.current_scene.first_team_position = None
            self.delete_additional_offence_player_football()
            # self.pushButton_add_additional_off_football.setVisible(False)
            # self.pushButton_del_additional_off_football.setVisible(False)
        self.delete_second_team_football()
        self.current_scene.delete_figures()
        self.current_scene.delete_labels()
        self.current_scene.delete_pencil()
        self.set_gui_all_teams_deleted_football()
        if self.current_scene.allow_painting:
            self.delete_drawing_actions()
        self.current_scene.update()
        # self.reset_settings()

    def set_gui_first_team_placed_football(self):
        self.pushButton_place_first_team_football.setEnabled(False)
        self.pushButton_place_second_team_football.setEnabled(True)
        self.lineEdit_yards_football.setEnabled(False)
        self.comboBox_team_type_football.setEnabled(False)
        self.pushButton_delete_all_players_football.setEnabled(True)

    def set_gui_for_second_team_football(self, condition: bool):
        self.pushButton_place_second_team_football.setEnabled(not condition)
        self.pushButton_delete_second_team_football.setEnabled(condition)

    def set_gui_for_additional_offence_player_football(self, condition: bool):
        self.pushButton_add_additional_off_football.setEnabled(not condition)
        self.pushButton_del_additional_off_football.setEnabled(condition)

    def set_gui_all_teams_deleted_football(self):
        self.comboBox_team_type_football.setEnabled(True)
        if self.comboBox_team_type_football.currentIndex() == 1:
            self.lineEdit_yards_football.setEnabled(False)
        else:
            self.lineEdit_yards_football.setEnabled(True)
        self.pushButton_place_first_team_football.setEnabled(True)
        self.pushButton_add_additional_off_football.setEnabled(False)
        self.pushButton_add_additional_off_football.setVisible(False)
        self.pushButton_del_additional_off_football.setEnabled(False)
        self.pushButton_del_additional_off_football.setVisible(False)
        self.pushButton_place_second_team_football.setEnabled(False)
        self.pushButton_delete_second_team_football.setEnabled(False)
        self.pushButton_delete_all_players_football.setEnabled(False)

    def set_gui_for_current_scene_football(self):
        self.fontComboBox.setCurrentFont(self.current_scene.config['font_type'])
        self.comboBox_font_size.setCurrentText(str(self.current_scene.config['font_size']))
        self.pushButton_bold.setChecked(self.current_scene.config['bold'])
        self.pushButton_italic.setChecked(self.current_scene.config['italic'])
        self.pushButton_underline.setChecked(self.current_scene.config['underline'])
        self.comboBox_line_thickness.setCurrentText(str(self.current_scene.config['line_thickness']))
        self.pushButton_current_color.setStyleSheet(f'background-color: {self.current_scene.config["color"]};')
        getattr(self, f'pushButton_{self.current_scene.mode}').setChecked(True)

        if self.current_scene.first_team_placed:
            self.comboBox_team_type_football.setEnabled(False)
            self.lineEdit_yards_football.setText(str(self.current_scene.first_team_position))
            self.lineEdit_yards_football.setEnabled(False)
            self.pushButton_place_first_team_football.setEnabled(False)
            self.pushButton_delete_all_players_football.setEnabled(True)
            if self.current_scene.first_team_placed == 'offence':
                self.comboBox_team_type_football.setCurrentIndex(0)
                self.pushButton_add_additional_off_football.setVisible(True)
                self.pushButton_del_additional_off_football.setVisible(True)
                condition = (lambda additional_offence_player: True if additional_offence_player is not None else False)(self.current_scene.additional_offence_player)
                self.set_gui_for_additional_offence_player_football(condition)
                condition = (lambda second_team_placed: True if second_team_placed is not None else False)(self.current_scene.second_team_placed)
                self.set_gui_for_second_team_football(condition)
            elif self.current_scene.first_team_placed == 'kick':
                self.comboBox_team_type_football.setCurrentIndex(1)
            elif self.current_scene.first_team_placed == 'punt':
                self.comboBox_team_type_football.setCurrentIndex(2)
            elif self.current_scene.first_team_placed == 'field_goal':
                self.comboBox_team_type_football.setCurrentIndex(3)
        else:
            self.set_gui_all_teams_deleted_football()

    '''-----------------------------------------------------------------------------------------------------------------
    ---------------------------------------------Методы флаг-футбольного поля-------------------------------------------
    -----------------------------------------------------------------------------------------------------------------'''
    def add_new_scheme_flag(self):
        if self.listWidget_schemes_flag.count() == 0:
            self.enable_disable_gui(True)
        item = CustomListItem(Field(self, self.field_data, 'flag'), '')
        self.listWidget_schemes_flag.addItem(item)
        self.listWidget_schemes_flag.setCurrentItem(item)
        self.edit_current_scheme_flag()
        self.choose_current_scheme_flag()
        self.connect_signals_to_current_scene()
        # self.set_gui_for_current_scene_flag()

    def delete_current_scheme_flag(self):
        item = self.listWidget_schemes_flag.takeItem(self.listWidget_schemes_flag.currentRow())
        if self.listWidget_schemes_flag.count() > 0:
            if item is self.chosen_list_item_flag:
                self.chosen_list_item_flag = None
                self.choose_current_scheme_flag()
        else:
            if self.current_scene:
                self.current_scene.deleteLater()
                self.current_scene = None
            self.chosen_list_item_flag = None
            # self.set_gui_for_current_scene_flag()
            self.enable_disable_gui(False)
        del item

    def edit_current_scheme_flag(self):
        item = self.listWidget_schemes_flag.currentItem()
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
        self.listWidget_schemes_flag.editItem(item)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    def choose_current_scheme_flag(self):
        if self.listWidget_schemes_flag.count() != 0:
            if self.current_scene:  # Запоминание точки обзора текущей сцены, при смене на другую сцену
                self.current_scene.view_point = self.graphics_view.mapToScene(QPoint(self.graphics_view.width() // 2, self.graphics_view.height() // 2))
                self.current_scene.zoom = self.graphics_view.current_zoom
            for item_number in range(self.listWidget_schemes_flag.count()):
                item = self.listWidget_schemes_flag.item(item_number)
                if self.action_dark_theme.isChecked():
                    item.setForeground(QColor('#b1b1b1'))
                else:
                    item.setForeground(QColor(Qt.black))
            self.chosen_list_item_flag = self.listWidget_schemes_flag.currentItem()
            if self.action_dark_theme.isChecked():
                self.chosen_list_item_flag.setForeground(QColor('#27c727'))
            else:
                self.chosen_list_item_flag.setForeground(QColor('#1a6aa7'))
            self.current_scene = self.chosen_list_item_flag.scene
            self.graphics_view.setScene(self.current_scene)
            self.graphics_view.set_current_zoom(self.current_scene.zoom)
            self.graphics_view.centerOn(self.current_scene.view_point)
            self.set_gui_for_current_scene_flag()

    def move_up_current_scheme_flag(self):
        row = self.listWidget_schemes_flag.currentRow()
        if row > 0:
            item = self.listWidget_schemes_flag.takeItem(row)
            row -= 1
            self.listWidget_schemes_flag.insertItem(row, item)
            self.listWidget_schemes_flag.setCurrentItem(item)

    def move_down_current_scheme_flag(self):
        row = self.listWidget_schemes_flag.currentRow()
        if row < self.listWidget_schemes_flag.count():
            item = self.listWidget_schemes_flag.takeItem(row)
            row += 1
            self.listWidget_schemes_flag.insertItem(row, item)
            self.listWidget_schemes_flag.setCurrentItem(item)

    def get_yards_to_end_zone_flag(self):
        yards = self.field_data.flag_ten_yard + self.field_data.flag_one_yard * int(self.lineEdit_yards_flag.text())
        return yards

    def check_max_yards_flag(self, value: str):
        try:
            if int(value) > 50:
                self.lineEdit_yards_flag.setText('50')
        except ValueError:
            pass

    def place_off_team_flag(self):
        if not self.current_scene.first_team_placed:
            self.create_players_flag(self.players.offence_flag, self.players.offence_flag_coordinates)
            self.current_scene.first_team_placed = True
            self.current_scene.first_team_position = int(self.lineEdit_yards_flag.text())
            self.pushButton_add_additional_off_flag.setVisible(True)
            self.pushButton_add_additional_off_flag.setEnabled(True)
            self.pushButton_del_additional_off_flag.setVisible(True)
            self.pushButton_del_additional_off_flag.setEnabled(False)
            self.pushButton_place_off_team_flag.setEnabled(False)
            self.lineEdit_yards_flag.setEnabled(False)
            self.pushButton_place_def_team_flag.setEnabled(True)
            self.pushButton_delete_all_players_flag.setEnabled(True)

    def set_gui_first_team_placed_flag(self):
        self.pushButton_add_additional_off_flag.setVisible(True)
        self.pushButton_add_additional_off_flag.setEnabled(True)
        self.pushButton_del_additional_off_flag.setVisible(True)
        self.pushButton_del_additional_off_flag.setEnabled(False)
        self.pushButton_place_off_team_flag.setEnabled(False)
        self.pushButton_place_def_team_flag.setEnabled(True)
        self.lineEdit_yards_flag.setEnabled(False)
        self.pushButton_delete_all_players_flag.setEnabled(True)

    def place_def_team_flag(self):
        if not self.current_scene.second_team_placed:
            self.create_players_flag(self.players.defence_flag, self.players.defence_flag_coordinates)
            self.current_scene.second_team_placed = True
            self.set_gui_for_def_team_flag(True)

    def create_players_flag(self, players: list, players_coordinates: list):
        for i, team_number in enumerate(players):
            item = Player(*team_number,
                          players_coordinates[i][0],
                          players_coordinates[i][1],
                          players_coordinates[i][2] + self.get_yards_to_end_zone_flag(),
                          players_coordinates[i][3],
                          players_coordinates[i][4], )
            self.current_scene.addItem(item)
            if not self.current_scene.first_team_placed:
                self.current_scene.first_team_players.append(item)
            else:
                self.current_scene.second_team_players.append(item)

    def place_additional_player_flag(self):
        if self.current_scene.first_team_placed is True and not self.current_scene.additional_offence_player:
            self.current_scene.additional_offence_player = Player(self.players.additional_player_flag[0],
                                                                  self.players.additional_player_flag[1],
                                                                  self.players.additional_player_flag[2],
                                                                  self.players.additional_player_flag[3],
                                                                  self.players.additional_player_flag[4] + self.get_yards_to_end_zone_flag(),
                                                                  self.players.additional_player_flag[5],
                                                                  self.players.additional_player_flag[6], )
            self.current_scene.addItem(self.current_scene.additional_offence_player)
            self.set_gui_for_additional_offence_player_flag(True)

    def delete_def_team_flag(self):
        if self.current_scene.second_team_placed:
            self.delete_second_team_actions()
            group = self.current_scene.createItemGroup(self.current_scene.second_team_players)
            self.current_scene.removeItem(group)
            self.current_scene.second_team_players.clear()
            self.current_scene.second_team_placed = None
            self.set_gui_for_def_team_flag(False)
            if self.current_scene.allow_painting and self.current_scene.current_player.team == 'defence':
                self.delete_drawing_actions()
            self.current_scene.update()

    def delete_additional_offence_player_flag(self):
        if self.current_scene.additional_offence_player:
            self.current_scene.additional_offence_player.delete_actions()
            self.current_scene.removeItem(self.current_scene.additional_offence_player)
            self.current_scene.additional_offence_player = None
            self.set_gui_for_additional_offence_player_flag(False)
            if self.current_scene.allow_painting and self.current_scene.current_player.team == 'offence_additional':
                self.delete_drawing_actions()
            self.current_scene.update()

    def delete_teams_flag(self):
        if self.current_scene.first_team_placed:
            self.delete_first_team_actions()
            group = self.current_scene.createItemGroup(self.current_scene.first_team_players)
            self.current_scene.removeItem(group)
            self.current_scene.first_team_players.clear()
            self.current_scene.first_team_placed = None
            self.current_scene.first_team_position = None
            self.delete_additional_offence_player_flag()
        self.delete_def_team_flag()
        self.current_scene.delete_figures()
        self.current_scene.delete_labels()
        self.current_scene.delete_pencil()
        self.set_gui_all_teams_deleted_flag()
        if self.current_scene.allow_painting:
            self.delete_drawing_actions()
        self.current_scene.update()
        # self.reset_settings()

    def set_gui_for_def_team_flag(self, condition: bool):
        self.pushButton_place_def_team_flag.setEnabled(not condition)
        self.pushButton_delete_def_team_flag.setEnabled(condition)

    def set_gui_for_additional_offence_player_flag(self, condition: bool):
        self.pushButton_add_additional_off_flag.setEnabled(not condition)
        self.pushButton_del_additional_off_flag.setEnabled(condition)

    def set_gui_all_teams_deleted_flag(self):
        self.lineEdit_yards_flag.setEnabled(True)
        self.pushButton_place_off_team_flag.setEnabled(True)
        self.pushButton_add_additional_off_flag.setEnabled(False)
        self.pushButton_add_additional_off_flag.setVisible(False)
        self.pushButton_del_additional_off_flag.setEnabled(False)
        self.pushButton_del_additional_off_flag.setVisible(False)
        self.pushButton_place_def_team_flag.setEnabled(False)
        self.pushButton_delete_def_team_flag.setEnabled(False)
        self.pushButton_delete_all_players_flag.setEnabled(False)

    def set_gui_for_current_scene_flag(self):
        self.fontComboBox.setCurrentFont(self.current_scene.config['font_type'])
        self.comboBox_font_size.setCurrentText(str(self.current_scene.config['font_size']))
        self.pushButton_bold.setChecked(self.current_scene.config['bold'])
        self.pushButton_italic.setChecked(self.current_scene.config['italic'])
        self.pushButton_underline.setChecked(self.current_scene.config['underline'])
        self.comboBox_line_thickness.setCurrentText(str(self.current_scene.config['line_thickness']))
        self.pushButton_current_color.setStyleSheet(f'background-color: {self.current_scene.config["color"]};')
        getattr(self, f'pushButton_{self.current_scene.mode}').setChecked(True)

        if self.current_scene.first_team_placed:
            self.lineEdit_yards_flag.setText(str(self.current_scene.first_team_position))
            self.lineEdit_yards_flag.setEnabled(False)
            self.pushButton_place_off_team_flag.setEnabled(False)
            self.pushButton_delete_all_players_flag.setEnabled(True)
            self.pushButton_add_additional_off_flag.setVisible(True)
            self.pushButton_del_additional_off_flag.setVisible(True)
            condition = (lambda additional_offence_player: True if additional_offence_player is not None else False)(self.current_scene.additional_offence_player)  #############################
            self.set_gui_for_additional_offence_player_flag(condition)
            condition = (lambda second_team_placed: True if second_team_placed is not None else False)(self.current_scene.second_team_placed)
            self.set_gui_for_def_team_flag(condition)
        else:
            self.set_gui_all_teams_deleted_flag()

    '''-----------------------------------------------------------------------------------------------------------------
    ------------------------------------Методы интерфейса напрямую не касающиеся полей----------------------------------
    -----------------------------------------------------------------------------------------------------------------'''
    def set_color(self, color: str):
        self.pushButton_current_color.setStyleSheet(f'background-color: {color};')
        self.colorChanged.emit(color)

    def set_user_color(self):
        color_dialog = QColorDialog()
        if color_dialog.exec():
            self.set_color(color_dialog.selectedColor().name())

    def label_set_current_zoom(self, value: int):
        self.label_current_zoom.setText(f'Приближение: {value}%')
        if self.current_scene:
            self.current_scene.zoom = value

    def set_dark_theme(self):
        self.setStyleSheet(open('Interface/Dark_theme/PlayCreator_dark_theme.css').read())
        # self.setStyleSheet('')
        for item_number in range(self.listWidget_schemes_flag.count()):
            item = self.listWidget_schemes_flag.item(item_number)
            item.setForeground(QColor('#b1b1b1'))
        if self.chosen_list_item_flag:
            self.chosen_list_item_flag.setForeground(QColor('#27c727'))
        for item_number in range(self.listWidget_schemes_football.count()):
            item = self.listWidget_schemes_football.item(item_number)
            item.setForeground(QColor('#b1b1b1'))
        if self.chosen_list_item_football:
            self.chosen_list_item_football.setForeground(QColor('#27c727'))
        icon = QIcon()
        icon.addPixmap(QPixmap('Interface/Dark_theme/save(dark_theme).png'))
        self.action_save.setIcon(icon)
        icon = QIcon()
        icon.addPixmap(QPixmap('Interface/Dark_theme/save_all(dark_theme).png'))
        self.action_save_all.setIcon(icon)
        icon = QIcon()
        icon.addPixmap(QPixmap('Interface/Dark_theme/new_scheme(dark_theme).png'))
        self.action_new_scheme.setIcon(icon)
        icon = QIcon()
        icon.addPixmap(QPixmap('Interface/Dark_theme/presentation_mode(dark_theme).png'))
        self.action_presentation_mode.setIcon(icon)

    def set_light_theme(self):
        self.setStyleSheet(open('Interface/Light_theme/PlayCreator_light_theme.css').read())
        # self.setStyleSheet('')
        for item_number in range(self.listWidget_schemes_flag.count()):
            item = self.listWidget_schemes_flag.item(item_number)
            item.setForeground(QColor(Qt.black))
        if self.chosen_list_item_flag:
            self.chosen_list_item_flag.setForeground(QColor('#1a6aa7'))
        for item_number in range(self.listWidget_schemes_football.count()):
            item = self.listWidget_schemes_football.item(item_number)
            item.setForeground(QColor(Qt.black))
        if self.chosen_list_item_football:
            self.chosen_list_item_football.setForeground(QColor('#1a6aa7'))
        icon = QIcon()
        icon.addPixmap(QPixmap('Interface/Light_theme/save(light_theme).png'))
        self.action_save.setIcon(icon)
        icon = QIcon()
        icon.addPixmap(QPixmap('Interface/Light_theme/save_all(light_theme).png'))
        self.action_save_all.setIcon(icon)
        icon = QIcon()
        icon.addPixmap(QPixmap('Interface/Light_theme/new_scheme(light_theme).png'))
        self.action_new_scheme.setIcon(icon)
        icon = QIcon()
        icon.addPixmap(QPixmap('Interface/Light_theme/presentation_mode(light_theme).png'))
        self.action_presentation_mode.setIcon(icon)

    def about_clicked(self):
        if self.action_dark_theme.isChecked():
            ico = 'Interface/tactic(dark128).png'
            color = '#27c727'
        else:
            ico = 'Interface/tactic(light128).png'
            color = '#1a6aa7'
        dialog = DialogAbout(self.version, ico, color, parent=self)
        dialog.exec()

    def presentation_mode(self):
        self.tabWidget_game_type.setVisible(not self.action_presentation_mode.isChecked())
        self.label_current_zoom.setVisible(not self.action_presentation_mode.isChecked())

    '''-----------------------------------------------------------------------------------------------------------------
    ------------------------------------------------------Методы отладки------------------------------------------------
    -----------------------------------------------------------------------------------------------------------------'''
    def test_fn(self):
        print('-' * 100)
        print(f'МОД: {self.current_scene.mode}')
        # print(f'ТЕКУЩИЙ ЛЭЙБЛ: {self.current_scene.current_label}')
        # print(f'КОНФИГ: {self.current_scene.config}')
        # print(f'ФИГУРЫ: {self.current_scene.figures}')
        # print(f'ФОКУС: {self.current_scene.focusItem()}')
        # print(f'ВЫБРАННЫЕ ИТЕМЫ: {self.current_scene.selectedItems()}')
        # print(f'ЛЭЙБЛЫ: {self.current_scene.labels}')
        # print(f'СПИСОК ИТЕМОВ: {self.current_scene.items()}')
        # print(f'КОЛИЧЕСТВО ИТЕМОВ НА СЦЕНЕ: {len(self.current_scene.items())}')
        # print(f'ИГРОКИ: {self.current_scene.first_team_players}')

        # print(f'current_action_lines: {self.current_scene.current_action_lines}')
        print(f'allow_painting: {self.current_scene.allow_painting}')
        # print(f'painting: {self.current_scene.painting}')
        # print(f'mouse_pressed_painting: {self.current_scene.mouse_pressed_painting}')
        # print(f'current_player: {self.current_scene.current_player}')
        # print(f'start_pos: {self.current_scene.start_pos}')
        # print(f'last_start_pos: {self.current_scene.last_start_pos}')
        # print(f'current_line: {self.current_scene.current_line}')
        # print(f'current_action_lines: {self.current_scene.current_action_lines}')
        # print(f'action_number_temp: {self.current_scene.action_number_temp}')
        # print(f'figures: {self.current_scene.figures}')
        # print(f'current_figure: {self.current_scene.current_figure}')
        # print(f'labels: {self.current_scene.labels}')
        # print(f'current_label: {self.current_scene.current_label')
        # print(f'pencil: {self.current_scene.pencil}')


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

        self.current_scene.first_team_placed = None
        self.current_scene.first_team_players.clear()
        self.current_scene.additional_offence_player = None
        self.current_scene.second_team_placed = None
        self.current_scene.second_team_players.clear()

        self.current_scene.allow_painting = False
        self.current_scene.painting = False
        self.current_scene.mouse_pressed_painting = False
        self.current_scene.current_player = None
        self.current_scene.player_center_pos = None
        self.current_scene.start_pos = None
        self.current_scene.last_start_pos = None
        self.current_scene.current_line = None
        self.current_scene.current_action_lines.clear()
        self.current_scene.action_number_temp = None

        # self.current_scene.current_figure = None
        # self.current_scene.figures.clear()

        # self.current_scene.current_label = None
        # self.current_scene.labels.clear()

        # self.current_scene.pencil.clear()

        self.current_scene.mode = 'move'
        getattr(self, f'pushButton_{self.current_scene.mode}').setChecked(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    play_creator = PlayCreator()
    play_creator.show()

    sys.exit(app.exec())
