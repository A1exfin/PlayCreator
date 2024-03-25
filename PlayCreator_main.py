import sys
import os
from typing import TYPE_CHECKING, Union
from datetime import datetime
from time import sleep
from PySide6.QtWidgets import QApplication, QSplashScreen, QMainWindow, QGraphicsScene, QButtonGroup, QLineEdit, \
    QFileDialog, QInputDialog, QColorDialog, QMessageBox, QFrame
from PySide6.QtGui import QActionGroup, QImage, QColor, QPainter, QFont, QPixmap, QIcon
from PySide6.QtCore import Qt, Signal, QDir, QRectF, QRect, QFile, QTextStream
from PlayCreator_ui import Ui_MainWindow
from Enums import AppTheme, PlaybookType, Modes, TeamType, SymbolType
from Dialog_windows import DialogSignUp, DialogLogIn, DialogAbout, DialogNewPlaybook, DialogOpenPlaybook
from Playbook_scheme import Playbook, Scheme
from Graphics import CustomGraphicsView, FirstTeamPlayer, SecondTeamPlayer, ActionLine, FinalActionArrow, FinalActionLine, \
    Rectangle, Ellipse, PencilLine, ProxyWidgetLabel
from DB_offline.queryes import create_db_if_not_exists, get_user_settings, get_playbook_info, select_playbook, save_playbook, save_user_settings, \
    save_new_playbook, drop_tables

if TYPE_CHECKING:
    from DB_offline.models import UserSettingsORM
    from Graphics import Field


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

    def __init__(self, settings_orm: 'UserSettingsORM'):
        super().__init__()
        self.setupUi(self)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.settings_orm = settings_orm
        self.playbook_orm = None
        self.user = None
        self.current_theme = None
        self.about_ico_path = None

        self.playbook: Union['Playbook', None] = None
        self.chosen_scheme: Union['Scheme', None] = None
        self.current_scene: Union['Field', None] = None

        self.graphics_view = CustomGraphicsView(parent=self.centralwidget)
        self.gridLayout_2.addWidget(self.graphics_view, 0, 0, 2, 1)
        self.label_set_current_zoom(self.graphics_view.current_zoom)

        action_theme_group = QActionGroup(self)
        action_theme_group.addAction(self.action_dark_theme)
        action_theme_group.addAction(self.action_light_theme)
        action_theme_group.setExclusive(True)

        getattr(self, f'action_{self.settings_orm.theme.name}_theme').setChecked(True)
        getattr(self, f'set_{self.settings_orm.theme.name}_theme')()
        self.showMaximized() if self.settings_orm.maximized else self.showNormal()
        self.addToolBar(self.settings_orm.toolbar_area, self.toolBar_main)
        self.toolBar_main.show() if self.settings_orm.toolbar_condition else self.toolBar_main.hide()
        self.action_toolbar_condition.setChecked(self.settings_orm.toolbar_condition)

        mode_group = QButtonGroup(parent=self)
        mode_group.setExclusive(True)
        for mode in Modes:
            button = getattr(self, f'pushButton_{mode.name}')
            button.pressed.connect(lambda mode=mode: self.current_scene.set_mode(mode) if self.current_scene else ...)
            mode_group.addButton(button)
        for i, color in enumerate(COLORS):
            button = getattr(self, f'pushButton_color_{i}')
            button.setStyleSheet(f'background-color: {color};')
            button.pressed.connect(lambda color=color: self.set_color(color))

        self.graphics_view.zoomChanged.connect(self.label_set_current_zoom)

        self.lineEdit_yards.textChanged.connect(lambda text: getattr(self, f'check_max_yards_{self.playbook.type.name}')(text))

        self.pushButton_place_first_team.clicked.connect(lambda: getattr(self, f'place_first_team_{self.playbook.type.name}')(self.current_scene) if self.current_scene else ...)
        self.pushButton_add_additional_off_player.clicked.connect(lambda: self.place_additional_offence_player(self.current_scene) if self.current_scene else ...)
        self.pushButton_place_second_team.clicked.connect(lambda: getattr(self, f'place_second_team_{self.playbook.type.name}')(self.current_scene) if self.current_scene else ...)
        self.pushButton_del_additional_off_player.clicked.connect(lambda: self.delete_additional_offence_player(self.current_scene) if self.current_scene else ...)
        self.pushButton_delete_second_team.clicked.connect(lambda: self.delete_second_team(self.current_scene) if self.current_scene else ...)
        self.pushButton_delete_all_players.clicked.connect(lambda: self.delete_all_players(self.current_scene) if self.current_scene else ...)
        self.comboBox_second_players_symbol.currentIndexChanged.connect(lambda: self.second_team_symbol_changed(self.current_scene) if self.current_scene else ...)

        self.pushButton_delete_actions.clicked.connect(lambda: self.current_scene.delete_all_players_actions() if self.current_scene else ...)
        self.pushButton_delete_figures.clicked.connect(lambda: self.current_scene.delete_figures() if self.current_scene else ...)
        self.pushButton_delete_labels.clicked.connect(lambda: self.current_scene.delete_labels() if self.current_scene else ...)
        self.pushButton_delete_pencil.clicked.connect(lambda: self.current_scene.delete_pencil() if self.current_scene else ...)

        self.comboBox_line_thickness.currentTextChanged.connect(lambda thickness: self.current_scene.set_config('line_thickness', int(thickness)) if self.current_scene else ...)
        self.fontComboBox.currentFontChanged.connect(lambda font: self.combobox_font_changed(self.current_scene, font) if self.current_scene else ...)
        self.comboBox_font_size.currentTextChanged.connect(lambda font_size: self.font_size_changed(self.current_scene, font_size) if self.current_scene else ...)
        self.pushButton_bold.toggled.connect(lambda bold_condition: self.bold_changed(self.current_scene, bold_condition) if self.current_scene else ...)
        self.pushButton_italic.toggled.connect(lambda italic_condition: self.italic_changed(self.current_scene, italic_condition) if self.current_scene else ...)
        self.pushButton_underline.toggled.connect(lambda underline_condition: self.underline_changed(self.current_scene, underline_condition) if self.current_scene else ...)
        self.colorChanged.connect(lambda color: self.color_changed(self.current_scene, color) if self.current_scene else ...)
        self.pushButton_current_color.clicked.connect(self.set_user_color)

        self.action_user_login.triggered.connect(self.user_log_in)
        self.action_user_logout.triggered.connect(self.user_log_out)

        self.action_close_programm.triggered.connect(lambda: self.close())
        self.action_dark_theme.toggled.connect(self.set_dark_theme)
        self.action_light_theme.toggled.connect(self.set_light_theme)
        self.action_toolbar_condition.toggled.connect(lambda: self.toolBar_main.hide() if not self.action_toolbar_condition.isChecked() else self.toolBar_main.show())
        self.action_about.triggered.connect(self.about_clicked)
        self.action_presentation_mode.toggled.connect(self.presentation_mode)
        self.action_new_playbook.triggered.connect(self.new_playbook)
        self.action_open_playbook_offline.triggered.connect(self.open_playbook_offline)
        self.action_save_playbook_offline.triggered.connect(self.save_current_playbook_offline)
        self.action_save_playbook_offline_as.triggered.connect(self.save_current_playbook_offline_as)
        self.action_save_like_picture.triggered.connect(lambda: self.save_current_scheme_on_picture(self.current_scene) if self.current_scene else ...)
        self.action_save_all_like_picture.triggered.connect(self.save_all_schemes_on_picture)

        self.pushButton_add_scheme.clicked.connect(self.add_new_scheme)
        self.pushButton_delete_scheme.clicked.connect(self.delete_current_scheme)
        self.pushButton_scheme_move_up.clicked.connect(self.move_up_current_scheme)
        self.pushButton_scheme_move_down.clicked.connect(self.move_down_current_scheme)
        self.pushButton_edit_scheme.clicked.connect(self.edit_current_scheme)
        self.pushButton_edit_playbook_name.clicked.connect(self.edit_playbook_name)
        self.listWidget_schemes.itemDoubleClicked.connect(self.choose_current_scheme)
        # self.listWidget_schemes.itemClicked.connect(lambda : print(self.listWidget_schemes.currentItem()))  # для отладки

        # self.test_func.clicked.connect(self.set_dark_theme)  ############################## тестовая функция для отладки
        # self.test_func.clicked.connect(self.set_light_theme)  ############################## тестовая функция для отладки
        # self.test_func.clicked.connect(self.test_fn)  ############################## тестовая функция
        self.test_func.setEnabled(False)
        self.test_func.setVisible(False)

        # self.user_log_in()    ##########################  Установить неактивным создание нового плейбука
        # self.sign_up()

        # dialog = DialogFigureSettings(self.dialog_windows_text_color, Modes.ellipse, True, '#ff0000', 2, True, '#333333', '#22', parent=self)
        # result = dialog.exec()
        # dialog = DialogFirstTeamPlayerSettings(self.dialog_windows_text_color, 'C', 'QW', '#ff0000', '#0000ff', 'right', parent=self)
        # result = dialog.exec()
        # dialog = DialogSecondTeamPlayerSettings(self.dialog_windows_text_color, 'W', '#ff0000', '#0000ff', 'x', parent=self)
        # result = dialog.exec()
        # dialog = DialogOpenPlaybook(self.dialog_windows_text_color, get_playbook_info(), parent=self)
        # dialog.exec()

    '''-----------------------------------------------------------------------------------------------------------------
    ------------------------------------------------------Методы отладки------------------------------------------------
    -----------------------------------------------------------------------------------------------------------------'''

    def test_fn(self):
        ...
        # print(self)

        # print(self.playbook_orm)
        # print(self.playbook_orm.schemes)

        # print(self.playbook)

        # print(f'{self.playbook.schemes = }')
        # print(f'{len(self.playbook.schemes) = }')
        # print(f'{self.current_scene.first_team_placed = }')
        # print(f'{self.current_scene.second_team_placed = }')

        # print(f'{self.current_scene.first_team_players = }')
        # print(f'{len(self.current_scene.first_team_players) = }')
        # print(f'{self.current_scene.deleted_first_team_players = }')
        # print(f'{len(self.current_scene.deleted_first_team_players) = }')

        # print(f'{self.current_scene.additional_offence_player = }')
        # print(f'{self.current_scene.deleted_additional_offence_player = }')

        # print(f'{self.current_scene.second_team_players = }')
        # print(f'{len(self.current_scene.second_team_players) = }')
        # print(f'{self.current_scene.deleted_second_team_players = }')
        # print(f'{len(self.current_scene.deleted_second_team_players) = }')

        # print(f'{self.current_scene.rectangles = }')
        # print(f'{len(self.current_scene.rectangles) = }')
        # print(f'{self.current_scene.ellipses = }')
        # print(f'{len(self.current_scene.ellipses) = }')

        # print(f'{self.current_scene.labels = }')
        # print(f'{len(self.current_scene.labels) = }')
        # print(f'{self.current_scene.current_label = }')

        # print(f'{self.current_scene.pencil = }')
        # print(f'{len(self.current_scene.pencil) = }')

        # print(f'{self.current_scene.zoom = }')
        # print(f'{self.current_scene.view_point = }')
        # print(f'{self.current_scene.focusItem() = }')

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

    def set_gui_for_playbook(self):
        self.action_save_playbook_offline.setEnabled(True)
        self.action_save_playbook_offline_as.setEnabled(True)
        if self.user:
            self.action_save_playbook_online.setEnabled(True)
            # self.action_save_playbook_online_as.setEnabled(True)
        self.pushButton_add_scheme.setEnabled(True)
        self.pushButton_edit_playbook_name.setEnabled(True)
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
        self.action_save_playbook_offline.setEnabled(condition)
        self.action_save_playbook_offline_as.setEnabled(condition)
        if self.user:
            self.action_save_playbook_online.setEnabled(condition)
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
        self.pushButton_edit_playbook_name.setEnabled(condition)
        self.pushButton_edit_scheme.setEnabled(condition)
        self.pushButton_add_scheme.setEnabled(condition)
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
            # self.pushButton_edit_playbook_name.setEnabled(condition)
            # self.pushButton_add_scheme.setEnabled(condition)
            self.pushButton_delete_scheme.setEnabled(condition)
            self.pushButton_scheme_move_up.setEnabled(condition)
            self.pushButton_scheme_move_down.setEnabled(condition)

    def set_gui_first_team_placed(self):
        self.comboBox_team_type.setEnabled(False)
        self.lineEdit_yards.setEnabled(False)
        self.pushButton_place_first_team.setEnabled(False)
        self.pushButton_place_second_team.setEnabled(True)
        self.pushButton_delete_all_players.setEnabled(True)
        if (self.playbook.type == PlaybookType.football and self.comboBox_team_type.currentIndex() == 0) or self.playbook.type == PlaybookType.flag:
            self.pushButton_add_additional_off_player.setVisible(True)
            self.pushButton_del_additional_off_player.setVisible(True)
            self.pushButton_add_additional_off_player.setEnabled(True)
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
        self.pushButton_place_first_team.setEnabled(True)
        self.pushButton_add_additional_off_player.setVisible(False)
        self.pushButton_del_additional_off_player.setVisible(False)
        self.pushButton_add_additional_off_player.setEnabled(False)
        self.pushButton_del_additional_off_player.setEnabled(False)
        self.pushButton_place_second_team.setEnabled(False)
        self.pushButton_delete_second_team.setEnabled(False)
        self.pushButton_delete_all_players.setEnabled(False)
        self.comboBox_second_players_symbol.setEnabled(False)
        self.comboBox_second_players_symbol.setVisible(False)

    def set_gui_for_current_scene(self):
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
                self.set_gui_for_additional_offence_player(True if self.current_scene.additional_offence_player else False)
            elif self.current_scene.first_team_placed == TeamType.kickoff:
                self.comboBox_team_type.setCurrentIndex(1)
                self.pushButton_add_additional_off_player.setVisible(False)
                self.pushButton_del_additional_off_player.setVisible(False)
            elif self.current_scene.first_team_placed == TeamType.punt_kick:
                self.comboBox_team_type.setCurrentIndex(2)
                self.pushButton_add_additional_off_player.setVisible(False)
                self.pushButton_del_additional_off_player.setVisible(False)
            elif self.current_scene.first_team_placed == TeamType.field_goal_off:
                self.comboBox_team_type.setCurrentIndex(3)
                self.pushButton_add_additional_off_player.setVisible(False)
                self.pushButton_del_additional_off_player.setVisible(False)
            self.set_gui_for_second_team(True if self.current_scene.second_team_placed else False)
        else:
            self.set_gui_all_teams_deleted()

    def closeEvent(self, event):
        save_user_settings(self.settings_orm, self.return_data())

    def save_current_playbook_offline(self):
        if self.playbook_orm:
            save_playbook(self.playbook, self.playbook_orm)
        else:
            new_playbook_id = save_new_playbook(self.playbook)
            self.listWidget_schemes.clear()
            self.load_playbook(new_playbook_id)
            if len(self.playbook.schemes) > 0:
                self.enable_disable_gui(True)
                self.listWidget_schemes.setCurrentRow(0)
                self.choose_current_scheme()

    def save_current_playbook_offline_as(self):
        dialog_get_playbook_name = QInputDialog(parent=self)
        dialog_get_playbook_name.setOkButtonText('ОК')
        dialog_get_playbook_name.setCancelButtonText('Отмена')
        text, result = dialog_get_playbook_name.getText(self, 'Сохранить плейбук как...', 'Название плейбука: ', QLineEdit.Normal, self.playbook.name)
        if result:
            new_playbook_id = save_new_playbook(self.playbook, text.strip())
            self.listWidget_schemes.clear()
            self.load_playbook(new_playbook_id)
            if len(self.playbook.schemes) > 0:
                self.enable_disable_gui(True)
                self.listWidget_schemes.setCurrentRow(0)
                self.choose_current_scheme()

    def open_playbook_offline(self):
        def open_playbook_dialog():
            dialog = DialogOpenPlaybook(get_playbook_info(), parent=self)
            dialog.exec()
            if dialog.result():
                playbook_id = dialog.table_playbooks.item(dialog.table_playbooks.currentRow(), 0).text()
                self.load_playbook(int(playbook_id))
                if len(self.playbook.schemes) > 0:
                    self.enable_disable_gui(True)
                    self.listWidget_schemes.setCurrentRow(0)
                    self.choose_current_scheme()

        if self.playbook:
            if self.user:
                question_dialog_save_current_playbook_online = QMessageBox(QMessageBox.Question, 'Сохранение', 'Сохранить текущий плейбук на сервере?', parent=self)
                question_dialog_save_current_playbook_online.addButton("Да", QMessageBox.AcceptRole)  # результат устанавливается в 0
                question_dialog_save_current_playbook_online.addButton("Нет", QMessageBox.RejectRole)  # результат устанавливается в 1
                question_dialog_save_current_playbook_online.exec()
                if not question_dialog_save_current_playbook_online.result():
                    ...
                    # print('СОХРАНЕНИЕ НА СЕРВЕРЕ')
            question_dialog_save_current_playbook_offline = QMessageBox(QMessageBox.Question, 'Сохранение', 'Сохранить текущий плейбук на компьютере?', parent=self)
            question_dialog_save_current_playbook_offline.addButton("Да", QMessageBox.AcceptRole)  # результат устанавливается в 0
            question_dialog_save_current_playbook_offline.addButton("Нет", QMessageBox.RejectRole)  # результат устанавливается в 1
            question_dialog_save_current_playbook_offline.exec()
            if not question_dialog_save_current_playbook_offline.result():
                self.save_current_playbook_offline()
            if self.current_scene:
                temp_scene = QGraphicsScene(parent=self)
                self.graphics_view.setScene(temp_scene)
                temp_scene.deleteLater()
                del temp_scene
                self.current_scene.deleteLater()
                self.current_scene = None
            self.playbook = None
            self.chosen_scheme = None
            self.listWidget_schemes.clear()
            self.label_playbook_name.setText('')
            self.enable_disable_gui(False)
            open_playbook_dialog()
        else:
            open_playbook_dialog()

    def load_playbook(self, playbook_id: int):
        playbook_orm = select_playbook(playbook_id)
        self.playbook_orm = playbook_orm
        self.create_playbook(*playbook_orm.return_data())
        for scheme_orm in playbook_orm.schemes:
            _, *scheme_data = scheme_orm.return_data()
            scheme = self.create_scheme(*scheme_data)
            for rect_orm in scheme_orm.rectangles:
                rect = Rectangle(*rect_orm.return_data())
                scheme.scene.addItem(rect)
                scheme.scene.rectangles.append(rect)
            for ellipse_orm in scheme_orm.ellipses:
                ellipse = Ellipse(*ellipse_orm.return_data())
                scheme.scene.addItem(ellipse)
                scheme.scene.ellipses.append(ellipse)
            for label_orm in scheme_orm.labels:
                label = ProxyWidgetLabel(*label_orm.return_data())
                scheme.scene.addItem(label)
                scheme.scene.labels.append(label)
            for pencil_line_orm in scheme_orm.pencil_lines:
                pencil_line = PencilLine(*pencil_line_orm.return_data())
                scheme.scene.addItem(pencil_line)
                scheme.scene.pencil.append(pencil_line)
            for player_orm in scheme_orm.players:
                if player_orm.team_type == TeamType.offence or player_orm.team_type == TeamType.kickoff\
                        or player_orm.team_type == TeamType.punt_kick or player_orm.team_type == TeamType.field_goal_off:
                    player = FirstTeamPlayer(*player_orm.return_data())
                    scheme.scene.addItem(player)
                    scheme.scene.first_team_players.append(player)
                    for line_orm in player_orm.lines:
                        line = ActionLine(player, *line_orm.return_data())
                        if f'action_number:{line.action_number}' not in player.actions.keys():
                            player.actions[f'action_number:{line.action_number}'] = []
                        player.actions[f'action_number:{line.action_number}'].append(line)
                        scheme.scene.addItem(line)
                    for fa_arrow_orm in player_orm.action_finishes_arr:
                        fa_arrow = FinalActionArrow(player, *fa_arrow_orm.return_data())
                        player.actions[f'action_number:{fa_arrow.action_number}'].append(fa_arrow)
                        scheme.scene.addItem(fa_arrow)
                    for fa_line_orm in player_orm.action_finishes_line:
                        fa_line = FinalActionLine(player, *fa_line_orm.return_data())
                        player.actions[f'action_number:{fa_line.action_number}'].append(fa_line)
                        scheme.scene.addItem(fa_line)
                elif player_orm.team_type == TeamType.defence or player_orm.team_type == TeamType.kick_ret\
                        or player_orm.team_type == TeamType.punt_ret or player_orm.team_type == TeamType.field_goal_def:
                    player = SecondTeamPlayer(*player_orm.return_data())
                    scheme.scene.addItem(player)
                    scheme.scene.second_team_players.append(player)
                    for line_orm in player_orm.lines:
                        line = ActionLine(player, *line_orm.return_data())
                        if f'action_number:{line.action_number}' not in player.actions.keys():
                            player.actions[f'action_number:{line.action_number}'] = []
                        player.actions[f'action_number:{line.action_number}'].append(line)
                        scheme.scene.addItem(line)
                    for fa_arrow_orm in player_orm.action_finishes_arr:
                        fa_arrow = FinalActionArrow(player, *fa_arrow_orm.return_data())
                        player.actions[f'action_number:{fa_arrow.action_number}'].append(fa_arrow)
                        scheme.scene.addItem(fa_arrow)
                    for fa_line_orm in player_orm.action_finishes_line:
                        fa_line = FinalActionLine(player, *fa_line_orm.return_data())
                        player.actions[f'action_number:{fa_line.action_number}'].append(fa_line)
                        scheme.scene.addItem(fa_line)
                else:
                    player = FirstTeamPlayer(*player_orm.return_data())
                    scheme.scene.addItem(player)
                    scheme.scene.additional_offence_player = player
                    for line_orm in player_orm.lines:
                        line = ActionLine(player, *line_orm.return_data())
                        if f'action_number:{line.action_number}' not in player.actions.keys():
                            player.actions[f'action_number:{line.action_number}'] = []
                        player.actions[f'action_number:{line.action_number}'].append(line)
                        scheme.scene.addItem(line)
                    for fa_arrow_orm in player_orm.action_finishes_arr:
                        fa_arrow = FinalActionArrow(player, *fa_arrow_orm.return_data())
                        player.actions[f'action_number:{fa_arrow.action_number}'].append(fa_arrow)
                        scheme.scene.addItem(fa_arrow)
                    for fa_line_orm in player_orm.action_finishes_line:
                        fa_line = FinalActionLine(player, *fa_line_orm.return_data())
                        player.actions[f'action_number:{fa_line.action_number}'].append(fa_line)
                        scheme.scene.addItem(fa_line)

    def user_log_in(self, wrong_login_pass=False):
        dialog = DialogLogIn(wrong_login_pass=wrong_login_pass, parent=self)
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
            ...
            # print('Регистрация')

    def user_log_out(self):
        if self.user and self.playbook:
            dialog_save_current_playbook_online = QMessageBox(QMessageBox.Question, 'Сохранение', 'Сохранить текущий плейбук на сервере?', parent=self)
            dialog_save_current_playbook_online.addButton("Да", QMessageBox.AcceptRole)  # результат устанавливается в 0
            dialog_save_current_playbook_online.addButton("Нет", QMessageBox.RejectRole)  # результат устанавливается в 1
            dialog_save_current_playbook_online.exec()
            if not dialog_save_current_playbook_online.result():
                ...
                # print('СОХРАНЕНИЕ НА СЕРВЕРЕ')
        self.user = None
        self.set_gui_enter_exit_online(False)

    def sign_up(self):
        dialog = DialogSignUp(parent=self)
        dialog.exec()

    def new_playbook(self):
        def new_playbook_dialog():
            dialog = DialogNewPlaybook(parent=self)
            dialog.exec()
            playbook_name = dialog.line_edit.text().strip()
            playbook_type = PlaybookType.football if dialog.radio_button_football.isChecked() else PlaybookType.flag
            if dialog.result() == 1 and len(playbook_name) > 0:
                self.create_playbook(playbook_name, playbook_type)

        if self.playbook:
            if self.user:
                question_dialog_new_playbook_online = QMessageBox(QMessageBox.Question, 'Сохранение', 'Сохранить текущий плейбук на сервере?', parent=self)
                question_dialog_new_playbook_online.addButton("Да", QMessageBox.AcceptRole)  # результат устанавливается в 0
                question_dialog_new_playbook_online.addButton("Нет", QMessageBox.RejectRole)  # результат устанавливается в 1
                question_dialog_new_playbook_online.exec()
                if not question_dialog_new_playbook_online.result():
                    ...
                    # print('СОХРАНЕНИЕ НА СЕРВЕРЕ')
            question_dialog_save_current_playbook = QMessageBox(QMessageBox.Question, 'Сохранение', 'Сохранить текущий плейбук на компьютере?', parent=self)
            question_dialog_save_current_playbook.addButton("Да", QMessageBox.AcceptRole)  # результат устанавливается в 0
            question_dialog_save_current_playbook.addButton("Нет", QMessageBox.RejectRole)  # результат устанавливается в 1
            question_dialog_save_current_playbook.exec()
            if not question_dialog_save_current_playbook.result():
                self.save_current_playbook_offline()
            if self.current_scene:
                temp_scene = QGraphicsScene(parent=self)
                # Устанавливается новая сцена и затем удаляется, что бы сразу после нажатия на кнопку диалогового окна, сцена очистилась
                self.graphics_view.setScene(temp_scene)
                temp_scene.deleteLater()
                del temp_scene
                self.current_scene.deleteLater()
                self.current_scene = None
            self.playbook = None
            self.playbook_orm = None
            self.chosen_scheme = None
            self.listWidget_schemes.clear()
            self.label_playbook_name.setText('')
            self.enable_disable_gui(False)
            new_playbook_dialog()
        else:
            new_playbook_dialog()

    def create_playbook(self, playbook_name: str, playbook_type: 'PlaybookType', playbook_id_pk: int = None, team_id_fk: int = None):
        self.playbook = Playbook(playbook_name, playbook_type, playbook_id_pk, team_id_fk)
        self.set_gui_for_playbook()
        self.label_playbook_name.setText(playbook_name)

    # @timeit###################################################################################################
    def save_all_schemes_on_picture(self, checked=None):
        url = QFileDialog.getExistingDirectory(parent=self, caption='Укажите путь для сохранения схем')
        files_with_same_name_list = []
        if url:
            for item_number in range(self.listWidget_schemes.count()):
                url_files_list = list(map(str.lower, QDir(url).entryList(QDir.Files)))
                scheme = self.listWidget_schemes.item(item_number)
                if f'{scheme.text().lower()}.png' in url_files_list:
                    files_with_same_name_list.append(scheme.text())
                    continue
                scheme_top_point, scheme_bot_point = self.get_top_bot_points_for_items_on_scene(scheme.scene)
                if not scheme_top_point is None and scheme.text() not in files_with_same_name_list:
                    rect = QRectF(0, scheme_top_point, scheme.scene.width(), scheme_bot_point - scheme_top_point)
                    self.render_picture(f'{url}/{scheme.text()}.png', scheme.scene, rect)
            if files_with_same_name_list:
                if len(files_with_same_name_list) == 1:
                    message = f'Схема с названием: {f", ".join(files_with_same_name_list)} не была сохранена из-за совпадения с именами файлов в выбранной папке. Для сохранения измените её название.'
                else:
                    message = f'Схемы с названиями: {f", ".join(files_with_same_name_list)} не были сохранены из-за совпадения с именами файлов в выбранной папке. Для сохранения измените их названия.'
                dialog = QMessageBox().information(self, 'Совпадение названий схем', message)

    def get_top_bot_points_for_items_on_scene(self, scene: 'Field') -> tuple[float | None, float | None]:
        if scene.first_team_placed:
            top_y = scene.first_team_players[0].y()
            bot_y = scene.first_team_players[0].y() + scene.first_team_players[0].height
        elif len(scene.rectangles) != 0:
            top_y = scene.rectangles[0].y()
            bot_y = scene.rectangles[0].y() + scene.rectangles[0].rect().height()
        elif len(scene.ellipses) != 0:
            top_y = scene.ellipses[0].y()
            bot_y = scene.ellipses[0].y() + scene.ellipses[0].rect().height()
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

        for figure in scene.rectangles:
            if figure.y() < top_y:
                top_y = figure.y()
            if figure.y() + figure.rect().height() > bot_y:
                bot_y = figure.y() + figure.rect().height()

        for figure in scene.ellipses:
            if figure.y() < top_y:
                top_y = figure.y()
            if figure.y() + figure.rect().height() > bot_y:
                bot_y = figure.y() + figure.rect().height()

        for label in scene.labels:
            if label.y() < top_y:
                top_y = label.y()
            if label.y() + label.rect().height() > bot_y:
                bot_y = label.y() + label.rect().height()
        top_y -= 30  # Отступ от верхней коардинаты итемов сцены
        bot_y += 30  # Отступ от нижней коардинаты итемов сцены
        top_y = 0 if top_y < 0 else top_y  # Ограничение верхней точки сохраняемой области, верхней границей сцены
        bot_y = scene.current_field_border[1] if bot_y > scene.current_field_border[1] else bot_y
        # Ограничение нижней точки сохраняемой области, нижней границей сцены
        return top_y, bot_y

    '''-----------------------------------------------------------------------------------------------------------------
    ------------------------------------------Общие для плейбуков методы------------------------------------------------
    -----------------------------------------------------------------------------------------------------------------'''
    def connect_signals_from_scene(self, scene: 'Field'):
        scene.modeChanged.connect(lambda mode: getattr(self, f'pushButton_{mode.name}').setChecked(True))
        scene.labelDoubleClicked.connect(self.set_gui_config_from_label)
        scene.labelEditingFinished.connect(self.set_gui_config_from_scene)

    def save_current_scheme_on_picture(self, scene: 'Field'):
        save_window = QFileDialog(parent=self)
        save_window.setOption(QFileDialog.Option.DontConfirmOverwrite, False)
        filters = 'JPEG (*.jpg *.jpeg *.jpe *.jfif);; TIFF (*.tif *.tiff);; PNG (*.png)'
        url, _ = save_window.getSaveFileName(self, 'Сохранить как изображение', filter=filters, selectedFilter='PNG (*.png)')
        if url:
            poly = self.graphics_view.mapToScene(QRect(0, 0, self.graphics_view.width() - 14, self.graphics_view.height() - 13))
            rect = poly.boundingRect()
            if rect.x() < 0:
                rect.setWidth(rect.width() + rect.x())
                rect.setX(- scene.field_data.border_width / 2)
            if rect.y() <= 0:
                rect.setHeight(rect.height() + rect.y())
                rect.setY(- scene.field_data.border_width / 2)
            self.render_picture(url, scene, rect)

    def render_picture(self, url: str, rendering_scene: 'Field', rendering_area: 'QRectF'):
        base_width = 1000
        img = QImage(base_width, base_width * rendering_area.height() / rendering_area.width(), QImage.Format_ARGB8565_Premultiplied)
        img.fill(QColor(Qt.white))
        painter = QPainter(img)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.VerticalSubpixelPositioning | QPainter.LosslessImageRendering)
        rendering_scene.render(painter, source=rendering_area)
        img.save(f'{url}')
        painter.end()

    def combobox_font_changed(self, scene: 'Field', font: 'QFont'):
        if scene.current_label:
            current_label_font = scene.current_label.font()
            current_label_font.setFamily(font.family())
            scene.current_label.setFont(current_label_font)
            scene.current_label.update_height()
        else:
            scene.set_config('font_type', font)

    def font_size_changed(self, scene: 'Field', font_size: str):
        if scene.current_label:
            current_label_font = scene.current_label.font()
            current_label_font.setPointSize(int(font_size))
            scene.current_label.setFont(current_label_font)
            scene.current_label.update_height()
        else:
            scene.set_config('font_size', int(font_size))

    def bold_changed(self, scene: 'Field', bold_condition: bool):
        if scene.current_label:
            current_label_font = scene.current_label.font()
            current_label_font.setBold(bold_condition)
            scene.current_label.setFont(current_label_font)
            scene.current_label.update_height()
        else:
            scene.set_config('bold', bold_condition)

    def italic_changed(self, scene: 'Field', italic_condition: bool):
        if scene.current_label:
            current_label_font = scene.current_label.font()
            current_label_font.setItalic(italic_condition)
            scene.current_label.setFont(current_label_font)
            scene.current_label.update_height()
        else:
            scene.set_config('italic', italic_condition)

    def underline_changed(self, scene: 'Field', underline_condition: bool):
        if scene.current_label:
            current_label_font = scene.current_label.font()
            current_label_font.setUnderline(underline_condition)
            scene.current_label.setFont(current_label_font)
            scene.current_label.update_height()
        else:
            scene.set_config('underline', underline_condition)

    def color_changed(self, scene: 'Field', color: str):
        if scene.current_label:
            text_cursor = scene.current_label.textCursor()
            scene.current_label.selectAll()
            scene.current_label.setTextColor(color)
            scene.current_label.setTextCursor(text_cursor)
            scene.current_label.update_height()
        else:
            scene.set_config('color', color)

    def set_gui_config_from_scene(self):
        self.fontComboBox.setCurrentFont(self.current_scene.config['font_type'])
        self.comboBox_font_size.setCurrentText(str(self.current_scene.config['font_size']))
        self.pushButton_bold.setChecked(self.current_scene.config['bold'])
        self.pushButton_italic.setChecked(self.current_scene.config['italic'])
        self.pushButton_underline.setChecked(self.current_scene.config['underline'])
        self.pushButton_current_color.setStyleSheet(f'background-color: {self.current_scene.config["color"]};')

    def set_gui_config_from_label(self):
        self.fontComboBox.setCurrentFont(self.current_scene.current_label.font())
        self.comboBox_font_size.setCurrentText(str(self.current_scene.current_label.font().pointSize()))
        self.pushButton_bold.setChecked(self.current_scene.current_label.font().bold())
        self.pushButton_italic.setChecked(self.current_scene.current_label.font().italic())
        self.pushButton_underline.setChecked(self.current_scene.current_label.font().underline())
        self.pushButton_current_color.setStyleSheet(f'background-color: {self.current_scene.current_label.textColor().name()};')

    # ТУТ БЫЛ МЕТОД enable_disable_gui

    '''-----------------------------------------------------------------------------------------------------------------
    --------------------------------------------Методы футбольного плейбука---------------------------------------------
    -----------------------------------------------------------------------------------------------------------------'''
    def edit_playbook_name(self):
        dialog = QInputDialog(parent=self)
        dialog.setOkButtonText('ОК')
        dialog.setCancelButtonText('Отмена')
        text, result = dialog.getText(self, 'Изменение названия плейбука', 'Название плейбука: ', QLineEdit.Normal, self.playbook.name)
        if result:
            self.playbook.name = text.strip()
            self.label_playbook_name.setText(text.strip())

    def add_new_scheme(self):
        if self.listWidget_schemes.count() == 0:
            self.enable_disable_gui(True)
        scheme = self.create_scheme('')
        self.listWidget_schemes.setCurrentItem(scheme)
        self.choose_current_scheme()
        self.edit_current_scheme()

    def create_scheme(self, scheme_name: str, view_point_x: float | None = None, view_point_y: float | None = None,
                      first_team_placed: Union['TeamType', None] = None, second_team_placed: Union['TeamType', None] = None,
                      first_team_position: int | None = None, scheme_id_pk: int = None, playbook_id_fk: int = None):
        scheme = Scheme(self, self.playbook.type, scheme_name, view_point_x, view_point_y,
                        first_team_placed, second_team_placed, first_team_position,
                        scheme_id_pk, playbook_id_fk)
        self.playbook.add_scheme(scheme)
        self.listWidget_schemes.addItem(scheme)
        self.connect_signals_from_scene(scheme.scene)
        return scheme

    def delete_current_scheme(self):
        scheme = self.listWidget_schemes.takeItem(self.listWidget_schemes.currentRow())
        if self.listWidget_schemes.count() > 0:
            if scheme is self.chosen_scheme:
                self.chosen_scheme = None
                self.current_scene = None
                self.choose_current_scheme()
        else:
            if self.current_scene:
                self.current_scene.deleteLater()
                self.current_scene = None
            self.chosen_scheme = None
            self.enable_disable_gui(False)
            if self.playbook:
                self.set_gui_for_playbook()
        if scheme.scheme_id_pk:
            scheme.is_deleted = True
        else:
            self.playbook.remove_scheme(scheme)
            del scheme

    def edit_current_scheme(self):
        scheme = self.listWidget_schemes.currentItem()
        scheme.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
        self.listWidget_schemes.editItem(scheme)
        scheme.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    def choose_current_scheme(self):
        if self.listWidget_schemes.count() != 0:
            self.chosen_scheme = self.listWidget_schemes.currentItem()
            self.current_scene = self.chosen_scheme.scene
            self.graphics_view.setScene(self.current_scene)
            self.graphics_view.set_current_zoom(self.current_scene.zoom)
            self.graphics_view.centerOn(self.current_scene.view_point)
            self.set_check_boxes_for_schemes()
            self.set_gui_for_current_scene()

    def set_check_boxes_for_schemes(self):
        for scheme_number in range(self.listWidget_schemes.count()):
            scheme = self.listWidget_schemes.item(scheme_number)
            if self.current_theme == AppTheme.dark:
                scheme.setIcon(QIcon(QPixmap('://Themes/Dark_theme/CheckBox-0(dark_theme).png')))
                scheme.setForeground(QColor('#b1b1b1'))
            elif self.current_theme == AppTheme.light:
                scheme.setIcon(QIcon(QPixmap('://Themes/Light_theme/CheckBox-0(light_theme).png')))
                scheme.setForeground(QColor(Qt.black))
        if self.chosen_scheme:
            if self.current_theme == AppTheme.dark:
                self.chosen_scheme.setIcon(QIcon(QPixmap('://Themes/Dark_theme/CheckBox-1(dark_theme).png')))
                self.chosen_scheme.setForeground(QColor('#27c727'))
            elif self.current_theme == AppTheme.light:
                self.chosen_scheme.setIcon(QIcon(QPixmap('://Themes/Light_theme/CheckBox-1(light_theme).png')))
                self.chosen_scheme.setForeground(QColor('#1a6aa7'))

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
            self.lineEdit_yards.setText('75') if int(value) >= 70 else self.lineEdit_yards.setText('65')
        elif self.comboBox_team_type.currentIndex() == 2:  # Пант нет смысла пробивать если до зачётной зоны меньше 20 ярдов
            if int(value) <= 20:
                self.lineEdit_yards.setText('20')

    def place_first_team_football(self, scene: 'Field'):
        self.validate_yards_football(self.lineEdit_yards.text())
        if scene and not scene.first_team_placed:
            team_type = TeamType(self.comboBox_team_type.currentIndex())
            scene.create_first_team_players_football(team_type, int(self.lineEdit_yards.text()))
            scene.first_team_placed = team_type
            scene.first_team_position = int(self.lineEdit_yards.text())
            self.set_gui_first_team_placed()

    def place_second_team_football(self, scene: 'Field'):
        if scene and scene.first_team_placed and not scene.second_team_placed:
            team_type = TeamType(scene.first_team_placed.value + 4)  # В TeamType нумерация типов второй команды начинается с 4 и соотвествует типам первой команды
            scene.create_second_team_football(team_type, int(self.lineEdit_yards.text()))
            scene.second_team_placed = team_type
            self.set_gui_for_second_team(True)

    def place_additional_offence_player(self, scene: 'Field'):
        if scene.first_team_placed == TeamType.offence and not scene.additional_offence_player:
            scene.create_additional_offence_player(int(self.lineEdit_yards.text()))
            # self.playbook.playbook_type.name = или football или flag
            self.set_gui_for_additional_offence_player(True)

    def delete_second_team(self, scene: 'Field'):
        if scene and scene.second_team_placed:
            scene.delete_second_team_players()
            self.set_gui_for_second_team(False)

    def delete_additional_offence_player(self, scene: 'Field'):
        if scene and scene.additional_offence_player:
            scene.delete_additional_offence_player()
            self.set_gui_for_additional_offence_player(False)

    def delete_all_players(self, scene: 'Field'):
        if scene and scene.first_team_placed:
            scene.delete_all_players()
            self.set_gui_all_teams_deleted()

    def second_team_symbol_changed(self, scene: 'Field'):
        symbol_type = SymbolType(self.comboBox_second_players_symbol.currentIndex())
        for player in scene.second_team_players:
            player.symbol_type = symbol_type
            player.text_color = '#000000'
            player.player_color = '#000000'

    '''-----------------------------------------------------------------------------------------------------------------
    -------------------------------------------Методы флаг-футбольного плейбука-----------------------------------------
    -----------------------------------------------------------------------------------------------------------------'''
    def check_max_yards_flag(self, value: str):
        try:
            if int(value) > 50:
                self.lineEdit_yards.setText('50')
        except ValueError:
            pass

    def validate_yards_flag(self, value: str):
        if not value.isdigit():
            self.lineEdit_yards.setText('25')

    def place_first_team_flag(self, scene: 'Field'):
        self.validate_yards_flag(self.lineEdit_yards.text())
        if scene and not scene.first_team_placed:
            scene.create_players_flag(TeamType.offence, int(self.lineEdit_yards.text()))
            scene.first_team_placed = TeamType.offence
            scene.first_team_position = int(self.lineEdit_yards.text())
            self. set_gui_first_team_placed()

    def place_second_team_flag(self, scene: 'Field'):
        if scene and scene.first_team_placed == TeamType.offence and not scene.second_team_placed:
            scene.create_players_flag(TeamType.defence, int(self.lineEdit_yards.text()))
            scene.second_team_placed = TeamType.defence
            self.set_gui_for_second_team(True)

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

    def set_dark_theme(self):
        self.current_theme = AppTheme.dark
        self.about_ico_path = '://Themes/Dark_theme/tactic(dark128).png'
        # self.setStyleSheet(open('Interface/Dark_theme/PlayCreator_dark_theme.css').read())
        style_file = QFile('://Themes/Dark_theme/PlayCreator_dark_theme.css')
        style_file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(style_file)
        style = stream.readAll()
        style_file.close()
        self.setStyleSheet(str(style))
        self.set_check_boxes_for_schemes()
        self.action_new_playbook.setIcon(QIcon(QPixmap('://Themes/Dark_theme/new_playbook(dark_theme).png')))
        self.action_open_playbook_offline.setIcon(QIcon(QPixmap('://Themes/Dark_theme/open(dark_theme).png')))
        self.action_save_playbook_offline.setIcon(QIcon(QPixmap('://Themes/Dark_theme/save(dark_theme).png')))
        self.action_save_playbook_offline_as.setIcon(QIcon(QPixmap('://Themes/Dark_theme/save_as(dark_theme).png')))
        self.action_open_playbook_online.setIcon(QIcon(QPixmap('://Themes/Dark_theme/open_from_server(dark_theme).png')))
        self.action_save_playbook_online.setIcon(QIcon(QPixmap('://Themes/Dark_theme/save_on_server(dark_theme).png')))
        self.action_save_like_picture.setIcon(QIcon(QPixmap('://Themes/Dark_theme/save_like_picture(dark_theme).png')))
        self.action_save_all_like_picture.setIcon(QIcon(QPixmap('://Themes/Dark_theme/save_all_like_picture(dark_theme).png')))
        self.action_presentation_mode.setIcon(QIcon(QPixmap('://Themes/Dark_theme/presentation_mode(dark_theme).png')))
        for mode in Modes:
            getattr(self, f'pushButton_{mode.name}').setIcon(QIcon(QPixmap(f'://Themes/Dark_theme/{mode.name}(dark_theme).png')))
        self.pushButton_delete_actions.setIcon(QIcon(QPixmap(f'://Themes/Dark_theme/delete_actions(dark_theme).png')))
        self.pushButton_delete_figures.setIcon(QIcon(QPixmap(f'://Themes/Dark_theme/delete_figures(dark_theme).png')))
        self.pushButton_delete_pencil.setIcon(QIcon(QPixmap(f'://Themes/Dark_theme/delete_pencil(dark_theme).png')))
        self.pushButton_delete_labels.setIcon(QIcon(QPixmap(f'://Themes/Dark_theme/delete_labels(dark_theme).png')))

    def set_light_theme(self):
        self.current_theme = AppTheme.light
        self.about_ico_path = '://Themes/Light_theme/tactic(light128).png'
        # self.setStyleSheet(open('Interface/Light_theme/PlayCreator_light_theme.css').read())
        style_file = QFile('://Themes/Light_theme/PlayCreator_light_theme.css')
        style_file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(style_file)
        style = stream.readAll()
        style_file.close()
        self.setStyleSheet(str(style))
        self.set_check_boxes_for_schemes()
        self.action_new_playbook.setIcon(QIcon(QPixmap('://Themes/Light_theme/new_playbook(light_theme).png')))
        self.action_open_playbook_offline.setIcon(QIcon(QPixmap('://Themes/Light_theme/open(light_theme).png')))
        self.action_save_playbook_offline.setIcon(QIcon(QPixmap('://Themes/Light_theme/save(light_theme).png')))
        self.action_save_playbook_offline_as.setIcon(QIcon(QPixmap('://Themes/Light_theme/save_as(light_theme).png')))
        self.action_open_playbook_online.setIcon(QIcon(QPixmap('://Themes/Light_theme/open_from_server(light_theme).png')))
        self.action_save_playbook_online.setIcon(QIcon(QPixmap('://Themes/Light_theme/save_on_server(light_theme).png')))
        self.action_save_like_picture.setIcon(QIcon(QPixmap('://Themes/Light_theme/save_like_picture(light_theme).png')))
        self.action_save_all_like_picture.setIcon(QIcon(QPixmap('://Themes/Light_theme/save_all_like_picture(light_theme).png')))
        self.action_presentation_mode.setIcon(QIcon(QPixmap('://Themes/Light_theme/presentation_mode(light_theme).png')))
        for mode in Modes:
            getattr(self, f'pushButton_{mode.name}').setIcon(QIcon(QPixmap(f'://Themes/Light_theme/{mode.name}(light_theme).png')))
        self.pushButton_delete_actions.setIcon(QIcon(QPixmap(f'://Themes/Light_theme/delete_actions(light_theme).png')))
        self.pushButton_delete_figures.setIcon(QIcon(QPixmap(f'://Themes/Light_theme/delete_figures(light_theme).png')))
        self.pushButton_delete_pencil.setIcon(QIcon(QPixmap(f'://Themes/Light_theme/delete_pencil(light_theme).png')))
        self.pushButton_delete_labels.setIcon(QIcon(QPixmap(f'://Themes/Light_theme/delete_labels(light_theme).png')))

    def about_clicked(self):
        dialog = DialogAbout(self.version, self.about_ico_path, parent=self)
        dialog.exec()

    def presentation_mode(self):
        self.groupBox_team_playbook_settings.setVisible(not self.action_presentation_mode.isChecked())
        self.label_current_zoom.setVisible(not self.action_presentation_mode.isChecked())

    def __repr__(self):
        return f'<{self.__class__.__name__} (maximized: {self.isMaximized()}, x: {self.x()}, y: {self.y()},' \
               f' width: {self.width()}, height: {self.height()}, toolbar: {self.toolBar_main.isVisible()},' \
               f' toolbar_area: {self.toolBarArea(self.toolBar_main)}, theme: {self.current_theme}) at {hex(id(self))}>'

    def return_data(self):
        return self.isMaximized(), self.toolBar_main.isVisible(), self.toolBarArea(self.toolBar_main), self.current_theme


if __name__ == '__main__':
    create_db_if_not_exists()
    app = QApplication(sys.argv)
    # screen_rect = app.primaryScreen().availableGeometry()
    if os.path.exists(f'SplashScreen.jpg'):
        splash = QSplashScreen(QPixmap('SplashScreen.jpg').scaled(1000, 700, Qt.AspectRatioMode.KeepAspectRatio), f=Qt.WindowStaysOnTopHint)
    else:
        splash = QSplashScreen(QPixmap('://Splash/SplashScreen.jpg').scaled(1000, 700, Qt.AspectRatioMode.KeepAspectRatio), f=Qt.WindowStaysOnTopHint)
    frame = QFrame(parent=splash)
    frame.setFixedSize(splash.width(), splash.height())
    frame.setFrameShadow(QFrame.Shadow.Raised)
    frame.setFrameShape(QFrame.Shape.Box)
    frame.setLineWidth(0)
    frame.setMidLineWidth(3)
    splash.show()
    sleep(2)
    play_creator = PlayCreator(get_user_settings())
    # x = (screen_rect.width() - play_creator.width()) // 2
    # y = (screen_rect.height() - play_creator.height()) // 2
    # play_creator.move(x, y)
    play_creator.show()
    splash.finish(play_creator)
    play_creator.user_log_in()
    sys.exit(app.exec())
