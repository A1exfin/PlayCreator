from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtGui import QColor, QLinearGradient, QPen, QPainter, QFont, QPolygonF, QBrush
from PySide6.QtCore import QPointF, QRectF, QLineF, Qt
from Dialog_windows import DialogFirstTeamPlayerSettings, DialogSecondTeamPlayerSettings
from Enums import TeamType, FillType, SymbolType, Modes
import Graphics
from DB_offline.models import PlayerORM

__all__ = ['Player', 'FirstTeamPlayer', 'SecondTeamPlayer']


class Player(QGraphicsItem):
    '''Класс для отрисовки игроков'''
    width = 20
    height = 20
    border_width = 2

    def __init__(self, x: float, y: float, team_type: TeamType, player_position: str, current_action_number: int,
                 player_id_pk: int, scheme_id_fk: int):
        super().__init__()
        self.player_id_pk = player_id_pk
        self.scheme_id_fk = scheme_id_fk
        self.team_type = team_type
        self.player_position = player_position
        self.actions = {}
        self.deleted_action_parts = []
        self.current_action_number = current_action_number
        self.start_pos = None
        self.object_name = f'{team_type.name}_player_{player_position}'
        self.hover = False
        self.setZValue(2)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setPos(x, y)
        self.rect = self.boundingRect().adjusted(self.border_width, self.border_width, -self.border_width, -self.border_width)

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def mousePressEvent(self, event):
        # print(self)
        self.setZValue(20)
        if self.scene().mode == Modes.move and event.button() == Qt.LeftButton:
            self.start_pos = event.scenePos()
            super().mousePressEvent(event)
            self.setSelected(True)
        elif (self.scene().mode == Modes.route or self.scene().mode == Modes.block or self.scene().mode == Modes.motion)\
                and not self.scene().allow_painting and event.button() == Qt.LeftButton:
            self.setSelected(True)
            self.scene().allow_painting = True
            self.scene().current_player = self
            self.scene().player_center_pos = self.get_start_pos_for_action()
        elif event.button() == Qt.RightButton:  # Для того чтобы маршрут не рисовался от игрока по которому кликнули правой кнопкой
            self.ungrabMouse()

    def mouseMoveEvent(self, event):
        self.delete_actions()
        if self.scene().mode == Modes.move:
            if self.start_pos:
                delta = event.scenePos() - self.start_pos
                if self.scene().check_field_x(self.x() + delta.x()) \
                        and self.scene().check_field_x(self.x() + self.rect.width() + delta.x()):
                    self.moveBy(delta.x(), 0)
                if self.scene().check_field_y(self.y() + delta.y())\
                        and self.scene().check_field_y(self.y() + self.rect.height() + delta.y()):
                    self.moveBy(0, delta.y())
                self.start_pos = event.scenePos()
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.setZValue(2)
        if self.scene().mode == Modes.move:
            self.start_pos = None
            super().mouseReleaseEvent(event)
            self.setSelected(False)

    def hoverEnterEvent(self, event):
        if self.scene().mode == Modes.move or self.scene().mode == Modes.route or\
                self.scene().mode == Modes.block or self.scene().mode == Modes.motion:
            self.hover = True
        # super().hoverEnterEvent(event)

    def hoverMoveEvent(self, event):
        if self.scene().mode == Modes.move or self.scene().mode == Modes.route or\
                self.scene().mode == Modes.block or self.scene().mode == Modes.motion:
            self.hover = True
        else:
            self.hover = False
        # super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event):
        self.hover = False
        # super().hoverLeaveEvent(event)

    def get_start_pos_for_action(self):
        return QPointF(self.scenePos().x() + self.width / 2, self.scenePos().y() + self.height / 2)

    def delete_actions(self):
        actions = self.actions.copy()
        for action_number in actions.keys():
            actions_lst = actions[action_number]
            for action_part in actions_lst:
                if isinstance(action_part, Graphics.ActionLine) and action_part.line_id_pk:
                    self.deleted_action_parts.append(action_part)
                elif isinstance(action_part, Graphics.FinalActionLine) and action_part.f_line_action_id_pk:
                    self.deleted_action_parts.append(action_part)
                elif isinstance(action_part, Graphics.FinalActionArrow) and action_part.f_arr_action_id_pk:
                    self.deleted_action_parts.append(action_part)
            group = self.scene().createItemGroup(actions_lst)
            self.scene().removeItem(group)
            self.actions.pop(action_number)
        del actions
        self.scene().update()

    def __eq__(self, other):
        return self.player_id_pk == other.player_id_pk if isinstance(other, PlayerORM) else super().__eq__(other)

    def __repr__(self):
        return f'\n\t<{self.__class__.__name__} (id_pk: {self.player_id_pk}; scheme_id_fk: {self.scheme_id_fk};' \
               f' team_type: {self.team_type.name}; x/y: {self.x()}/{self.y()}; position/text: {self.player_position}/{self.text};' \
               f' current_action_number: {self.current_action_number}) at {hex(id(self))} \n\t\tactions: {self.actions}\n\t\tdeleted_actions: {self.deleted_action_parts}>'

    # def __del__(self):
    #     print(f'удаление {self.object_name}')


class FirstTeamPlayer(Player):
    font = QFont('Times New Roman', 5, QFont.Bold)

    def __init__(self, team_type: TeamType, position: str, text: str, text_color: str,
                 player_color: str, fill_type: FillType, x: float, y: float,
                 current_action_number: int = 0, player_id_pk: int = None, scheme_id_fk: int = None):
        super().__init__(x, y, team_type, position, current_action_number, player_id_pk=player_id_pk, scheme_id_fk=scheme_id_fk)
        self.text = text
        self.gradient = None
        self.fill_type = fill_type
        self.player_color = player_color
        self.text_color = text_color
        self.set_linear_gradient(self.fill_type)

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        painter.setFont(self.font)
        painter.setBrush(QBrush(self.gradient))
        if self.isSelected():
            painter.setPen(QPen(QColor(Qt.red), self.border_width, s=Qt.DotLine, c=Qt.RoundCap, j=Qt.RoundJoin))
        elif self.hover:
            painter.setPen(QPen(QColor(self.player_color), self.border_width, s=Qt.DotLine, c=Qt.RoundCap, j=Qt.RoundJoin))
        else:
            painter.setPen(QPen(QColor(self.player_color), self.border_width, s=Qt.SolidLine, c=Qt.RoundCap, j=Qt.RoundJoin))
        if self.player_position == 'C':
            painter.drawRect(self.rect)
            painter.setPen(QPen(QColor(self.text_color), self.border_width))
            painter.drawText(self.rect, Qt.AlignCenter, self.text)
        else:
            painter.drawEllipse(self.rect)
            painter.setPen(QPen(QColor(self.text_color), self.border_width))
            painter.drawText(self.rect, Qt.AlignCenter, self.text)
        # self.scene().update()
        self.update()

    def mouseDoubleClickEvent(self, event):
        self.ungrabMouse()
        if self.scene().mode == Modes.move:
            dialog = DialogFirstTeamPlayerSettings(self.player_position, self.text, self.player_color, self.text_color,
                                                   self.fill_type, parent=self.scene().main_window)
            result = dialog.exec()
            if result:
                self.text = dialog.player_text
                self.player_color = dialog.player_color
                self.text_color = dialog.player_text_color
                self.fill_type = dialog.button_group_fill_symbol_type.checkedButton().fill_type
                self.set_linear_gradient(dialog.button_group_fill_symbol_type.checkedButton().fill_type)

    def set_linear_gradient(self, fill: FillType):
        if fill == FillType.white:
            self.gradient = QLinearGradient()
            self.gradient.setStart(0, 0)
            self.gradient.setFinalStop(20, 0)
            self.gradient.setColorAt(0, QColor(f'#afffffff'))
        elif fill == FillType.full:
            self.gradient = QLinearGradient()
            self.gradient.setStart(0, 0)
            self.gradient.setFinalStop(20, 0)
            self.gradient.setColorAt(0, QColor(f'#9f{self.player_color[1:]}'))
        elif fill == FillType.left:
            self.gradient = QLinearGradient()
            self.gradient.setStart(10, 0)
            self.gradient.setFinalStop(10.001, 0)
            self.gradient.setColorAt(0, QColor(f'#9f{self.player_color[1:]}'))
            self.gradient.setColorAt(1, QColor('#afffffff'))
        elif fill == FillType.right:
            self.gradient = QLinearGradient()
            self.gradient.setStart(10, 0)
            self.gradient.setFinalStop(10.001, 0)
            self.gradient.setColorAt(0, QColor('#afffffff'))
            self.gradient.setColorAt(1, QColor(f'#9f{self.player_color[1:]}'))
        elif fill == FillType.mid:
            self.gradient = QLinearGradient()
            self.gradient.setStart(0, 0)
            self.gradient.setFinalStop(20, 0)
            self.gradient.setColorAt(0, QColor('#afffffff'))
            self.gradient.setColorAt(0.355, QColor('#afffffff'))
            self.gradient.setColorAt(0.356, QColor(f'#9f{self.player_color[1:]}'))
            self.gradient.setColorAt(0.650, QColor(f'#9f{self.player_color[1:]}'))
            self.gradient.setColorAt(0.651, QColor('#afffffff'))
            self.gradient.setColorAt(1, QColor('#afffffff'))

    def return_data(self):
        return self.player_id_pk, self.scheme_id_fk, self.x(), self.y(),\
               self.team_type, self.player_position, self.current_action_number,\
               self.text, self.text_color, self.player_color, self.fill_type


class SecondTeamPlayer(Player):
    font_letter_symbol = QFont('Times New Roman', 10, QFont.Bold)
    font_triangle_symbol = QFont('Times New Roman', 5, QFont.Bold)

    def __init__(self, team_type: TeamType, position: str, text: str, text_color: str,
                 player_color: str, symbol_type: SymbolType, x: float, y: float,
                 current_action_number: int = 0, player_id_pk: int = None, scheme_id_fk: int = None):
        super().__init__(x, y, team_type, position, current_action_number=current_action_number, player_id_pk=player_id_pk, scheme_id_fk=scheme_id_fk)
        self.symbol_type = symbol_type
        self.text = text
        self.text_color = text_color
        self.player_color = player_color
        # Треугольник вершиной вверх
        self.poligon_top = (QPointF(self.width / 2, 2),  # Вершина
                            QPointF(2, self.height - 3),  # Основание левая точка
                            QPointF(self.width - 2, self.height - 3),)  # Основание правая точка
        # Треугольник вершиной вниз
        self.poligon_bot = (QPointF(self.width / 2, self.height - 2),  # Вершина
                            QPointF(2, 3),  # Основание левая точка
                            QPointF(self.width - 2, 3),)  # Основание правая точка
        # Крест
        self.line1 = QLineF(QPointF(5, 5), QPointF(self.width - 5, self.height - 5))
        self.line2 = QLineF(QPointF(self.width - 5, 5), QPointF(5, self.height - 5))

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        painter.setBrush(QBrush(QColor('#bfffffff')))
        if self.symbol_type == SymbolType.letter:
            painter.setFont(self.font_letter_symbol)
        elif self.symbol_type == SymbolType.triangle_top or self.symbol_type == SymbolType.triangle_bot:
            painter.setFont(self.font_triangle_symbol)

        if self.isSelected():
            painter.setPen(QPen(QColor(Qt.red), self.border_width, s=Qt.DotLine, c=Qt.RoundCap, j=Qt.RoundJoin))
            if self.symbol_type == SymbolType.letter:
                painter.drawEllipse(self.rect)
        elif self.hover:
            painter.setPen(QPen(QColor(self.player_color), self.border_width, s=Qt.DotLine, c=Qt.RoundCap, j=Qt.RoundJoin))
            if self.symbol_type == SymbolType.letter:
                painter.drawEllipse(self.rect)
        else:
            painter.setPen(QPen(QColor(self.player_color), self.border_width, s=Qt.SolidLine, c=Qt.RoundCap, j=Qt.RoundJoin))
        if self.symbol_type == SymbolType.letter:
            if (self.text == '' or self.text == ' ') and not (self.hover or self.isSelected()):
                painter.setPen(QPen(QColor(self.player_color), self.border_width, s=Qt.DotLine, c=Qt.RoundCap, j=Qt.RoundJoin))
                painter.drawEllipse(self.rect)
            else:
                painter.setPen(QPen(QColor(self.text_color)))
                painter.drawText(self.rect, Qt.AlignCenter, self.text)
        elif self.symbol_type == SymbolType.cross:
            painter.drawLines([self.line1, self.line2])
        elif self.symbol_type == SymbolType.triangle_bot:
            painter.drawPolygon(QPolygonF(self.poligon_bot))
            painter.setPen(QPen(QColor(self.text_color)))
            painter.drawText(QRectF(0, - 3, self.width, self.height + 3), Qt.AlignCenter, self.text)
        elif self.symbol_type == SymbolType.triangle_top:
            painter.drawPolygon(QPolygonF(self.poligon_top))
            painter.setPen(QPen(QColor(self.text_color)))
            painter.drawText(QRectF(0, 4, self.width, self.height - 4), Qt.AlignCenter, self.text)
        # self.scene().update()
        self.update()

    def mouseDoubleClickEvent(self, event):
        '''обязательно переопределить чтобы не срабатывал двойной клик за пределами сцены,
        который считается кликом по игроку (не знаю почему так работает)'''
        self.ungrabMouse()
        if self.scene().mode == Modes.move:
            dialog = DialogSecondTeamPlayerSettings(self.text, self.text_color, self.player_color, self.symbol_type,
                                                    parent=self.scene().main_window)
            result = dialog.exec()
            if result:
                if dialog.player_symbol == SymbolType.letter:
                    self.text = dialog.player_text
                    self.text_color = dialog.player_text_color
                    self.symbol_type = dialog.player_symbol
                elif dialog.player_symbol == SymbolType.cross:
                    self.player_color = dialog.player_color
                    self.symbol_type = dialog.player_symbol
                else:
                    self.text = dialog.player_text
                    self.player_color = dialog.player_color
                    self.text_color = dialog.player_text_color
                    self.symbol_type = dialog.player_symbol

    def return_data(self):
        return self.player_id_pk, self.scheme_id_fk, self.x(), self.y(), \
               self.team_type, self.player_position, self.current_action_number, \
               self.text, self.text_color, self.player_color, self.symbol_type