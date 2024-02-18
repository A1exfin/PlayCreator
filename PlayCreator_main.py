from datetime import datetime
import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PlayCreator_ui import *
from Enum_flags import *
from Custom_widgets.Custom_graphics_view import CustomGraphicsView
from Custom_widgets.Custom_scene import Field
from Data.Data_players import PlayersData
from Data.Data_field import FieldData
from Custom_scene_items.Item_player import FirstTeamPlayer, SecondTeamPlayer
from Custom_widgets.Custom_dialog_log_in import DialogLogIn
from Custom_widgets.Custom_dialog_new_playbook import DialogNewPlaybook
from Custom_widgets.Custom_dialog_about import DialogAbout
from Custom_widgets.Custom_dialog_sign_up import DialogSignUp
from Custom_widgets.Custom_dialog_player_settings import DialogSecondTeamPlayerSettings, DialogFirstTeamPlayerSettings
from Custom_widgets.Custom_dialog_figure_settings import DialogFigureSettings
from Custom_widgets.Custom_list_item import CustomListItem

from Custom_scene_items.Item_line_action import ActionLine##########################
from Playbook import Playbook
# style = os.path.join(os.path.dirname(__file__), 'PlayCreator_dark_theme.css')


def timeit(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        print(datetime.now() - start)
        return result
    return wrapper


COLORS = ('#000000', '#800000', '#400080', '#0004ff', '#8d8b9a', '#22b14c',
          '#ff0000', '#ff00ea', '#ff80ff', '#ff8000', '#dcdc00', '#00ff00')


class PlayCreator(QMainWindow, Ui_MainWindow):
    colorChanged = Signal(str)
    version = '3.0'

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.user = None
        self.field_data = FieldData()
        self.players_data = PlayersData(self.field_data)
        self.playbook = None

        self.chosen_list_item = None
        self.current_scene: Field | None = None
        self.current_theme = None
        self.dialog_windows_text_color = None
        self.ico_about_path = None
        self.graphics_view = CustomGraphicsView(parent=self.centralwidget)
        self.gridLayout_2.addWidget(self.graphics_view, 0, 0, 2, 1)
        self.label_set_current_zoom(self.graphics_view.current_zoom)
        # self.enable_disable_gui(False)

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

        mode_group = QButtonGroup(parent=self)
        mode_group.setExclusive(True)
        for mode in Modes:
            button = getattr(self, f'pushButton_{mode.name}')
            button.pressed.connect(lambda mode=mode: self.current_scene.set_mode(mode))
            mode_group.addButton(button)
        for i, color in enumerate(COLORS):
            button = getattr(self, f'pushButton_color_{i}')
            button.setStyleSheet(f'background-color: {color};')
            button.pressed.connect(lambda color=color: self.set_color(color))

        self.graphics_view.zoomChanged.connect(self.label_set_current_zoom)

        # self.comboBox_team_type_football.currentIndexChanged.connect(self.team_type_changed_football)
        self.lineEdit_yards.textChanged.connect(lambda text: getattr(self, f'check_max_yards_{self.playbook.type.name}')(text))
        self.pushButton_place_first_team.clicked.connect(lambda: getattr(self, f'place_first_team_{self.playbook.type.name}')())
        self.pushButton_add_additional_off_player.clicked.connect(lambda: getattr(self, f'place_additional_offence_player_{self.playbook.type.name}')())
        self.pushButton_place_second_team.clicked.connect(lambda: getattr(self, f'place_second_team_{self.playbook.type.name}')())
        self.pushButton_del_additional_off_player.clicked.connect(self.delete_additional_offence_player)
        self.pushButton_delete_second_team.clicked.connect(self.delete_second_team)
        self.pushButton_delete_all_players.clicked.connect(self.clear_scene)
        self.comboBox_second_players_symbol.currentIndexChanged.connect(self.second_team_symbol_changed)

        self.comboBox_line_thickness.currentTextChanged.connect(lambda thickness: self.current_scene.set_config('line_thickness', int(thickness)))
        self.fontComboBox.currentFontChanged.connect(self.combobox_font_changed)
        self.comboBox_font_size.currentTextChanged.connect(self.font_size_changed)
        self.pushButton_bold.toggled.connect(self.bold_changed)
        self.pushButton_italic.toggled.connect(self.italic_changed)
        self.pushButton_underline.toggled.connect(self.underline_changed)
        self.pushButton_current_color.clicked.connect(self.set_user_color)
        self.colorChanged.connect(self.color_changed)

        self.action_user_login.triggered.connect(self.user_log_in)
        self.action_user_logout.triggered.connect(self.user_log_out)

        self.action_new_playbook.triggered.connect(self.create_new_playbook)
        self.action_close_programm.triggered.connect(lambda: sys.exit(app.exec()))
        self.action_save_like_picture.triggered.connect(self.save_on_picture)
        self.action_save_all_like_picture.triggered.connect(self.save_all_schemes_on_picture)
        self.action_about.triggered.connect(self.about_clicked)
        self.action_presentation_mode.toggled.connect(self.presentation_mode)
        self.action_dark_theme.toggled.connect(self.set_dark_theme)
        self.action_light_theme.toggled.connect(self.set_light_theme)

        self.pushButton_add_scheme.clicked.connect(self.add_new_scheme)
        self.pushButton_delete_scheme.clicked.connect(self.delete_current_scheme)
        self.pushButton_scheme_move_up.clicked.connect(self.move_up_current_scheme)
        self.pushButton_scheme_move_down.clicked.connect(self.move_down_current_scheme)
        self.pushButton_edit_scheme.clicked.connect(self.edit_current_scheme)
        self.pushButton_edit_playbook_name.clicked.connect(self.edit_playbook_name)
        self.listWidget_schemes.itemDoubleClicked.connect(self.choose_current_scheme)

        # self.test_func.clicked.connect(self.test_fn)############################## тестовая функция
        # self.test_func.clicked.connect(self.set_dark_theme)  ############################## тестовая функция
        # self.test_func.clicked.connect(self.set_light_theme)  ############################## тестовая функция
        self.test_func.clicked.connect(self.qwe)  ############################## тестовая функция
        # self.test_func.setEnabled(False)
        # self.test_func.setVisible(False)

        # self.user_log_in()    ##########################  Установить неактивным создание нового плейбука
        # self.sign_up()
        self.create_new_playbook()
        # dialog = DialogFigureSettings(self.dialog_windows_text_color, Modes.ellipse, True, '#ff0000', 2, True, '#333333', '#22', parent=self)
        # result = dialog.exec()
        # dialog = DialogFirstTeamPlayerSettings(self.dialog_windows_text_color, 'C', 'QW', '#ff0000', '#0000ff', 'right', parent=self)
        # result = dialog.exec()
        # dialog = DialogSecondTeamPlayerSettings(self.dialog_windows_text_color, 'W', '#ff0000', '#0000ff', 'x', parent=self)
        # result = dialog.exec()

    def qwe(self):
        ...
        print(self.current_scene.figures)
        # print(f'{self.playbook.schemes = }')
        # print(self.playbook)
        # self.set_dark_theme()
        # print(f'{self.current_scene.first_team_placed = }')
        # print(f'{self.current_scene.second_team_placed = }')
        # print(f'{self.current_scene.additional_offence_player = }')
        # if self.current_scene.first_team_placed:
        #     print(f'{self.current_scene.first_team_placed = }')
        #     for player in self.current_scene.first_team_players:
        #         print(f'{player.team = }')
        # if self.current_scene.second_team_placed:
        #     print(f'{self.current_scene.second_team_placed = }')
        #     for player in self.current_scene.second_team_players:
        #         print(f'{player.team = }')
        # if self.current_scene.additional_offence_player:
        #     print(f'{self.current_scene.additional_offence_player = }')
        #     print(f'{self.current_scene.additional_offence_player.team = }')
        # for rect in self.current_scene.figures:
            # print(f'{rect.rect().x() = }')
            # print(f'{rect.rect().y() = }')
            # print(f'{rect.scenePos().x() = }')
            # print(f'{rect.scenePos().y() = }')

    def user_log_in(self, wrong_login_pass=False):
        dialog = DialogLogIn(self.dialog_windows_text_color, wrong_login_pass=wrong_login_pass, parent=self)
        dialog.exec()
        result, login, password = dialog.result(), dialog.line_edit_login.text(), dialog.line_edit_password.text()
        if result == 1:
            if login == 'admin' and password == 'admin':
                self.user = login
                self.set_gui_enter_offline()
                self.set_gui_enter_exit_online(True)
            else:
                self.user_log_in(wrong_login_pass=True)
        elif result == 0:
            self.set_gui_enter_offline()
        elif result == 2:
            print('Регистрация')

    def user_log_out(self):
        if self.playbook:
            dialog_save_current_playbook = QMessageBox(QMessageBox.Question, '', 'Сохранить текущий плейбук на сервере?', parent=self)
            dialog_save_current_playbook.addButton("Да", QMessageBox.AcceptRole)  # результат устанавливается в 0
            dialog_save_current_playbook.addButton("Нет", QMessageBox.RejectRole)  # результат устанавливается в 1
            dialog_save_current_playbook.exec()
            if not dialog_save_current_playbook.result():
                print('Сохранение')
        self.user = None
        self.set_gui_enter_exit_online(False)

    def set_gui_enter_offline(self):
        self.action_user_login.setEnabled(True)
        self.action_new_playbook.setEnabled(True)
        self.action_open_playbook_offline.setEnabled(True)

    def set_gui_enter_exit_online(self, condition: bool):
        self.action_user_login.setEnabled(not condition)
        self.action_user_logout.setEnabled(condition)
        self.action_open_playbook_online.setEnabled(condition)
        if self.playbook:
            self.action_save_playbook_online.setEnabled(condition)
        self.setWindowTitle(f'PlayCreator - {self.user}') if condition else self.setWindowTitle('PlayCreator')

    def sign_up(self):
        dialog = DialogSignUp(self.dialog_windows_text_color, parent=self)
        dialog.exec()

    def create_new_playbook(self):
        def new_playbook_dialog():
            dialog = DialogNewPlaybook(self.dialog_windows_text_color, parent=self)
            result, playbook_name = dialog.exec(), dialog.line_edit.text().strip()
            if result == 1 and len(playbook_name) > 0:
                if dialog.radio_button_football.isChecked():
                    self.playbook = Playbook(playbook_name, PlaybookType.football)
                elif dialog.radio_button_flag.isChecked():
                    self.playbook = Playbook(playbook_name, PlaybookType.flag)
                self.set_gui_for_playbook()
                self.label_playbook_name.setText(playbook_name)

        if self.playbook:
            question_dialog_new_playbook = QMessageBox(QMessageBox.Question, '', 'Создать новый плейбук?', parent=self)
            question_dialog_new_playbook.addButton("Да", QMessageBox.AcceptRole)  # результат устанавливается в 0
            question_dialog_new_playbook.addButton("Нет", QMessageBox.RejectRole)  # результат устанавливается в 1
            question_dialog_new_playbook.exec()
            if not question_dialog_new_playbook.result():
                question_dialog_save_current_playbook = QMessageBox(QMessageBox.Question, '', 'Сохранить текущий плейбук?', parent=self)
                question_dialog_save_current_playbook.addButton("Да", QMessageBox.AcceptRole)  # результат устанавливается в 0
                question_dialog_save_current_playbook.addButton("Нет", QMessageBox.RejectRole)  # результат устанавливается в 1
                question_dialog_save_current_playbook.exec()
                if not question_dialog_save_current_playbook.result():
                    print('Сохранение')
                if self.current_scene:
                    temp_scene = QGraphicsScene(parent=self)
                    self.graphics_view.setScene(temp_scene)
                    temp_scene.deleteLater()
                    del temp_scene
                    self.current_scene.deleteLater()
                    self.current_scene = None
                self.playbook = None
                self.chosen_list_item = None
                self.listWidget_schemes.clear()
                self.label_playbook_name.setText('')
                self.enable_disable_gui(False)
                new_playbook_dialog()
        else:
            new_playbook_dialog()

    def set_gui_for_playbook(self):
        self.action_save_playbook_offline.setEnabled(True)
        self.pushButton_add_scheme.setEnabled(True)
        self.pushButton_edit_playbook_name.setEnabled(True)
        if self.user:
            self.action_save_playbook_online.setEnabled(True)
        if self.playbook.type == PlaybookType.football:
            self.lineEdit_yards.setInputMask('999')
            self.lineEdit_yards.setMaxLength(3)
            self.lineEdit_yards.setText('50')
            self.label_place_players.setVisible(True)
            self.comboBox_team_type.setVisible(True)
        elif self.playbook.type == PlaybookType.flag:
            self.lineEdit_yards.setInputMask('99')
            self.lineEdit_yards.setMaxLength(2)
            self.lineEdit_yards.setText('25')
            self.label_place_players.setVisible(False)
            self.comboBox_team_type.setVisible(False)

    def enable_disable_gui(self, condition: bool):
        for mode in Modes:
            button = getattr(self, f'pushButton_{mode.name}')
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
        self.action_save_like_picture.setEnabled(condition)
        self.action_save_all_like_picture.setEnabled(condition)

        self.pushButton_edit_scheme.setEnabled(condition)
        self.pushButton_delete_scheme.setEnabled(condition)
        self.pushButton_scheme_move_up.setEnabled(condition)
        self.pushButton_scheme_move_down.setEnabled(condition)

        if not condition:
            self.comboBox_team_type.setEnabled(condition)
            self.lineEdit_yards.setEnabled(condition)
            self.pushButton_place_first_team.setEnabled(condition)
            self.pushButton_add_additional_off_player.setEnabled(condition)
            self.pushButton_add_additional_off_player.setVisible(condition)
            self.pushButton_del_additional_off_player.setEnabled(condition)
            self.pushButton_del_additional_off_player.setVisible(condition)
            self.pushButton_place_second_team.setEnabled(condition)
            self.comboBox_second_players_symbol.setVisible(condition)
            self.comboBox_second_players_symbol.setEnabled(condition)
            self.pushButton_delete_second_team.setEnabled(condition)
            self.pushButton_delete_all_players.setEnabled(condition)
            self.pushButton_delete_scheme.setEnabled(condition)
            self.pushButton_scheme_move_up.setEnabled(condition)
            self.pushButton_scheme_move_down.setEnabled(condition)

    def set_gui_first_team_placed(self):
        self.pushButton_place_first_team.setEnabled(False)
        self.pushButton_place_second_team.setEnabled(True)
        self.lineEdit_yards.setEnabled(False)
        self.comboBox_team_type.setEnabled(False)
        self.pushButton_delete_all_players.setEnabled(True)
        if (self.playbook.type == PlaybookType.football and self.comboBox_team_type.currentIndex() == 0) or self.playbook.type == PlaybookType.flag:
            self.pushButton_add_additional_off_player.setVisible(True)
            self.pushButton_add_additional_off_player.setEnabled(True)
            self.pushButton_del_additional_off_player.setVisible(True)
            self.pushButton_del_additional_off_player.setEnabled(False)

    def set_gui_for_second_team(self, condition: bool):
        self.pushButton_place_second_team.setEnabled(not condition)
        self.pushButton_delete_second_team.setEnabled(condition)
        self.comboBox_second_players_symbol.setEnabled(condition)
        self.comboBox_second_players_symbol.setVisible(condition)

    def set_gui_for_additional_offence_player(self, condition: bool):
        self.pushButton_add_additional_off_player.setEnabled(not condition)
        self.pushButton_del_additional_off_player.setEnabled(condition)

    def set_gui_all_teams_deleted(self):
        if self.playbook.type == PlaybookType.football:
            self.comboBox_team_type.setEnabled(True)
        self.lineEdit_yards.setEnabled(True)
        # if self.comboBox_team_type_football.currentIndex() == 1:
        #     self.lineEdit_yards_football.setEnabled(False)
        # else:
        #     self.lineEdit_yards_football.setEnabled(True)
        self.pushButton_place_first_team.setEnabled(True)
        self.pushButton_add_additional_off_player.setEnabled(False)
        self.pushButton_add_additional_off_player.setVisible(False)
        self.pushButton_del_additional_off_player.setEnabled(False)
        self.pushButton_del_additional_off_player.setVisible(False)
        self.pushButton_place_second_team.setEnabled(False)
        self.pushButton_delete_second_team.setEnabled(False)
        self.pushButton_delete_all_players.setEnabled(False)
        self.comboBox_second_players_symbol.setEnabled(False)
        self.comboBox_second_players_symbol.setVisible(False)

    def set_gui_for_current_scene_football(self):
        self.fontComboBox.setCurrentFont(self.current_scene.config['font_type'])
        self.comboBox_font_size.setCurrentText(str(self.current_scene.config['font_size']))
        self.pushButton_bold.setChecked(self.current_scene.config['bold'])
        self.pushButton_italic.setChecked(self.current_scene.config['italic'])
        self.pushButton_underline.setChecked(self.current_scene.config['underline'])
        self.comboBox_line_thickness.setCurrentText(str(self.current_scene.config['line_thickness']))
        self.pushButton_current_color.setStyleSheet(f'background-color: {self.current_scene.config["color"]};')
        getattr(self, f'pushButton_{self.current_scene.mode.name}').setChecked(True)

        if self.current_scene.first_team_placed:
            self.comboBox_team_type.setEnabled(False)
            self.lineEdit_yards.setText(str(self.current_scene.first_team_position))
            self.lineEdit_yards.setEnabled(False)
            self.pushButton_place_first_team.setEnabled(False)
            self.pushButton_delete_all_players.setEnabled(True)
            if self.current_scene.first_team_placed == TeamType.offence:
                self.comboBox_team_type.setCurrentIndex(0)
                self.pushButton_add_additional_off_player.setVisible(True)
                self.pushButton_del_additional_off_player.setVisible(True)
                condition = True if self.current_scene.additional_offence_player else False
                self.set_gui_for_additional_offence_player(condition)
            elif self.current_scene.first_team_placed == TeamType.kickoff:
                self.pushButton_add_additional_off_player.setVisible(False)
                self.pushButton_del_additional_off_player.setVisible(False)
                self.comboBox_team_type.setCurrentIndex(1)
            elif self.current_scene.first_team_placed == TeamType.punt_kick:
                self.pushButton_add_additional_off_player.setVisible(False)
                self.pushButton_del_additional_off_player.setVisible(False)
                self.comboBox_team_type.setCurrentIndex(2)
            elif self.current_scene.first_team_placed == TeamType.field_goal_off:
                self.pushButton_add_additional_off_player.setVisible(False)
                self.pushButton_del_additional_off_player.setVisible(False)
                self.comboBox_team_type.setCurrentIndex(3)
            condition = True if self.current_scene.second_team_placed else False
            self.set_gui_for_second_team(condition)
        else:
            self.set_gui_all_teams_deleted()

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

    def get_top_bot_points_for_items_on_scene(self, scene: Field) -> tuple[None, None] | tuple[float, float]:###### Проверить ещё раз условие для низа итема
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
            if figure.y() < top_y:
                top_y = figure.y()
            if figure.y() + figure.height() > bot_y:
                bot_y = figure.y() + figure.height()

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
        self.pushButton_delete_actions.clicked.connect(self.delete_all_players_actions)
        self.pushButton_delete_figures.clicked.connect(self.current_scene.delete_figures)
        self.pushButton_delete_labels.clicked.connect(self.current_scene.delete_labels)
        self.pushButton_delete_pencil.clicked.connect(self.current_scene.delete_pencil)
        self.current_scene.modeChanged.connect(lambda mode: getattr(self, f'pushButton_{mode.name}').setChecked(True))
        self.current_scene.labelDoubleClicked.connect(self.update_window_font_config)
        self.current_scene.labelEditingFinished.connect(self.label_editing_finished)

    # def create_new_playbook(self):

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
            painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.VerticalSubpixelPositioning | QPainter.LosslessImageRendering)
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

    def delete_all_players_actions(self):
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

    # ТУТ БЫЛ МЕТОД enable_disable_gui

    '''-----------------------------------------------------------------------------------------------------------------
    ----------------------------------------------Методы футбольного поля-----------------------------------------------
    -----------------------------------------------------------------------------------------------------------------'''
    def add_new_scheme(self):
        if self.listWidget_schemes.count() == 0:
            self.enable_disable_gui(True)
        item = CustomListItem(Field(self, self.field_data, self.playbook.type, parent=self.graphics_view), '')
        self.playbook.add_scheme(item)
        self.listWidget_schemes.addItem(item)
        self.listWidget_schemes.setCurrentItem(item)
        self.edit_current_scheme()
        self.choose_current_scheme()
        self.connect_signals_to_current_scene()

    def delete_current_scheme(self):
        item = self.listWidget_schemes.takeItem(self.listWidget_schemes.currentRow())
        if self.listWidget_schemes.count() > 0:
            if item is self.chosen_list_item:
            # if item is self.listWidget_schemes_football.selectedItems()[0]:
                self.chosen_list_item = None
            self.choose_current_scheme()
        else:
            if self.current_scene:
                self.current_scene.deleteLater()
                self.current_scene = None
            self.chosen_list_item = None
            # self.set_gui_for_current_scene_football()
            self.enable_disable_gui(False)
        self.playbook.remove_scheme(item)
        del item

    def edit_current_scheme(self):
        item = self.listWidget_schemes.currentItem()
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
        self.listWidget_schemes.editItem(item)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    def edit_playbook_name(self):
        dialog = QInputDialog(parent=self)
        dialog.setOkButtonText('ОК')
        dialog.setCancelButtonText('Отмена')
        text, result = dialog.getText(self, 'Изменение названия плейбука', 'Название плейбука: ', QLineEdit.Normal, self.playbook.name)
        if result:
            self.playbook.name = text.strip()
            self.label_playbook_name.setText(text.strip())

    def choose_current_scheme(self):
        if self.listWidget_schemes.count() != 0:
            if self.current_scene:  # Запоминание точки обзора текущей сцены и зума, при смене на другую сцену
                self.current_scene.view_point = self.graphics_view.mapToScene(QPoint(self.graphics_view.width() // 2, self.graphics_view.height() // 2))
                self.current_scene.zoom = self.graphics_view.current_zoom
            for item_number in range(self.listWidget_schemes.count()):
                item = self.listWidget_schemes.item(item_number)
                if self.current_theme == AppTheme.dark:
                    item.setForeground(QColor('#b1b1b1'))
                elif self.current_theme == AppTheme.light:
                    item.setForeground(QColor(Qt.black))
            self.chosen_list_item = self.listWidget_schemes.currentItem()
            if self.current_theme == AppTheme.dark:
                self.chosen_list_item.setForeground(QColor('#27c727'))
            elif self.current_theme == AppTheme.light:
                self.chosen_list_item.setForeground(QColor('#1a6aa7'))
            self.chosen_list_item.setSelected(True)
            self.current_scene = self.chosen_list_item.scene
            self.graphics_view.setScene(self.current_scene)
            self.graphics_view.set_current_zoom(self.current_scene.zoom)
            self.graphics_view.centerOn(self.current_scene.view_point)
            self.set_gui_for_current_scene_football()

    def move_up_current_scheme(self):
        row = self.listWidget_schemes.currentRow()
        if row > 0:
            item = self.listWidget_schemes.takeItem(row)
            row -= 1
            self.listWidget_schemes.insertItem(row, item)
            self.listWidget_schemes.setCurrentItem(item)

    def move_down_current_scheme(self):
        row = self.listWidget_schemes.currentRow()
        if row < self.listWidget_schemes.count():
            item = self.listWidget_schemes.takeItem(row)
            row += 1
            self.listWidget_schemes.insertItem(row, item)
            self.listWidget_schemes.setCurrentItem(item)

    # def team_type_changed_football(self):
    #     if self.comboBox_team_type_football.currentIndex() == 1:
    #         self.lineEdit_yards_football.setEnabled(False)
    #         self.lineEdit_yards_football.setText(str(65))
    #     else:
    #         self.lineEdit_yards_football.setEnabled(True)

    def get_yards_to_end_zone_football(self):
        yards = self.field_data.football_ten_yard + self.field_data.football_one_yard * int(self.lineEdit_yards.text())
        return yards

    def check_max_yards_football(self, value: str):
        try:
            if int(value) > 100:
                self.lineEdit_yards.setText('100')
        except ValueError:
            pass

    def validate_yards_football(self, value: str):
        if not value.isdigit():  # Защита от пустого поля ввода ярдов
            value = '50'
            self.lineEdit_yards.setText('50')
        self.check_max_yards_football(value)
        if self.comboBox_team_type.currentIndex() == 1:  # Кикофф пробивается либо с 75 ярдов, либо с 65
            if int(value) >= 70:
                self.lineEdit_yards.setText('75')
            else:
                self.lineEdit_yards.setText('65')
        elif self.comboBox_team_type.currentIndex() == 2:  # Пант нет смысла пробивать если до зачётной зоны меньше 20 ярдов
            if int(value) <= 20:
                self.lineEdit_yards.setText('20')
        elif self.comboBox_team_type.currentIndex() == 3:
            pass

    def place_first_team_football(self):
        self.validate_yards_football(self.lineEdit_yards.text())
        if not self.current_scene.first_team_placed:
            if self.comboBox_team_type.currentIndex() == 0:
                self.create_first_team_players_football(self.players_data.offence_football)
                self.current_scene.first_team_placed = TeamType.offence
                self.current_scene.first_team_position = int(self.lineEdit_yards.text())
                self.set_gui_first_team_placed()
            elif self.comboBox_team_type.currentIndex() == 1:
                self.create_first_team_players_football(self.players_data.kickoff_football)
                self.current_scene.first_team_placed = TeamType.kickoff
                self.current_scene.first_team_position = int(self.lineEdit_yards.text())
                self.set_gui_first_team_placed()
            elif self.comboBox_team_type.currentIndex() == 2:
                # if int(self.lineEdit_yards_football.text()) >= 20:
                self.create_first_team_players_football(self.players_data.punt_football)
                self.current_scene.first_team_placed = TeamType.punt_kick
                self.current_scene.first_team_position = int(self.lineEdit_yards.text())
                self.set_gui_first_team_placed()
                # else:
                #     self.lineEdit_yards_football.setText('20')
            elif self.comboBox_team_type.currentIndex() == 3:
                # if int(self.lineEdit_yards_football.text()) <= 70:
                self.create_first_team_players_football(self.players_data.field_goal_off_football)
                self.current_scene.first_team_placed = TeamType.field_goal_off
                self.current_scene.first_team_position = int(self.lineEdit_yards.text())
                self.set_gui_first_team_placed()
                # else:
                #     self.lineEdit_yards_football.setText('70')

    def create_first_team_players_football(self, players: tuple | list):
        for i, player in enumerate(players):
            team, position, text_color, fill_color, fill_type, x, y = player
            if i == 10 and team == TeamType.punt_kick and int(self.lineEdit_yards.text()) >= 95:
                item = FirstTeamPlayer(team, position, text_color, fill_color, fill_type, x,
                                       119 * self.current_scene.field_data.football_one_yard - self.players_data.player_size / 2)
            else:
                item = FirstTeamPlayer(team, position, text_color, fill_color, fill_type, x,
                                       y + self.get_yards_to_end_zone_football())
            self.current_scene.addItem(item)
            self.current_scene.first_team_players.append(item)

    def place_second_team_football(self):
        if not self.current_scene.second_team_placed:
            if self.current_scene.first_team_placed == TeamType.offence:
                self.create_second_team_football(self.players_data.defence_football)
                self.current_scene.second_team_placed = TeamType.defence
            elif self.current_scene.first_team_placed == TeamType.kickoff:
                self.create_second_team_football(self.players_data.kickoff_return)
                self.current_scene.second_team_placed = TeamType.kick_ret
            elif self.current_scene.first_team_placed == TeamType.punt_kick:
                self.create_second_team_football(self.players_data.punt_return)
                self.current_scene.second_team_placed = TeamType.punt_ret
            elif self.current_scene.first_team_placed == TeamType.field_goal_off:
                self.create_second_team_football(self.players_data.field_goal_def)
                self.current_scene.second_team_placed = TeamType.field_goal_def
            self.set_gui_for_second_team(True)

    def create_second_team_football(self, players: tuple | list):
        for i, player in enumerate(players):
            team, position, text_color, border_color, symbol, x, y = player
            if (team == TeamType.punt_ret and i == 10) or (team == TeamType.kick_ret and i == 10):  # punt_returner and kick_returner
                item = SecondTeamPlayer(team, position, text_color, border_color, symbol, x, y)
            elif team == TeamType.field_goal_def and i == 10 and int(self.lineEdit_yards.text()) > 20:  # kick returner
                item = SecondTeamPlayer(team, position, text_color, border_color, symbol, x,
                                        self.current_scene.field_data.football_five_yard)
            elif team == TeamType.defence and i == 10 and int(self.lineEdit_yards.text()) < 3:  # free safety
                item = SecondTeamPlayer(team, position, text_color, border_color, symbol, x,
                                        y + self.get_yards_to_end_zone_football() + 3 * self.current_scene.field_data.football_one_yard)
            elif team == TeamType.kick_ret and 4 < i <= 7 and int(self.lineEdit_yards.text()) == 75:  # second line
                item = SecondTeamPlayer(team, position, text_color, border_color, symbol, x,
                                        y + self.get_yards_to_end_zone_football() - self.field_data.football_five_yard)
            elif team == TeamType.kick_ret and 7 < i <= 9 and int(self.lineEdit_yards.text()) == 75:  # third line
                item = SecondTeamPlayer(team, position, text_color, border_color, symbol, x,
                                        y + self.get_yards_to_end_zone_football() - self.field_data.football_ten_yard)
            else:  # other players
                item = SecondTeamPlayer(team, position, text_color, border_color, symbol, x,
                                        y + self.get_yards_to_end_zone_football())
            self.current_scene.addItem(item)
            self.current_scene.second_team_players.append(item)

    def place_additional_offence_player_football(self):
        if self.current_scene.first_team_placed == TeamType.offence and not self.current_scene.additional_offence_player:
            team, position, text_color, fill_color, fill_type, x, y = self.players_data.additional_player_football
            self.current_scene.additional_offence_player = FirstTeamPlayer(team, position, text_color, fill_color, fill_type, x,
                                                                           y + self.get_yards_to_end_zone_football())
            self.current_scene.addItem(self.current_scene.additional_offence_player)
            self.set_gui_for_additional_offence_player(True)

    def delete_second_team(self):
        if self.current_scene.second_team_placed:
            self.delete_second_team_actions()
            group = self.current_scene.createItemGroup(self.current_scene.second_team_players)
            self.current_scene.removeItem(group)
            self.current_scene.second_team_players.clear()
            self.current_scene.second_team_placed = None
            self.set_gui_for_second_team(False)
            if self.current_scene.allow_painting and \
                    (self.current_scene.current_player.team == TeamType.defence  # Используется для команды защиты в футболе и во флаге
                     or self.current_scene.current_player.team == TeamType.punt_ret
                     or self.current_scene.current_player.team == TeamType.kick_ret
                     or self.current_scene.current_player.team == TeamType.field_goal_def):
                self.delete_drawing_actions()
            self.current_scene.update()

    def delete_additional_offence_player(self):
        if self.current_scene.additional_offence_player:
            self.current_scene.additional_offence_player.delete_actions()
            self.current_scene.removeItem(self.current_scene.additional_offence_player)
            self.current_scene.additional_offence_player = None
            self.set_gui_for_additional_offence_player(False)
            if self.current_scene.allow_painting and self.current_scene.current_player.team == TeamType.offence_add:
                self.delete_drawing_actions()
            self.current_scene.update()

    def clear_scene(self):
        if self.current_scene.first_team_placed:
            self.delete_first_team_actions()
            group = self.current_scene.createItemGroup(self.current_scene.first_team_players)
            self.current_scene.removeItem(group)
            self.current_scene.first_team_players.clear()
            self.current_scene.first_team_placed = None
            self.current_scene.first_team_position = None
            self.delete_additional_offence_player()
        self.delete_second_team()
        self.current_scene.delete_figures()
        self.current_scene.delete_labels()
        self.current_scene.delete_pencil()
        self.set_gui_all_teams_deleted()
        if self.current_scene.allow_painting:
            self.delete_drawing_actions()
        self.current_scene.update()

    def second_team_symbol_changed(self):
        if self.comboBox_second_players_symbol.currentIndex() == 0:
            for player in self.current_scene.second_team_players:
                # player.set_symbol('letters')
                player.symbol = SymbolType.letter
                player.text_color = '#000000'
                player.border_color = '#000000'
        elif self.comboBox_second_players_symbol.currentIndex() == 1:
            for player in self.current_scene.second_team_players:
                # player.set_symbol('x')
                player.symbol = SymbolType.cross
                player.text_color = '#000000'
                player.border_color = '#000000'
        elif self.comboBox_second_players_symbol.currentIndex() == 2:
            for player in self.current_scene.second_team_players:
                # player.set_symbol('triangle_bot')
                player.symbol = SymbolType.triangle_bot
                player.text_color = '#000000'
                player.border_color = '#000000'
        elif self.comboBox_second_players_symbol.currentIndex() == 3:
            for player in self.current_scene.second_team_players:
                # player.set_symbol('triangle_top')
                player.symbol = SymbolType.triangle_top
                player.text_color = '#000000'
                player.border_color = '#000000'

    # ТУТ БЫЛИ МЕТОДЫ SET_GUI ДЛЯ ФУТБОЛА

    '''-----------------------------------------------------------------------------------------------------------------
    ---------------------------------------------Методы флаг-футбольного поля-------------------------------------------
    -----------------------------------------------------------------------------------------------------------------'''
    def get_yards_to_end_zone_flag(self):
        yards = self.field_data.flag_ten_yard + self.field_data.flag_one_yard * int(self.lineEdit_yards.text())
        return yards

    def check_max_yards_flag(self, value: str):
        try:
            if int(value) > 50:
                self.lineEdit_yards.setText('50')
        except ValueError:
            pass

    def validate_yards_flag(self, value: str):
        if not value.isdigit():
            self.lineEdit_yards.setText('25')

    def place_first_team_flag(self):
        self.validate_yards_flag(self.lineEdit_yards.text())
        if not self.current_scene.first_team_placed:
            self.create_players_flag(self.players_data.offence_flag)
            self.current_scene.first_team_placed = TeamType.offence
            self.current_scene.first_team_position = int(self.lineEdit_yards.text())
            self. set_gui_first_team_placed()

    def place_second_team_flag(self):
        if not self.current_scene.second_team_placed:
            self.create_players_flag(self.players_data.defence_flag)
            self.current_scene.second_team_placed = True
            self.set_gui_for_second_team(True)

    def create_players_flag(self, players: tuple | list):
        for i, player in enumerate(players):
            team, position, text_color, fill_color, fill_type, x, y = player
            if team == TeamType.offence:
                item = FirstTeamPlayer(team, position, text_color, fill_color, fill_type, x,
                                       y + self.get_yards_to_end_zone_flag())
                self.current_scene.first_team_players.append(item)
            else:
                item = SecondTeamPlayer(team, position, text_color, fill_color, fill_type, x,
                                        y + self.get_yards_to_end_zone_flag())
                self.current_scene.second_team_players.append(item)
            self.current_scene.addItem(item)

    def place_additional_offence_player_flag(self):
        if self.current_scene.first_team_placed == TeamType.offence and not self.current_scene.additional_offence_player:
            team, position, text_color, fill_color, fill_type, x, y = self.players_data.additional_player_flag
            self.current_scene.additional_offence_player = FirstTeamPlayer(team, position, text_color, fill_color, fill_type, x,
                                                                           y + self.get_yards_to_end_zone_flag())
            self.current_scene.addItem(self.current_scene.additional_offence_player)
            self.set_gui_for_additional_offence_player(True)

    '''-----------------------------------------------------------------------------------------------------------------
    ------------------------------------Методы интерфейса напрямую не касающиеся полей----------------------------------
    -----------------------------------------------------------------------------------------------------------------'''
    def set_color(self, color: str):
        self.pushButton_current_color.setStyleSheet(f'background-color: {color};')
        self.colorChanged.emit(color)

    def set_user_color(self):
        user_color_dialog = QColorDialog(parent=self)
        if user_color_dialog.exec():
            self.set_color(user_color_dialog.selectedColor().name())

    def label_set_current_zoom(self, value: int):
        self.label_current_zoom.setText(f'Приближение: {value}%')
        if self.current_scene:
            self.current_scene.zoom = value

    def set_dark_theme(self):
        self.current_theme = AppTheme.dark
        self.change_style('Interface/tactic(dark128).png', '#27c727')
        self.setStyleSheet(open('Interface/Dark_theme/PlayCreator_dark_theme.css').read())
        # self.setStyleSheet('')
        for item_number in range(self.listWidget_schemes.count()):
            item = self.listWidget_schemes.item(item_number)
            item.setForeground(QColor('#b1b1b1'))
        if self.chosen_list_item:
            self.chosen_list_item.setForeground(QColor('#27c727'))
        icon = QIcon()
        icon.addPixmap(QPixmap('Interface/Dark_theme/save(dark_theme).png'))
        self.action_save_like_picture.setIcon(icon)
        icon = QIcon()
        icon.addPixmap(QPixmap('Interface/Dark_theme/save_all(dark_theme).png'))
        self.action_save_all_like_picture.setIcon(icon)
        icon = QIcon()
        icon.addPixmap(QPixmap('Interface/Dark_theme/new_scheme(dark_theme).png'))
        self.action_new_playbook.setIcon(icon)
        icon = QIcon()
        icon.addPixmap(QPixmap('Interface/Dark_theme/presentation_mode(dark_theme).png'))
        self.action_presentation_mode.setIcon(icon)

    def set_light_theme(self):
        self.current_theme = AppTheme.light
        self.change_style('Interface/tactic(light128).png', '#1a6aa7')
        self.setStyleSheet(open('Interface/Light_theme/PlayCreator_light_theme.css').read())
        # self.setStyleSheet('')
        for item_number in range(self.listWidget_schemes.count()):
            item = self.listWidget_schemes.item(item_number)
            item.setForeground(QColor(Qt.black))
        if self.chosen_list_item:
            self.chosen_list_item.setForeground(QColor('#1a6aa7'))
        icon = QIcon()
        icon.addPixmap(QPixmap('Interface/Light_theme/save(light_theme).png'))
        self.action_save_like_picture.setIcon(icon)
        icon = QIcon()
        icon.addPixmap(QPixmap('Interface/Light_theme/save_all(light_theme).png'))
        self.action_save_all_like_picture.setIcon(icon)
        icon = QIcon()
        icon.addPixmap(QPixmap('Interface/Light_theme/new_scheme(light_theme).png'))
        self.action_new_playbook.setIcon(icon)
        icon = QIcon()
        icon.addPixmap(QPixmap('Interface/Light_theme/presentation_mode(light_theme).png'))
        self.action_presentation_mode.setIcon(icon)

    def change_style(self, ico: str, color: str):
        self.ico_about_path = ico
        self.dialog_windows_text_color = color

    def about_clicked(self):
        dialog = DialogAbout(self.version, self.ico_about_path, self.dialog_windows_text_color, parent=self)
        dialog.exec()

    def presentation_mode(self):
        self.groupBox_team_playbook_settings.setVisible(not self.action_presentation_mode.isChecked())
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    play_creator = PlayCreator()
    play_creator.show()

    sys.exit(app.exec())
