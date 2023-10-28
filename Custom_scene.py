from math import acos, degrees, radians, sqrt, cos, sin
from PyQt5.Qt import *
from PyQt5.QtCore import Qt
from Item_line_action import ActionLine
from Item_rect import Rect
from Item_ellipse import Ellipse
from Item_final_action_arrow import FinalActionArrow
from Item_final_action_block import FinalActionBlock
from Item_field_triangle import FieldTriangle
from Item_field_number import FieldNumber
from ProxyLabel import ProxyWidget


class Field(QGraphicsScene):
    labelDoubleClicked = pyqtSignal(object)
    labelEditingFinished = pyqtSignal(object)
    modeChanged = pyqtSignal(str)

    def __init__(self, main_window):
        super().__init__()
        # football field settings
        self.football_field_length = int(1200)
        self.football_field_width = int(534)
        self.football_field_length_center = int(self.football_field_length / 2)
        self.football_hash_center = self.football_field_width / 2.65
        self.side_five_yard_line_length = 20
        self.football_ten_yard = int(self.football_field_length / 12)
        self.football_five_yard = int(self.football_field_length / 24)
        self.football_one_yard = int(self.football_field_length / 120)
        self.football_width_one_yard = self.football_field_width / 53
        # flag-football settings
        self.flag_field_length = int(1400)
        self.flag_field_width = int(508)
        self.flag_ten_yard = int(self.flag_field_length / 7)
        self.flag_five_yard = int(self.flag_field_length / 14)
        self.flag_one_yard = int(self.flag_field_length / 70)
        self.flag_field_center = int(self.flag_field_length / 2)
        self.flag_hash_center = self.flag_field_width / 2
        self.flag_width_one_yard = self.flag_field_width / 25
        # both field settings
        self.border_width = 4
        self.black_color = (0, 0, 0, 255)
        self.gray_color_light = (228, 228, 228, 255)
        self.gray_color_dark = (140, 140, 140, 255)
        self.line_width_ten_yard_lines = 3
        self.line_width_other = 2
        self.ten_yard_lines_style = QPen(QColor(*self.gray_color_dark), self.line_width_other)
        self.end_zone_center_lines_style = QPen(QColor(*self.black_color), self.line_width_ten_yard_lines)
        self.border_line_style = QPen(QColor(*self.black_color), self.border_width)
        # self.border_line_style = QPen(QColor(Qt.red), self.border_width)
        self.other_lines_style = QPen(QColor(*self.gray_color_light), self.line_width_other)
        self.hash_line_length = 10
        self.side_one_yard_line_length = 14

        self.current_field_border = None  # Границы текущего поля, используются при проверке попадания event внутрь поля при рисовании

        self.main_window = main_window

        self.first_team_placed = None
        self.first_team_players = []
        self.additional_offence_player = None
        self.second_team_placed = None
        self.second_team_players = []

        self.config = {
            # Drawing options.
            'line_thickness': 4,
            'pen_style': Qt.PenStyle.SolidLine,
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
        self.start_pos = None  # Коардинаты начала рисования действий фигур и тд
        self.last_start_pos = None  # Коардинаты предыдущей стартовой точки. Используется при завершении рисования действия, для вычисления угла поворота полигона стрелки маршрута или линии блока
        self.current_line = None  # Текущая линия действия
        self.current_action_lines = []  # Список текущих действий при данной операции рисования
        self.action_number_temp = None  # Временный номер рисуемого действия. В него записывается номер кликнутого маршрута,
        # при рисовании опционных маршрутов или дайствия после моушена

        self.figures = []  # Список фигур расположенных на сцене
        # self.finish_pos = None
        self.current_figure = None  # Рисуемая в данный момент фигура

        self.labels = []  # Список надписей расположенных на сцене
        self.current_label = None  # Редактируемая в данный момент надпись

        self.pencil = []  # Список всех линий рисунка карандаша

        self.mode = 'move'

    def set_mode(self, mode):
        '''Установка мода сцены'''
        if self.painting:
            if self.mode == 'route' or self.mode == 'block':
                action_finish = self.get_action_finish(self.last_start_pos, self.start_pos)  ################
                self.addItem(action_finish)
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
        # self.ungrab_unselect_items()
        # self.action_number_temp = None
        # self.current_figure = None
        self.mode = mode
        if self.mode == 'motion':
            self.config['pen_style'] = Qt.PenStyle.DashLine
        else:
            self.config['pen_style'] = Qt.PenStyle.SolidLine
        # self.set_players_flags()
        self.modeChanged.emit(self.mode)
        self.update()

    def set_config(self, key, value):
        '''Установка конфига цвета, толщины линий, размера текста и тд.'''
        self.config[key] = value

    # def ungrab_unselect_items(self):
    #     for item in self.selectedItems():
    #         item.setSelected(False)
    #     try:
    #         self.mouseGrabberItem().ungrabMouse()
    #     except AttributeError:
    #         pass

    def mousePressEvent(self, event):  # Обработка нажатия кнопки мыши и перенаправление на другие методы в зависимости от mode
        if self.mode == 'move':
            super().mousePressEvent(event)
        elif self.mode == 'route' or self.mode == 'block' or self.mode == 'motion':
            if self.allow_painting:
                self.action_mousePressEvent(event)
            else:  # Это условие для выбора игрока от которого будут рисоваться действия, и установки флага разрешения рисования
                super().mousePressEvent(event)
        elif self.mode == 'erase':
            super().mousePressEvent(event)
        elif self.mode == 'rectangle' or self.mode == 'ellipse':
            self.figure_mousePressEvent(event)
        elif self.mode == 'label':
            self.label_mousePressEvent(event)
        elif self.mode == 'pencil':
            self.pencil_mousePressEvent(event)

    def mouseMoveEvent(self, event):  # Обработка движения курсора мыши и перенаправление на другие методы в зависимости от mode
        if self.mode == 'move':
            super().mouseMoveEvent(event)
        elif self.mode == 'route' or self.mode == 'block' or self.mode == 'motion':
            if self.allow_painting:
                self.action_mouseMoveEvent(event)
            # else:
            #     super().mouseMoveEvent(event)
        elif self.mode == 'erase':
            super().mouseMoveEvent(event)
        elif self.mode == 'rectangle' or self.mode == 'ellipse':
            self.figure_mouseMoveEvent(event)
        elif self.mode == 'pencil':
            self.pencil_mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):  # Обработка отпускания кнопки мыши и перенаправление на другие методы в зависимости от mode
        if self.mode == 'move':
            super().mouseReleaseEvent(event)
        elif self.mode == 'route' or self.mode == 'block' or self.mode == 'motion':
            if self.allow_painting:
                self.action_mouseReleaseEvent(event)
            # else:
            #     super().mouseReleaseEvent(event)
        elif self.mode == 'rectangle' or self.mode == 'ellipse':
            self.figure_mouseReleaseEvent(event)
        elif self.mode == 'pencil':
            self.pencil_mouseReleaseEvent(event)

    def action_mousePressEvent(self, event):  # Рисование действий игроков
        if not self.painting and event.button() == Qt.LeftButton:
            if self.check_field_border(event):
                if self.player_center_pos:
                    self.get_start_pos(self.player_center_pos, event.scenePos())
                action_line = ActionLine(QLineF(self.start_pos, event.scenePos()),
                                         QPen(QColor(self.config['color']), self.config['line_thickness'], self.config['pen_style'], Qt.RoundCap),
                                         self.current_player, self.mode)
                self.addItem(action_line)
                self.current_line = action_line
                self.painting = True
                self.mouse_pressed_painting = True
        elif self.painting and not self.current_line and event.button() == Qt.LeftButton:
            if self.check_field_border(event):
                action_line = ActionLine(QLineF(self.start_pos, event.scenePos()),
                                         QPen(QColor(self.config['color']), self.config['line_thickness'], self.config['pen_style'], Qt.RoundCap),
                                         self.current_player, self.mode)
                self.addItem(action_line)
                self.current_line = action_line
                self.mouse_pressed_painting = True
        # elif self.painting and self.current_line and event.button() == Qt.LeftButton:
        #     if self.check_field_border(event):
        #         self.mouse_pressed_painting = True
        #         self.current_line.setLine(QLineF(self.start_pos, event.scenePos()))
        elif self.painting and event.button() == Qt.RightButton and not self.mouse_pressed_painting:
            if self.mode == 'route' or self.mode == 'block':
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
            self.current_player.ungrabMouse()
            self.current_player = None
            self.current_line = None
            self.start_pos = None
            self.last_start_pos = None
            self.painting = False
            self.allow_painting = False
            # self.ungrab_unselect_items()
            self.update()

    def action_mouseMoveEvent(self, event):  # Рисование действий игроков
        if self.current_line:
            if self.player_center_pos:
                self.get_start_pos(self.player_center_pos, event.scenePos())
            if self.check_field_border(event):
                self.current_line.setLine(QLineF(self.start_pos, event.scenePos()))
            else:
                self.current_line.setLine(QLineF(self.start_pos, self.start_pos))

    def action_mouseReleaseEvent(self, event):  # Рисование действий игроков
        if self.current_line and event.button() == Qt.LeftButton:
            if self.check_field_border(event):
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
        angle = self.get_angle(start_pos, finish_pos)
        r = self.current_player.w / 2
        x = cos(radians(angle)) * r
        y = sin(radians(angle)) * r
        self.start_pos = QPointF(start_pos.x() + x, start_pos.y() - y)

    def get_action_finish(self, start_pos, finish_pos):
        '''Получение финала (стрелка для маршрута и линия для блока) действия игрока'''
        angle = self.get_angle(start_pos, finish_pos)
        if self.mode == 'route':
            arrow = FinalActionArrow(angle, self.start_pos,
                            QPen(QColor(self.config['color']), self.config['line_thickness'],
                                 Qt.SolidLine, cap=Qt.RoundCap, join=Qt.RoundJoin),
                            self.current_player, self.mode)
            return arrow
        elif self.mode == 'block':
            line = FinalActionBlock(angle, self.start_pos,
                              QPen(QColor(self.config['color']), self.config['line_thickness'],
                                   Qt.SolidLine, cap=Qt.RoundCap, join=Qt.RoundJoin),
                              self.current_player, self.mode)
            return line

    def get_angle(self, start_pos, finish_pos):
        '''Получение угла наклона линии, начало которой-start_pos, конец-finish_pos.
        метод используется при отрисовке финала действия игрока(маршрут или блок)
        и при расчёте начальной точки рисования действия, находящейся на границе игрока (данная точка необходима
        для того, чтобы отображение маршрута не сливалось с буквами обозначающими игроков защиты'''
        x1, y1 = start_pos.x(), start_pos.y()
        x2, y2 = finish_pos.x(), finish_pos.y()
        a = y2 - y1
        c = x2 - x1
        b = sqrt(a ** 2 + c ** 2)
        angle = 0
        if a == 0 and b == c:
            angle = 0
        elif c == 0 and -a == b:
            angle = 90
        elif a == 0 and b == -c:
            angle = 180
        elif c == 0 and a == b:
            angle = 270
        elif a < 0 and b > 0:
            angle = degrees(acos((b ** 2 + c ** 2 - a ** 2) / (2.0 * b * c)))
        else:
            angle = 360 - degrees(acos((b ** 2 + c ** 2 - a ** 2) / (2.0 * b * c)))
        return angle

    def figure_mousePressEvent(self, event):  # Рисование фигур
        if not self.painting and event.button() == Qt.LeftButton:
            if self.check_field_border(event):
                self.start_pos = event.scenePos()
                if self.mode == 'rectangle':
                    figure = Rect(QRectF(self.start_pos, event.scenePos()),
                                   QPen(QColor(self.config['color']), self.config['line_thickness'],
                                        self.config['pen_style']))
                elif self.mode == 'ellipse':
                    figure = Ellipse(QRectF(self.start_pos, event.scenePos()),
                                      QPen(QColor(self.config['color']), self.config['line_thickness'],
                                           self.config['pen_style']))
                self.addItem(figure)
                self.current_figure = figure
                self.painting = True
        elif self.painting and event.button() == Qt.LeftButton and self.current_figure:
            if self.check_field_border(event):
                self.current_figure.setRect(QRectF(self.start_pos, event.scenePos()))

    def figure_mouseMoveEvent(self, event):  # Рисование фигур
        if self.painting and self.current_figure:
            if self.check_field_border(event):
                self.current_figure.setRect(QRectF(self.start_pos, event.scenePos()))
            else:
                self.current_figure.setRect(QRectF(self.start_pos, self.start_pos))
            self.update()

    def figure_mouseReleaseEvent(self, event):  # Рисование фигур
        if self.painting and self.current_figure:
            if self.check_field_border(event):
                finish_pos = event.scenePos()
                if event.scenePos().x() < self.start_pos.x():  # так сделано для того чтобы фигуры нарисованные обратным способом нормально прокликивались
                    finish_pos.setX(self.start_pos.x())
                    self.start_pos.setX(event.scenePos().x())
                if event.scenePos().y() < self.start_pos.y():  # так сделано для того чтобы фигуры нарисованные обратным способом нормально прокликивались
                    finish_pos.setY(self.start_pos.y())
                    self.start_pos.setY(event.scenePos().y())
                self.current_figure.setRect(QRectF(self.start_pos, finish_pos))
                self.figures.append(self.current_figure)
                self.start_pos = None
                self.current_figure = None
                self.painting = False
            else:
                self.current_figure.setRect(QRectF(self.start_pos, self.start_pos))

    def delete_figures(self):
        '''Удаление всех фигур со сцены'''
        group = self.createItemGroup(self.figures)
        self.removeItem(group)
        self.figures.clear()
        self.update()

    def label_mousePressEvent(self, event):
        '''Размещение надписи на сцене'''
        for label in self.labels:
            label.widget.clear_focus()
        font = QFont(self.config['font_type'].family())  # Так написано для того что бы не было ссылки на объект словаря self.config
        font.setPointSize(self.config['font_size'])
        font.setBold(self.config['bold'])
        font.setItalic(self.config['italic'])
        font.setUnderline(self.config['underline'])
        label = ProxyWidget(event.scenePos(), font, self.config['color'])
        label.widget.updateRequest.connect(label.widget.update_height)
        self.current_label = label.widget
        self.setFocusItem(self.current_label.proxy)
        self.current_label.grabKeyboard()
        self.addItem(label)
        self.labels.append(label) ##########################   проверить что добавляется и в списках находится
        self.set_mode('move')

    def delete_labels(self):
        '''Удаление всех надписей со сцены'''
        for label in self.labels:
            label.deleteLater()
        self.labels.clear()

    def pencil_mousePressEvent(self, event):  # Рисование карандашом
        self.start_pos = event.scenePos()

    def pencil_mouseMoveEvent(self, event):  # Рисование карандашом
        if self.start_pos:
            line = self.addLine(QLineF(self.start_pos, event.scenePos()),
                                QPen(QColor(self.config['color']), self.config['line_thickness'],
                                     Qt.SolidLine, Qt.RoundCap))
            self.pencil.append(line)
            self.start_pos = event.scenePos()
            self.update()

    def pencil_mouseReleaseEvent(self, event):  # Рисование карандашом
        self.start_pos = None

    def delete_pencil(self):
        '''Удаление всех риснуков карандаша'''
        group = self.createItemGroup(self.pencil)
        self.removeItem(group)
        self.pencil.clear()
        self.update()

    def check_field_border(self, event):
        '''Проверка границ поля (при рисовании фигур, действий и тд.)'''
        if 0 < event.scenePos().x() < self.current_field_border[0] and 0 < event.scenePos().y() < self.current_field_border[1]:
            return True
        return False

    def create_football_field_full(self):
        '''Отрисовка всего футбольного поля размерами 120 ярдов на 53 ярда. Расстояние между хэш-марками 13 ярдов.
        Пропорция length / width должна быть 1200 / 534'''
        # Установка размеров текущего поля, необходимо для проверки границ поля при рисовании действий игроков
        self.current_field_border = [self.football_field_width, self.football_field_length]
        self.addRect(QRectF(0, 0, self.football_field_width, self.football_field_length), QPen(Qt.white), QBrush(QColor(Qt.white)))
        # Отрисовка номеров
        numbers_left_1 = [[f'{i}', 90, self.gray_color_light, 14 * self.football_width_one_yard] for i in range(10, 60, 10)]
        numbers_left_2 = [[f'{i}', 90, self.gray_color_light, 14 * self.football_width_one_yard] for i in range(40, 0, -10)]
        numbers_right_1 = [[f'{i}', -90, self.gray_color_light, 40 * self.football_width_one_yard] for i in range(10, 60, 10)]
        numbers_right_2 = [[f'{i}', -90, self.gray_color_light, 40 * self.football_width_one_yard] for i in range(40, 0, -10)]
        numbers_left_y = [16.9 * self.football_one_yard + i * self.football_ten_yard for i in range(9)]
        numbers_right_y = [23 * self.football_one_yard + i * self.football_ten_yard for i in range(9)]
        # self.addRect(0, 0, self.football_field_width, self.football_field_length, QPen(Qt.transparent), QBrush(Qt.green))
        for i, number in enumerate(numbers_left_1):
            self.addItem(FieldNumber(*number, numbers_left_y[i]))
        for i, number in enumerate(numbers_left_2):
            self.addItem(FieldNumber(*number, numbers_left_y[5 + i]))
        for i, number in enumerate(numbers_right_1):
            self.addItem(FieldNumber(*number, numbers_right_y[i]))
        for i, number in enumerate(numbers_right_2):
            self.addItem(FieldNumber(*number, numbers_right_y[5 + i]))
        # Отрисовка стрелок около номеров
        polygon_top = QPolygonF([QPointF(5, 0), QPointF(0, 10), QPointF(10, 10)])
        polygon_bot = QPolygonF([QPointF(5, 10), QPointF(0, 0), QPointF(10, 0)])
        arrows_right_coordinates_1 = [[43 * self.football_width_one_yard, 16 * self.football_one_yard + i * self.football_ten_yard] for i in range(4)]
        arrows_left_coordinates_1 = [[10 * self.football_width_one_yard, 16 * self.football_one_yard + i * self.football_ten_yard] for i in range(4)]
        arrows_right_coordinates_2 = [[43 * self.football_width_one_yard, 23 * self.football_one_yard + i * self.football_ten_yard] for i in range(5, 9)]
        arrows_left_coordinates_2 = [[10 * self.football_width_one_yard, 23 * self.football_one_yard + i * self.football_ten_yard] for i in range(5, 9)]
        for coordinates in arrows_left_coordinates_1:
            self.addItem(FieldTriangle(polygon_top, self.gray_color_light, *coordinates))
        for coordinates in arrows_left_coordinates_2:
            self.addItem(FieldTriangle(polygon_bot, self.gray_color_light, *coordinates))
        for coordinates in arrows_right_coordinates_1:
            self.addItem(FieldTriangle(polygon_top, self.gray_color_light, *coordinates))
        for coordinates in arrows_right_coordinates_2:
            self.addItem(FieldTriangle(polygon_bot, self.gray_color_light, *coordinates))

        self.addLine(0, self.football_ten_yard,
                     self.football_field_width, self.football_ten_yard,
                     self.end_zone_center_lines_style)  # end zone line top
        self.addLine(0, self.football_field_length - self.football_ten_yard,
                     self.football_field_width, self.football_field_length - self.football_ten_yard,
                     self.end_zone_center_lines_style)  # end zone line bot
        self.addLine(0, self.football_field_length_center,
                     self.football_field_width, self.football_field_length_center,
                     self.end_zone_center_lines_style)  # field center line

        for j in range(2 * self.football_ten_yard,
                       self.football_field_length,
                       self.football_field_length_center - self.football_ten_yard):  # 10 yard lines
            for i in range(0,
                           self.football_field_length_center - 2 * self.football_ten_yard,
                           self.football_ten_yard):
                self.addLine(0, j + i,
                             self.football_field_width, j + i,
                             self.ten_yard_lines_style)

        for i in range(self.football_ten_yard + self.football_five_yard,
                       self.football_field_length - self.football_ten_yard,
                       self.football_ten_yard):  # 5 yard lines + 5 yard lines hash
            self.addLine(0, i, self.football_field_width, i, self.other_lines_style)  # 5 yard lines

        for j in range(self.football_ten_yard,
                       self.football_field_length - self.football_ten_yard,
                       self.football_five_yard):  # 1 yard lines + 1 yard lines hash
            for i in range(self.football_one_yard,
                           self.football_five_yard,
                           self.football_one_yard):
                self.addLine(0, j + i,
                             self.side_one_yard_line_length, j + i,
                             self.other_lines_style)  # 1 yard lines left
                self.addLine(self.football_field_width - self.side_one_yard_line_length, j + i,
                             self.football_field_width, j + i,
                             self.other_lines_style)   # 1 yard lines right
                self.addLine(QLineF((self.football_hash_center - self.hash_line_length / 2), j + i,
                                    (self.football_hash_center + self.hash_line_length / 2), j + i),
                                    self.other_lines_style)  # 1 yard lines left hash
                self.addLine(QLineF(self.football_field_width - (self.football_hash_center - self.hash_line_length / 2), j + i,
                                    (self.football_field_width - (self.football_hash_center + self.hash_line_length / 2)), j + i),
                                    self.other_lines_style)   # 1 yard lines right hash

        self.addLine(QLineF(self.football_field_width / 2 - self.hash_line_length / 2,
                            self.football_ten_yard + 3 * self.football_one_yard,
                            self.football_field_width / 2 + self.hash_line_length / 2,
                            self.football_ten_yard + 3 * self.football_one_yard),
                            self.other_lines_style)  # conversion line top
        self.addLine(QLineF(self.football_field_width / 2 - self.hash_line_length / 2,
                            self.football_field_length - (self.football_ten_yard + 3 * self.football_one_yard),
                            self.football_field_width / 2 + self.hash_line_length / 2,
                            self.football_field_length - (self.football_ten_yard + 3 * self.football_one_yard)),
                            self.other_lines_style)  # conversion line bot

        self.addRect(0, 0, self.football_field_width, self.football_field_length, self.border_line_style)  # border

    def create_flag_field_full(self):
        '''Отрисовка всего поля для флаг футбола размерами 70 ярдов на 25 ярдов.
        Пропорция length / width должна быть 700 / 250'''
        # Установка размеров текущего поля, необходимо для проверки границ поля при рисовании действий игроков
        self.current_field_border = [self.flag_field_width, self.flag_field_length]
        self.addRect(QRectF(0, 0, self.flag_field_width, self.flag_field_length), QPen(Qt.white), QBrush(QColor(Qt.white)))
        # Отрисовка номеров
        numbers_left = (('10', 90, self.gray_color_light, 6 * self.flag_width_one_yard),
                        ('20', 90, self.gray_color_light, 6 * self.flag_width_one_yard),
                        ('20', 90, self.gray_color_light, 6 * self.flag_width_one_yard),
                        ('10', 90, self.gray_color_light, 6 * self.flag_width_one_yard),)
        numbers_right = (('10', -90, self.gray_color_light, 19 * self.flag_width_one_yard),
                         ('20', -90, self.gray_color_light, 19 * self.flag_width_one_yard),
                         ('20', -90, self.gray_color_light, 19 * self.flag_width_one_yard),
                         ('10', -90, self.gray_color_light, 19 * self.flag_width_one_yard),)
        numbers_left_y = [18.5 * self.flag_one_yard + i * self.flag_ten_yard for i in range(4)]
        numbers_right_y = [21.5 * self.flag_one_yard + i * self.flag_ten_yard for i in range(4)]
        for i, number in enumerate(numbers_left):
            self.addItem(FieldNumber(*number, numbers_left_y[i]))
        for i, number in enumerate(numbers_right):
            self.addItem(FieldNumber(*number, numbers_right_y[i]))
        # Отрисовка стрелок около номеров
        polygon_top = QPolygonF([QPointF(5, 0), QPointF(0, 10), QPointF(10, 10)])
        polygon_bot = QPolygonF([QPointF(5, 10), QPointF(0, 0), QPointF(10, 0)])
        arrows_left_coordinates_1 = [[4 * self.flag_width_one_yard, 18 * self.flag_one_yard + i * self.flag_ten_yard] for i in range(2)]
        arrows_left_coordinates_2 = [[4 * self.flag_width_one_yard, 11.5 * self.flag_one_yard + i * self.flag_ten_yard] for i in range(3, 5)]
        arrows_right_coordinates_1 = [[20.5 * self.flag_width_one_yard, 18 * self.flag_one_yard + i * self.flag_ten_yard] for i in range(2)]
        arrows_right_coordinates_2 = [[20.5 * self.flag_width_one_yard, 11.5 * self.flag_one_yard + i * self.flag_ten_yard] for i in range(3, 5)]
        for coordinates in arrows_left_coordinates_1:
            self.addItem(FieldTriangle(polygon_top, self.gray_color_light, *coordinates))
        for coordinates in arrows_left_coordinates_2:
            self.addItem(FieldTriangle(polygon_bot, self.gray_color_light, *coordinates))
        for coordinates in arrows_right_coordinates_1:
            self.addItem(FieldTriangle(polygon_top, self.gray_color_light, *coordinates))
        for coordinates in arrows_right_coordinates_2:
            self.addItem(FieldTriangle(polygon_bot, self.gray_color_light, *coordinates))

        self.addLine(0, self.flag_field_center, self.flag_field_width, self.flag_field_center, self.ten_yard_lines_style)  # center line
        self.addLine(0, self.flag_ten_yard, self.flag_field_width, self.flag_ten_yard, self.ten_yard_lines_style)  # end zone top line
        self.addLine(0, self.flag_field_length - self.flag_ten_yard, self.flag_field_width, self.flag_field_length - self.flag_ten_yard, self.ten_yard_lines_style)  # end zone bot line

        for j in range(self.flag_ten_yard, self.flag_field_length - self.flag_ten_yard, self.flag_field_center - self.flag_ten_yard):  # 5 yard lines
            for i in range(self.flag_five_yard, self.flag_field_center - self.flag_ten_yard, self.flag_five_yard):
                self.addLine(0, j + i, self.flag_field_width, j + i, self.other_lines_style)

        for j in range(self.flag_ten_yard, self.flag_field_length - self.flag_ten_yard, self.flag_five_yard):  # 1 yard lines + 1 yard lines hash
            for i in range(self.flag_one_yard, self.flag_five_yard, self.flag_one_yard):
                self.addLine(0, j + i, self.side_one_yard_line_length, j + i, self.other_lines_style)  # 1 yard lines left
                self.addLine(self.flag_field_width - self.side_one_yard_line_length, j + i, self.flag_field_width, j + i, self.other_lines_style)   # 1 yard lines right
                self.addLine(QLineF((self.flag_hash_center - self.hash_line_length / 2), j + i, (self.flag_hash_center + self.hash_line_length / 2), j + i), self.other_lines_style)  # 1 yard lines hash

        self.addRect(0, 0, self.flag_field_width, self.flag_field_length, self.border_line_style)  # border