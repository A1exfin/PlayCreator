from typing import TYPE_CHECKING, Union
from datetime import datetime
from math import radians, cos, sin
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import Qt, Signal, QPointF, QLineF, QRectF, QRect
from PySide6.QtGui import QFont, QPen, QBrush, QColor, QPolygonF
from Enums import PlaybookType, Modes, TeamType
from Data import FieldData, PlayersData
import Graphics

if TYPE_CHECKING:
    from PySide6.QtWidgets import QMainWindow

__all__ = ['Field']


def timeit(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        print(datetime.now() - start)
        return result
    return wrapper


class Field(QGraphicsScene):
    labelDoubleClicked = Signal(object)
    labelEditingFinished = Signal(object)
    modeChanged = Signal(Modes)

    def __init__(self, main_window: 'QMainWindow', playbook_type: 'PlaybookType', parent=None):
        super().__init__(parent=parent)
        self.main_window = main_window
        self.playbook_type = playbook_type
        self.field_data = FieldData()
        self.players_data = PlayersData(self.field_data)

        # Точка обзора. На неё наводится GraphicsView при смене схемы. При создании схемы устнавливается на середину поля
        self.view_point = QPointF(getattr(self.field_data, f'{self.playbook_type.name}_field_width') / 2,
                                  getattr(self.field_data, f'{self.playbook_type.name}_field_length') / 2)
        self.zoom = 60  # Значение приближения сцены (при выборе схемы устанавливается это значение приближения)

        self.first_team_placed = None
        self.first_team_position = None
        self.first_team_players = []
        # Если игроки первой команды имеют id_pk (то есть они загружены из БД с помощью ORM),
        # то при удалении они добавляются в этот список, что бы обновить ORM и затем удалить игроков из БД
        self.deleted_first_team_players = []

        self.additional_offence_player = None
        # Если дополнительный игрок имеет id_pk (то есть он загружен из БД с помощью ORM),
        # то при удалении он сохраняется в этом атрибуте, что бы обновить ORM и затем удалить игрока из БД
        self.deleted_additional_offence_player = None

        self.second_team_placed = None
        self.second_team_players = []
        # Если игроки второй команды имеют id_pk (то есть они загружены из БД с помощью ORM),
        # то при удалении они добавляются в этот список, что бы обновить ORM и затем удалить игроков из БД
        self.deleted_second_team_players = []

        self.current_field_border = None  # Границы текущего поля, используются при рисовании для проверки попадания event внутрь поля

        if self.playbook_type == PlaybookType.football:
            self.draw_football_field()
        elif self.playbook_type == PlaybookType.flag:
            self.draw_flag_field()

        self.config = {
            # Drawing options.
            'line_thickness': 4,
            'color': '#000000',
            # Font options.
            'font_type': QFont('Times New Roman'),
            'font_size': 12,
            'bold': False,
            'italic': False,
            'underline': False
        }

        self.allow_painting = False  # Флаг разрешения рисования, активируется по клику на игрока или на некоторые действия игрока
        self.painting = False  # Флаг показывает что сейчас идёт процесс рисования
        self.mouse_pressed_painting = False  # Флаг нажатия кнопки мыши. Нужен для того, чтобы при рисовании действия игрока исключить нажатие второй кнопки мыши (правой), при нажатой левой
        self.current_player = None  # Текущий игрок по которому кликнули, от него рисуется действие
        self.player_center_pos = None  # Коардинаты центра кликнутого игрока
        self.start_pos = None  # Коардинаты начала рисования действий, фигур и тд
        self.last_start_pos = None  # Коардинаты предыдущей стартовой точки. Используется при завершении рисования действия, для вычисления угла поворота стрелки маршрута или линии блока
        self.current_line = None  # Текущая линия действия
        self.current_action_lines = []  # Список текущих действий при данной операции рисования
        self.action_number_temp = None  # Временный номер рисуемого действия. В него записывается номер кликнутого маршрута,
        # при рисовании опционных маршрутов или действия после моушена

        self.rectangles = []  # Список прямоугольников расположенных на сцене
        self.ellipses = []  # Список эллипсов расположенных на сцене
        self.current_figure = None  # Рисуемая в данный момент фигура

        self.labels = []  # Список надписей расположенных на сцене
        self.current_label = None  # Редактируемая в данный момент надпись

        self.pencil = []  # Список всех линий рисунка карандаша

        self.mode = Modes.move

    def set_mode(self, mode):
        '''Установка мода сцены'''
        if self.painting:
            if self.mode == Modes.route or self.mode == Modes.block:
                action_finish = self.get_action_finish(self.last_start_pos, self.start_pos)  ################
                self.addItem(action_finish)
            if self.mode == Modes.route or self.mode == Modes.block or self.mode == Modes.motion:
                if self.action_number_temp is not None:
                    self.current_player.actions[f'action_number:{self.current_player.current_action_number}'].append(action_finish)
                    self.current_player.current_action_number = self.action_number_temp
                    self.action_number_temp = None
                else:
                    try:
                        self.current_action_lines.append(action_finish)
                    except UnboundLocalError:
                        pass
                    self.current_player.actions[f'action_number:{self.current_player.current_action_number}'] = self.current_action_lines.copy()
                    self.current_action_lines.clear()
                    self.current_player.current_action_number += 1
            elif self.mode == Modes.rectangle or self.mode == Modes.ellipse:
                self.removeItem(self.current_figure)
                self.current_figure = None
        self.allow_painting = False
        self.painting = False
        self.mouse_pressed_painting = False
        if self.current_player:
            self.current_player.ungrabMouse()
            self.current_player.setSelected(False)
        self.current_player = None
        self.start_pos = None
        self.last_start_pos = None
        if self.current_line:
            self.removeItem(self.current_line)
            self.current_line = None
        if self.current_label:
            self.current_label.proxy.start_pos = None
            self.current_label.proxy.hover = None
            self.current_label.proxy.selected_border = None
            self.current_label.clear_focus()
        self.mode = mode
        self.modeChanged.emit(self.mode)
        self.update()

    def set_config(self, key, value):
        '''Установка конфига цвета, толщины линий, размера текста и тд.'''
        self.config[key] = value

    def get_yards_to_end_zone_football(self, first_team_position: int):
        return self.field_data.football_ten_yard + self.field_data.football_one_yard * first_team_position

    def get_yards_to_end_zone_flag(self, first_team_position: int):
        return self.field_data.flag_ten_yard + self.field_data.flag_one_yard * first_team_position

    def create_first_team_players_football(self, team_type: TeamType, first_team_position: int):
        yards_to_end_zone = self.get_yards_to_end_zone_football(first_team_position)
        players = getattr(self.players_data, f'{team_type.name}_{self.playbook_type.name}')
        for i, player in enumerate(players):
            team, position, text, text_color, fill_color, fill_type, x, y = player
            if i == 10 and team == TeamType.punt_kick and\
                    yards_to_end_zone >= self.field_data.football_ten_yard + self.field_data.football_one_yard * 95:
                item = Graphics.FirstTeamPlayer(team, position, text, text_color, fill_color, fill_type, x,
                                                119 * self.field_data.football_one_yard - self.players_data.player_size / 2)
            else:
                item = Graphics.FirstTeamPlayer(team, position, text, text_color, fill_color, fill_type, x,
                                                y + yards_to_end_zone)
            self.addItem(item)
            self.first_team_players.append(item)

    def create_second_team_football(self, team_type: TeamType, first_team_position: int):
        yards_to_end_zone = self.get_yards_to_end_zone_football(first_team_position)
        players = getattr(self.players_data, f'{team_type.name}_{self.playbook_type.name}')
        for i, player in enumerate(players):
            team, position, text, text_color, border_color, symbol, x, y = player
            if (team == TeamType.punt_ret and i == 10) or (team == TeamType.kick_ret and i == 10):  # punt_returner and kick_returner
                item = Graphics.SecondTeamPlayer(team, position, text, text_color, border_color, symbol, x, y)
            elif team == TeamType.field_goal_def and i == 10\
                    and yards_to_end_zone > self.field_data.football_ten_yard + self.field_data.football_one_yard * 20:  # kick returner
                item = Graphics.SecondTeamPlayer(team, position, text, text_color, border_color, symbol, x,
                                                 self.field_data.football_five_yard)
            elif team == TeamType.defence and i == 10\
                    and yards_to_end_zone < self.field_data.football_ten_yard + self.field_data.football_one_yard * 3:  # free safety
                item = Graphics.SecondTeamPlayer(team, position, text, text_color, border_color, symbol, x,
                                                 y + yards_to_end_zone + 3 * self.field_data.football_one_yard)
            elif team == TeamType.kick_ret and 4 < i <= 7\
                    and yards_to_end_zone == self.field_data.football_ten_yard + self.field_data.football_one_yard * 75:  # second line
                item = Graphics.SecondTeamPlayer(team, position, text, text_color, border_color, symbol, x,
                                                 y + yards_to_end_zone - self.field_data.football_five_yard)
            elif team == TeamType.kick_ret and 7 < i <= 9\
                    and yards_to_end_zone == self.field_data.football_ten_yard + self.field_data.football_one_yard * 75:  # third line
                item = Graphics.SecondTeamPlayer(team, position, text, text_color, border_color, symbol, x,
                                                 y + yards_to_end_zone - self.field_data.football_ten_yard)
            else:  # other players
                item = Graphics.SecondTeamPlayer(team, position, text, text_color, border_color, symbol, x,
                                                 y + yards_to_end_zone)
            self.addItem(item)
            self.second_team_players.append(item)

    def create_additional_offence_player(self, first_team_position: int):
        yards_to_end_zone = getattr(self, f'get_yards_to_end_zone_{self.playbook_type.name}')(first_team_position)
        team, position, text, text_color, fill_color, fill_type, x, y = getattr(self.players_data, f'additional_player_{self.playbook_type.name}')
        # self.playbook_type.name = или football или flag
        self.additional_offence_player = Graphics.FirstTeamPlayer(team, position, text, text_color, fill_color, fill_type, x,
                                                                  y + yards_to_end_zone)
        self.addItem(self.additional_offence_player)

    def create_players_flag(self, team_type: TeamType, first_team_position: int):
        yards_to_end_zone = self.get_yards_to_end_zone_flag(first_team_position)
        players = getattr(self.players_data, f'{team_type.name}_{self.playbook_type.name}')
        for i, player in enumerate(players):
            team, position, text, text_color, fill_color, fill_type, x, y = player
            if team == TeamType.offence:
                item = Graphics.FirstTeamPlayer(team, position, text, text_color, fill_color, fill_type, x,
                                                y + yards_to_end_zone)
                self.first_team_players.append(item)
            else:
                item = Graphics.SecondTeamPlayer(team, position, text, text_color, fill_color, fill_type, x,
                                                 y + yards_to_end_zone)
                self.second_team_players.append(item)
            self.addItem(item)

    def delete_second_team_players(self):
        if self.second_team_placed:
            self.delete_second_team_actions()
            for player in self.second_team_players.copy():
                if player.player_id_pk:
                    self.deleted_second_team_players.append(player)
                self.second_team_players.remove(player)
                self.removeItem(player)
            self.second_team_placed = None
            if self.allow_painting and \
                    (self.current_player.team_type == TeamType.defence  # Используется для команды защиты в футболе и во флаге
                     or self.current_player.team_type == TeamType.punt_ret
                     or self.current_player.team_type == TeamType.kick_ret
                     or self.current_player.team_type == TeamType.field_goal_def):
                self.delete_drawing_actions()
            self.update()

    def delete_additional_offence_player(self):
        if self.additional_offence_player:
            self.additional_offence_player.delete_actions()
            if self.additional_offence_player.player_id_pk:
                self.deleted_additional_offence_player = self.additional_offence_player
            self.removeItem(self.additional_offence_player)
            self.additional_offence_player = None
            if self.allow_painting and self.current_player.team_type == TeamType.offence_add:
                self.delete_drawing_actions()
            self.update()

    def delete_all_players(self):
        if self.first_team_placed:
            self.delete_first_team_actions()
            for player in self.first_team_players.copy():
                if player.player_id_pk:
                    self.deleted_first_team_players.append(player)
                self.first_team_players.remove(player)
                self.removeItem(player)
            self.first_team_placed = None
            self.first_team_position = None
            self.delete_additional_offence_player()
            self.delete_second_team_players()
            if self.allow_painting:
                self.delete_drawing_actions()
            self.update()

    def delete_first_team_actions(self):
        if self.first_team_placed:
            for player in self.first_team_players:
                player.delete_actions()
        if self.additional_offence_player:
            self.additional_offence_player.delete_actions()

    def delete_second_team_actions(self):
        if self.second_team_placed:
            for player in self.second_team_players:
                player.delete_actions()

    def delete_all_players_actions(self):
        self.delete_first_team_actions()
        self.delete_second_team_actions()
        if self.allow_painting:
            self.delete_drawing_actions()
        self.update()

    def delete_drawing_actions(self):
        '''Вызывается во время рисования, при удалении команды для которой рисуется в данный момент действие,
         для корректного завершения рисования (удаление линий со сцены)'''
        self.current_player.setSelected(False)
        self.current_player.hover = False
        self.allow_painting = False
        self.painting = False
        self.mouse_pressed_painting = False
        self.current_player = None
        self.player_center_pos = None
        self.start_pos = None
        self.last_start_pos = None
        self.removeItem(self.current_line)
        self.current_line = None
        for line in self.current_action_lines:
            self.removeItem(line)
        self.current_action_lines.clear()
        self.action_number_temp = None

    # def mouseDoubleClickEvent(self, event):
    #     if self.mode == Modes.move:
    #         super().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):  # Обработка нажатия кнопки мыши и перенаправление на другие методы в зависимости от mode
        if self.mode == Modes.move:
            super().mousePressEvent(event)
        elif self.mode == Modes.route or self.mode == Modes.block or self.mode == Modes.motion:
            if self.allow_painting:
                self.action_mousePressEvent(event)
            else:  # Это условие для выбора игрока от которого будут рисоваться действия, и установки флага разрешения рисования
                super().mousePressEvent(event)
        elif self.mode == Modes.erase:
            super().mousePressEvent(event)
        elif self.mode == Modes.rectangle or self.mode == Modes.ellipse:
            self.figure_mousePressEvent(event)
        elif self.mode == Modes.label:
            self.label_mousePressEvent(event)
        elif self.mode == Modes.pencil:
            self.pencil_mousePressEvent(event)

    def mouseMoveEvent(self, event):  # Обработка движения курсора мыши и перенаправление на другие методы в зависимости от mode
        if self.mode == Modes.move:
            super().mouseMoveEvent(event)
        elif self.mode == Modes.route or self.mode == Modes.block or self.mode == Modes.motion:
            if self.allow_painting:
                self.action_mouseMoveEvent(event)
            else:
                super().mouseMoveEvent(event)
        elif self.mode == Modes.erase:
            super().mouseMoveEvent(event)
        elif self.mode == Modes.rectangle or self.mode == Modes.ellipse:
            self.figure_mouseMoveEvent(event)
        elif self.mode == Modes.pencil:
            self.pencil_mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):  # Обработка отпускания кнопки мыши и перенаправление на другие методы в зависимости от mode
        if self.mode == Modes.move:
            super().mouseReleaseEvent(event)
        elif self.mode == Modes.route or self.mode == Modes.block or self.mode == Modes.motion:
            if self.allow_painting:
                self.action_mouseReleaseEvent(event)
            # else:
            #     super().mouseReleaseEvent(event)
        elif self.mode == Modes.rectangle or self.mode == Modes.ellipse:
            self.figure_mouseReleaseEvent(event)
        elif self.mode == Modes.pencil:
            self.pencil_mouseReleaseEvent(event)

    def action_mousePressEvent(self, event):  # Рисование действий игроков
        if not self.painting and event.button() == Qt.LeftButton:
            if self.check_field_borders(event.scenePos()):
                if self.player_center_pos:
                    self.get_start_pos(self.player_center_pos, event.scenePos())
                action_line = Graphics.ActionLine(self.current_player, self.start_pos.x(), self.start_pos.y(),
                                                  event.scenePos().x(), event.scenePos().y(),
                                                  self.current_player.current_action_number,
                                                  self.config['line_thickness'], self.config['color'], self.mode)
                self.addItem(action_line)
                self.current_line = action_line
                self.painting = True
                self.mouse_pressed_painting = True
        elif self.painting and not self.current_line and event.button() == Qt.LeftButton:
            if self.check_field_borders(event.scenePos()):
                action_line = Graphics.ActionLine(self.current_player, self.start_pos.x(), self.start_pos.y(),
                                                  event.scenePos().x(), event.scenePos().y(),
                                                  self.current_player.current_action_number,
                                                  self.config['line_thickness'], self.config['color'], self.mode)
                self.addItem(action_line)
                self.current_line = action_line
                self.mouse_pressed_painting = True
        # elif self.painting and self.current_line and event.button() == Qt.LeftButton:
        #     if self.check_field_border(event):
        #         self.mouse_pressed_painting = True
        #         self.current_line.setLine(QLineF(self.start_pos, event.scenePos()))
        elif self.painting and event.button() == Qt.RightButton and not self.mouse_pressed_painting:
            if self.mode == Modes.route or self.mode == Modes.block:
                action_finish = self.get_action_finish(self.last_start_pos, self.start_pos)
                self.addItem(action_finish)
            if self.action_number_temp is not None:
                try:  # необходимо для завершения рисования моушена
                    self.current_player.actions[f'action_number:{self.current_player.current_action_number}'].append(action_finish)
                except UnboundLocalError:
                    pass
                self.current_player.current_action_number = self.action_number_temp
                self.action_number_temp = None
            else:
                try:  # необходимо для завершения рисования моушена
                    self.current_action_lines.append(action_finish)
                except UnboundLocalError:
                    pass
                self.current_player.actions[f'action_number:{self.current_player.current_action_number}'] = self.current_action_lines.copy()
                self.current_action_lines.clear()
                self.current_player.current_action_number += 1
            self.current_player.setSelected(False)
            self.current_player.hover = False
            self.current_player.ungrabMouse()
            self.current_player = None
            self.current_line = None
            self.start_pos = None
            self.last_start_pos = None
            self.painting = False
            self.allow_painting = False
            self.update()

    def action_mouseMoveEvent(self, event):  # Рисование действий игроков
        if self.current_line:
            if self.player_center_pos:
                self.get_start_pos(self.player_center_pos, event.scenePos())
            if self.check_field_borders(event.scenePos()):
                self.current_line.setLine(QLineF(self.start_pos, event.scenePos()))
            else:
                self.current_line.setLine(QLineF(self.start_pos, self.start_pos))

    def action_mouseReleaseEvent(self, event):  # Рисование действий игроков
        if self.current_line and event.button() == Qt.LeftButton:
            if self.check_field_borders(event.scenePos()):
                self.current_line.setLine(QLineF(self.start_pos, event.scenePos()))
                if self.action_number_temp is not None:
                    self.current_player.actions[f'action_number:{self.current_player.current_action_number}'].append(self.current_line)
                else:
                    self.current_action_lines.append(self.current_line)
                self.player_center_pos = None
                self.last_start_pos = self.start_pos
                self.start_pos = event.scenePos()
                self.current_line = None
                self.mouse_pressed_painting = False
            else:
                self.current_line.setLine(QLineF(self.start_pos, self.start_pos))

    def get_start_pos(self, start_pos, finish_pos):
        '''Расчёт начальной точки, находящейся на границе игрока, при рисовании первой линии действия игрока'''
        angle = QLineF(start_pos, finish_pos).angle()
        r = self.current_player.width / 2
        x = cos(radians(angle)) * r
        y = sin(radians(angle)) * r
        self.start_pos = QPointF(start_pos.x() + x, start_pos.y() - y)

    def get_action_finish(self, start_pos, finish_pos):
        '''Получение финала (стрелка для маршрута и линия для блока) действия игрока'''
        angle = QLineF(start_pos, finish_pos).angle()
        if self.mode == Modes.route:
            arrow = Graphics.FinalActionArrow(self.current_player, self.start_pos.x(), self.start_pos.y(), angle,
                                              self.config['line_thickness'], self.config['color'],
                                              self.current_player.current_action_number, self.mode)
            return arrow
        elif self.mode == Modes.block:
            line = Graphics.FinalActionLine(self.current_player, self.start_pos.x(), self.start_pos.y(), angle,
                                            self.config['line_thickness'], self.config['color'],
                                            self.current_player.current_action_number, self.mode)
            return line

    def figure_mousePressEvent(self, event):  # Рисование фигур
        if not self.painting and event.button() == Qt.LeftButton:
            if self.check_field_borders(event.scenePos()):
                self.start_pos = event.scenePos()
                if self.mode == Modes.rectangle:
                    figure = Graphics.Rectangle(self.start_pos.x(), self.start_pos.y(), 0, 0,
                                                True, self.config['line_thickness'], self.config['color'],
                                                False, '#22', '#000000')
                elif self.mode == Modes.ellipse:
                    figure = Graphics.Ellipse(self.start_pos.x(), self.start_pos.y(), 0, 0,
                                              True, self.config['line_thickness'], self.config['color'],
                                              False, '#22', '#000000')
                self.addItem(figure)
                self.current_figure = figure
                self.painting = True
        # elif self.painting and event.button() == Qt.LeftButton and self.current_figure:
        #     if self.check_field_border(event):
        #         self.current_figure.setRect(QRectF(self.start_pos, event.scenePos()))

    def figure_mouseMoveEvent(self, event):  # Рисование фигур
        if self.painting and self.current_figure:
            if self.check_field_borders(event.scenePos()):
                self.current_figure.set_rect(self.start_pos.x(), self.start_pos.y(),
                                             event.scenePos().x() - self.start_pos.x(),
                                             event.scenePos().y() - self.start_pos.y())
            else:
                self.current_figure.set_rect(self.start_pos.x(), self.start_pos.y(), 0, 0)
            self.update()

    def figure_mouseReleaseEvent(self, event):  # Рисование фигур
        if self.painting and self.current_figure and event.button() == Qt.LeftButton:
            if self.check_field_borders(event.scenePos()):
                self.current_figure.set_rect(self.start_pos.x(), self.start_pos.y(),
                                             event.scenePos().x() - self.start_pos.x(),
                                             event.scenePos().y() - self.start_pos.y())
                self.current_figure.normalizate()
                if self.mode == Modes.rectangle:
                    self.rectangles.append(self.current_figure)
                elif self.mode == Modes.ellipse:
                    self.ellipses.append(self.current_figure)
                self.start_pos = None
                self.current_figure = None
                self.painting = False
            else:
                self.current_figure.set_rect(self.start_pos.x(), self.start_pos.y(), 0, 0)

    def delete_figures(self):
        '''Удаление всех фигур со сцены'''
        for rect in self.rectangles.copy():
            if rect.rect_id_pk:
                rect.is_deleted = True
            else:
                self.rectangles.remove(rect)
            self.removeItem(rect)
        for ellipse in self.ellipses.copy():
            if ellipse.ellipse_id_pk:
                ellipse.is_deleted = True
            else:
                self.ellipses.remove(ellipse)
            self.removeItem(ellipse)
        self.update()

    def label_mousePressEvent(self, event):
        '''Размещение надписи на сцене'''
        for label in self.labels:
            label.clearFocus()
        if event.button() == Qt.LeftButton:
            self.set_mode(Modes.move)
            label = Graphics.ProxyWidgetLabel('', self.config['font_type'].family(), self.config['font_size'],
                                              self.config['bold'], self.config['italic'], self.config['underline'], self.config['color'],
                                              event.scenePos().x(), event.scenePos().y())
            self.current_label = label.widget()
            self.current_label.setReadOnly(False)
            self.current_label.setFocus()
            self.labels.append(label)
            self.addItem(label)
            label.widget().update_height()
            if label.x() < 0:
                label.setPos(0, label.y())
            if label.y() < 0:
                label.setPos(label.x(), 0)
            if label.x() + label.rect().width() > self.current_field_border[0]:
                x = label.x() - (label.x() + label.rect().width() - self.current_field_border[0])
                label.setPos(x, label.y())
            if label.y() + label.rect().height() > self.current_field_border[1]:
                y = label.y() - (label.y() + label.rect().height() - self.current_field_border[1])
                label.setPos(label.x(), y)

    def delete_labels(self):
        '''Удаление всех надписей со сцены'''
        for label in self.labels.copy():
            if label.label_id_pk:
                label.is_deleted = True
            else:
                self.labels.remove(label)
            self.removeItem(label)
        self.update()

    def pencil_mousePressEvent(self, event):  # Рисование карандашом
        if event.button() == Qt.LeftButton:
            if self.check_field_borders(event.scenePos()):
                self.start_pos = event.scenePos()

    def pencil_mouseMoveEvent(self, event):  # Рисование карандашом
        if self.check_field_borders(event.scenePos()):
            if self.start_pos:
                line = Graphics.PencilLine(self.start_pos.x(), self.start_pos.y(), event.scenePos().x(), event.scenePos().y(),
                                           self.config['line_thickness'], self.config['color'])
                self.addItem(line)
                self.pencil.append(line)
                self.start_pos = event.scenePos()
                self.update()

    def pencil_mouseReleaseEvent(self, event):  # Рисование карандашом
        if event.button() == Qt.LeftButton:
            self.start_pos = None

    def delete_pencil(self):
        '''Удаление всех риснуков карандаша'''
        for line in self.pencil.copy():
            if line.line_id_pk:
                line.is_deleted = True
            else:
                self.pencil.remove(line)
            self.removeItem(line)
        self.update()

    def check_field_x(self, pos_x: float) -> bool:
        '''Проверка попадания координаты в границы поля по оси X (при рисовании фигур, действий и тд.)'''
        return True if 0 < pos_x < self.current_field_border[0] else False

    def check_field_y(self, pos_y: float) -> bool:
        '''Проверка попадания координаты в границы поля по оси Y (при рисовании фигур, действий и тд.)'''
        return True if 0 < pos_y < self.current_field_border[1] else False

    def check_field_borders(self, mouse_pos: QPointF) -> bool:
        '''Проверка попадания координаты в границы поля по осям X и Y (при рисовании фигур, действий и тд.)'''
        return True if self.check_field_x(mouse_pos.x()) and self.check_field_y(mouse_pos.y()) else False

    def draw_football_field(self):
        '''Отрисовка всего футбольного поля размерами 120 ярдов на 53 ярда. Расстояние между хэш-марками 13 ярдов.
        Пропорция length / width должна быть 1200 / 534'''
        # Установка размеров текущего поля, необходимо для проверки границ поля при рисовании действий игроков
        self.current_field_border = [self.field_data.football_field_width, self.field_data.football_field_length]
        self.setSceneRect(0, 0, self.field_data.football_field_width, self.field_data.football_field_length)
        self.addRect(QRectF(0, 0, self.field_data.football_field_width, self.field_data.football_field_length), QPen(Qt.white), QBrush(QColor(Qt.white)))
        # Отрисовка номеров
        numbers_left_1 = [[f'{i}', 90, self.field_data.gray_color_light, 14 * self.field_data.football_width_one_yard] for i in range(10, 60, 10)]
        numbers_left_2 = [[f'{i}', 90, self.field_data.gray_color_light, 14 * self.field_data.football_width_one_yard] for i in range(40, 0, -10)]
        numbers_right_1 = [[f'{i}', -90, self.field_data.gray_color_light, 40 * self.field_data.football_width_one_yard] for i in range(10, 60, 10)]
        numbers_right_2 = [[f'{i}', -90, self.field_data.gray_color_light, 40 * self.field_data.football_width_one_yard] for i in range(40, 0, -10)]
        numbers_left_y = [16.9 * self.field_data.football_one_yard + i * self.field_data.football_ten_yard for i in range(9)]
        numbers_right_y = [23 * self.field_data.football_one_yard + i * self.field_data.football_ten_yard for i in range(9)]
        # self.addRect(0, 0, self.field_data.football_field_width, self.field_data.football_field_length, QPen(Qt.transparent), QBrush(QColor('#004400')))
        for i, number in enumerate(numbers_left_1):
            self.addItem(Graphics.FieldNumber(*number, numbers_left_y[i]))
        for i, number in enumerate(numbers_left_2):
            self.addItem(Graphics.FieldNumber(*number, numbers_left_y[5 + i]))
        for i, number in enumerate(numbers_right_1):
            self.addItem(Graphics.FieldNumber(*number, numbers_right_y[i]))
        for i, number in enumerate(numbers_right_2):
            self.addItem(Graphics.FieldNumber(*number, numbers_right_y[5 + i]))
        # Отрисовка стрелок около номеров
        polygon_top = QPolygonF([QPointF(5, 0), QPointF(0, 10), QPointF(10, 10)])
        polygon_bot = QPolygonF([QPointF(5, 10), QPointF(0, 0), QPointF(10, 0)])
        arrows_right_coordinates_1 = [[43 * self.field_data.football_width_one_yard, 16 * self.field_data.football_one_yard + i * self.field_data.football_ten_yard] for i in range(4)]
        arrows_left_coordinates_1 = [[10 * self.field_data.football_width_one_yard, 16 * self.field_data.football_one_yard + i * self.field_data.football_ten_yard] for i in range(4)]
        arrows_right_coordinates_2 = [[43 * self.field_data.football_width_one_yard, 23 * self.field_data.football_one_yard + i * self.field_data.football_ten_yard] for i in range(5, 9)]
        arrows_left_coordinates_2 = [[10 * self.field_data.football_width_one_yard, 23 * self.field_data.football_one_yard + i * self.field_data.football_ten_yard] for i in range(5, 9)]
        for coordinates in arrows_left_coordinates_1:
            self.addItem(Graphics.FieldTriangle(polygon_top, self.field_data.gray_color_light, *coordinates))
        for coordinates in arrows_left_coordinates_2:
            self.addItem(Graphics.FieldTriangle(polygon_bot, self.field_data.gray_color_light, *coordinates))
        for coordinates in arrows_right_coordinates_1:
            self.addItem(Graphics.FieldTriangle(polygon_top, self.field_data.gray_color_light, *coordinates))
        for coordinates in arrows_right_coordinates_2:
            self.addItem(Graphics.FieldTriangle(polygon_bot, self.field_data.gray_color_light, *coordinates))

        self.addLine(0, self.field_data.football_ten_yard,
                     self.field_data.football_field_width, self.field_data.football_ten_yard,
                     self.field_data.end_zone_center_lines_style)  # end zone line top
        self.addLine(0, self.field_data.football_field_length - self.field_data.football_ten_yard,
                     self.field_data.football_field_width, self.field_data.football_field_length - self.field_data.football_ten_yard,
                     self.field_data.end_zone_center_lines_style)  # end zone line bot
        self.addLine(0, self.field_data.football_field_length_center,
                     self.field_data.football_field_width, self.field_data.football_field_length_center,
                     self.field_data.end_zone_center_lines_style)  # field center line

        for j in range(2 * self.field_data.football_ten_yard,
                       self.field_data.football_field_length,
                       self.field_data.football_field_length_center - self.field_data.football_ten_yard):  # 10 yard lines
            for i in range(0,
                           self.field_data.football_field_length_center - 2 * self.field_data.football_ten_yard,
                           self.field_data.football_ten_yard):
                self.addLine(0, j + i,
                             self.field_data.football_field_width, j + i,
                             self.field_data.ten_yard_lines_style)

        for i in range(self.field_data.football_ten_yard + self.field_data.football_five_yard,
                       self.field_data.football_field_length - self.field_data.football_ten_yard,
                       self.field_data.football_ten_yard):  # 5 yard lines + 5 yard lines hash
            self.addLine(0, i, self.field_data.football_field_width, i, self.field_data.other_lines_style)  # 5 yard lines

        for j in range(self.field_data.football_ten_yard,
                       self.field_data.football_field_length - self.field_data.football_ten_yard,
                       self.field_data.football_five_yard):  # 1 yard lines + 1 yard lines hash
            for i in range(self.field_data.football_one_yard,
                           self.field_data.football_five_yard,
                           self.field_data.football_one_yard):
                self.addLine(0, j + i,
                             self.field_data.side_one_yard_line_length, j + i,
                             self.field_data.other_lines_style)  # 1 yard lines left
                self.addLine(self.field_data.football_field_width - self.field_data.side_one_yard_line_length, j + i,
                             self.field_data.football_field_width, j + i,
                             self.field_data.other_lines_style)   # 1 yard lines right
                self.addLine(QLineF((self.field_data.football_hash_center - self.field_data.hash_line_length / 2), j + i,
                                    (self.field_data.football_hash_center + self.field_data.hash_line_length / 2), j + i),
                             self.field_data.other_lines_style)  # 1 yard lines left hash
                self.addLine(QLineF(self.field_data.football_field_width - (self.field_data.football_hash_center - self.field_data.hash_line_length / 2), j + i,
                                    (self.field_data.football_field_width - (self.field_data.football_hash_center + self.field_data.hash_line_length / 2)), j + i),
                             self.field_data.other_lines_style)   # 1 yard lines right hash

        self.addLine(QLineF(self.field_data.football_field_width / 2 - self.field_data.hash_line_length / 2,
                            self.field_data.football_ten_yard + 3 * self.field_data.football_one_yard,
                            self.field_data.football_field_width / 2 + self.field_data.hash_line_length / 2,
                            self.field_data.football_ten_yard + 3 * self.field_data.football_one_yard),
                     self.field_data.other_lines_style)  # conversion line top
        self.addLine(QLineF(self.field_data.football_field_width / 2 - self.field_data.hash_line_length / 2,
                            self.field_data.football_field_length - (self.field_data.football_ten_yard + 3 * self.field_data.football_one_yard),
                            self.field_data.football_field_width / 2 + self.field_data.hash_line_length / 2,
                            self.field_data.football_field_length - (self.field_data.football_ten_yard + 3 * self.field_data.football_one_yard)),
                     self.field_data.other_lines_style)  # conversion line bot

        self.addRect(0, 0, self.field_data.football_field_width, self.field_data.football_field_length, self.field_data.border_line_style)  # border

    def draw_flag_field(self):
        '''Отрисовка всего поля для флаг футбола размерами 70 ярдов на 25 ярдов.
        Пропорция length / width должна быть 700 / 250'''
        # Установка размеров текущего поля, необходимо для проверки границ поля при рисовании действий игроков
        self.current_field_border = [self.field_data.flag_field_width, self.field_data.flag_field_length]
        self.setSceneRect(0, 0, self.field_data.flag_field_width, self.field_data.flag_field_length)
        self.addRect(QRectF(0, 0, self.field_data.flag_field_width, self.field_data.flag_field_length), QPen(Qt.white), QBrush(QColor(Qt.white)))
        # Отрисовка номеров
        numbers_left = (('10', 90, self.field_data.gray_color_light, 6 * self.field_data.flag_width_one_yard),
                        ('20', 90, self.field_data.gray_color_light, 6 * self.field_data.flag_width_one_yard),
                        ('20', 90, self.field_data.gray_color_light, 6 * self.field_data.flag_width_one_yard),
                        ('10', 90, self.field_data.gray_color_light, 6 * self.field_data.flag_width_one_yard),)
        numbers_right = (('10', -90, self.field_data.gray_color_light, 19 * self.field_data.flag_width_one_yard),
                         ('20', -90, self.field_data.gray_color_light, 19 * self.field_data.flag_width_one_yard),
                         ('20', -90, self.field_data.gray_color_light, 19 * self.field_data.flag_width_one_yard),
                         ('10', -90, self.field_data.gray_color_light, 19 * self.field_data.flag_width_one_yard),)
        numbers_left_y = [18.5 * self.field_data.flag_one_yard + i * self.field_data.flag_ten_yard for i in range(4)]
        numbers_right_y = [21.5 * self.field_data.flag_one_yard + i * self.field_data.flag_ten_yard for i in range(4)]
        for i, number in enumerate(numbers_left):
            self.addItem(Graphics.FieldNumber(*number, numbers_left_y[i]))
        for i, number in enumerate(numbers_right):
            self.addItem(Graphics.FieldNumber(*number, numbers_right_y[i]))
        # Отрисовка стрелок около номеров
        polygon_top = QPolygonF([QPointF(5, 0), QPointF(0, 10), QPointF(10, 10)])
        polygon_bot = QPolygonF([QPointF(5, 10), QPointF(0, 0), QPointF(10, 0)])
        arrows_left_coordinates_1 = [[4 * self.field_data.flag_width_one_yard, 18 * self.field_data.flag_one_yard + i * self.field_data.flag_ten_yard] for i in range(2)]
        arrows_left_coordinates_2 = [[4 * self.field_data.flag_width_one_yard, 11.5 * self.field_data.flag_one_yard + i * self.field_data.flag_ten_yard] for i in range(3, 5)]
        arrows_right_coordinates_1 = [[20.5 * self.field_data.flag_width_one_yard, 18 * self.field_data.flag_one_yard + i * self.field_data.flag_ten_yard] for i in range(2)]
        arrows_right_coordinates_2 = [[20.5 * self.field_data.flag_width_one_yard, 11.5 * self.field_data.flag_one_yard + i * self.field_data.flag_ten_yard] for i in range(3, 5)]
        for coordinates in arrows_left_coordinates_1:
            self.addItem(Graphics.FieldTriangle(polygon_top, self.field_data.gray_color_light, *coordinates))
        for coordinates in arrows_left_coordinates_2:
            self.addItem(Graphics.FieldTriangle(polygon_bot, self.field_data.gray_color_light, *coordinates))
        for coordinates in arrows_right_coordinates_1:
            self.addItem(Graphics.FieldTriangle(polygon_top, self.field_data.gray_color_light, *coordinates))
        for coordinates in arrows_right_coordinates_2:
            self.addItem(Graphics.FieldTriangle(polygon_bot, self.field_data.gray_color_light, *coordinates))

        self.addLine(0, self.field_data.flag_field_center, self.field_data.flag_field_width, self.field_data.flag_field_center, self.field_data.ten_yard_lines_style)  # center line
        self.addLine(0, self.field_data.flag_ten_yard, self.field_data.flag_field_width, self.field_data.flag_ten_yard, self.field_data.ten_yard_lines_style)  # end zone top line
        self.addLine(0, self.field_data.flag_field_length - self.field_data.flag_ten_yard, self.field_data.flag_field_width, self.field_data.flag_field_length - self.field_data.flag_ten_yard, self.field_data.ten_yard_lines_style)  # end zone bot line

        for j in range(self.field_data.flag_ten_yard, self.field_data.flag_field_length - self.field_data.flag_ten_yard, self.field_data.flag_field_center - self.field_data.flag_ten_yard):  # 5 yard lines
            for i in range(self.field_data.flag_five_yard, self.field_data.flag_field_center - self.field_data.flag_ten_yard, self.field_data.flag_five_yard):
                self.addLine(0, j + i, self.field_data.flag_field_width, j + i, self.field_data.other_lines_style)

        for j in range(self.field_data.flag_ten_yard, self.field_data.flag_field_length - self.field_data.flag_ten_yard, self.field_data.flag_five_yard):  # 1 yard lines + 1 yard lines hash
            for i in range(self.field_data.flag_one_yard, self.field_data.flag_five_yard, self.field_data.flag_one_yard):
                self.addLine(0, j + i, self.field_data.side_one_yard_line_length, j + i, self.field_data.other_lines_style)  # 1 yard lines left
                self.addLine(self.field_data.flag_field_width - self.field_data.side_one_yard_line_length, j + i, self.field_data.flag_field_width, j + i, self.field_data.other_lines_style)   # 1 yard lines right
                self.addLine(QLineF((self.field_data.flag_hash_center - self.field_data.hash_line_length / 2), j + i, (self.field_data.flag_hash_center + self.field_data.hash_line_length / 2), j + i), self.field_data.other_lines_style)  # 1 yard lines hash

        self.addRect(0, 0, self.field_data.flag_field_width, self.field_data.flag_field_length, self.field_data.border_line_style)  # border