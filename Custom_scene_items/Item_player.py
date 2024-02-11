from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtGui import QColor, QLinearGradient, QPen, QPainter, QFont, QPolygonF, QBrush
from PySide6.QtCore import QPointF, QRectF, QLineF, Qt
from Custom_widgets.Custom_dialog_player_settings import DialogFirstTeamPlayerSettings, DialogSecondTeamPlayerSettings
from Enum_flags import TeamType, FillType, SymbolType, Modes


class Player(QGraphicsItem):
    '''Класс для отрисовки игроков'''
    width = 20
    height = 20
    border_width = 2

    def __init__(self, team: TeamType, position: str, x: int | float, y: int | float, current_action_number: int = 0):
        super().__init__()
        self.id = None
        self.team = team
        self.position = position
        self.actions = {}
        self.current_action_number = current_action_number + 1
        self.start_pos = None
        self.object_name = f'{team.name}_player_{position}'
        self.hover = False
        self.setZValue(2)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setPos(x, y)

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def mousePressEvent(self, event):
        # print(self.actions)
        # for key, lst in self.actions.items():
        #     for line in lst:
        #         print(f'\n{key}: {line.return_data()}')
        self.setZValue(20)
        if self.scene().mode == Modes.move:
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
                delta_x = event.scenePos().x() - self.start_pos.x()
                delta_y = event.scenePos().y() - self.start_pos.y()
                self.moveBy(delta_x, delta_y)
                self.start_pos = QPointF(event.scenePos())
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.setZValue(1)
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
        for action in actions.keys():
            self.scene().removeItem(self.scene().createItemGroup(self.actions[f'{action}']))
            self.actions.pop(f'{action}')
        del actions
        self.scene().update()

    # def __del__(self):
    #     print(f'удаление {self.object_name}')


class FirstTeamPlayer(Player):
    font = QFont('Times New Roman', 5, QFont.Bold)

    def __init__(self, team: TeamType, position: str, text_color: str, fill_color: str, fill_type: FillType, x: int | float, y: int | float):
        super().__init__(team, position, x, y)
        if team == TeamType.offence or team == TeamType.offence_add:
            self.text = position
        else:
            self.text = ''
        self.gradient = None
        self.fill_type = fill_type
        self.fill_color = fill_color
        self.text_color = text_color
        self.set_linear_gradient(self.fill_type)

    def paint(self, painter: QPainter, option, widget=None):
        self.rect = self.boundingRect().adjusted(self.border_width, self.border_width, -self.border_width, -self.border_width)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        painter.setFont(self.font)
        painter.setBrush(QBrush(self.gradient))
        if self.isSelected():
            painter.setPen(QPen(QColor(Qt.red), self.border_width, s=Qt.DotLine, c=Qt.RoundCap, j=Qt.RoundJoin))
        elif self.hover:
            painter.setPen(QPen(QColor(self.fill_color), self.border_width, s=Qt.DotLine, c=Qt.RoundCap, j=Qt.RoundJoin))
        else:
            painter.setPen(QPen(QColor(self.fill_color), self.border_width, s=Qt.SolidLine, c=Qt.RoundCap, j=Qt.RoundJoin))
        if self.position == 'C':
            painter.drawRect(self.rect)
            painter.setPen(QPen(QColor(self.text_color), self.border_width))
            painter.drawText(self.rect, Qt.AlignCenter, self.text)
        else:
            painter.drawEllipse(self.rect)
            painter.setPen(QPen(QColor(self.text_color), self.border_width))
            painter.drawText(self.rect, Qt.AlignCenter, self.text)
        # self.scene().update()
        self.update()

    # def mousePressEvent(self, event):
    #     super().mousePressEvent(event)
    #     print(f'{self.position = }, {self.text = }')

    def mouseDoubleClickEvent(self, event):
        '''обязательно переопределить чтобы не срабатывал двойной клик за пределами сцены,
        который считается кликом по игроку (не знаю почему так работает)'''
        self.ungrabMouse()
        if self.scene().mode == Modes.move:
            dialog = DialogFirstTeamPlayerSettings(self.scene().main_window.dialog_windows_text_color, self.position, self.text,
                                                   self.fill_color, self.text_color, self.fill_type,
                                                   parent=self.scene().main_window)
            result = dialog.exec()
            if result:
                self.text = dialog.player_text
                self.fill_color = dialog.player_color
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
            self.gradient.setColorAt(0, QColor(f'#9f{self.fill_color[1:]}'))
        elif fill == FillType.left:
            self.gradient = QLinearGradient()
            self.gradient.setStart(10, 0)
            self.gradient.setFinalStop(10.001, 0)
            self.gradient.setColorAt(0, QColor(f'#9f{self.fill_color[1:]}'))
            self.gradient.setColorAt(1, QColor('#afffffff'))
        elif fill == FillType.right:
            self.gradient = QLinearGradient()
            self.gradient.setStart(10, 0)
            self.gradient.setFinalStop(10.001, 0)
            self.gradient.setColorAt(0, QColor('#afffffff'))
            self.gradient.setColorAt(1, QColor(f'#af{self.fill_color[1:]}'))
        elif fill == FillType.mid:
            self.gradient = QLinearGradient()
            self.gradient.setStart(0, 0)
            self.gradient.setFinalStop(20, 0)
            self.gradient.setColorAt(0, QColor('#afffffff'))
            self.gradient.setColorAt(0.355, QColor('#afffffff'))
            self.gradient.setColorAt(0.356, QColor(f'#af{self.fill_color[1:]}'))
            self.gradient.setColorAt(0.650, QColor(f'#af{self.fill_color[1:]}'))
            self.gradient.setColorAt(0.651, QColor('#afffffff'))
            self.gradient.setColorAt(1, QColor('#afffffff'))


class SecondTeamPlayer(Player):
    font_letter_symbol = QFont('Times New Roman', 10, QFont.Bold)
    font_triangle_symbol = QFont('Times New Roman', 5, QFont.Bold)

    def __init__(self, team: TeamType, position: str, text_color: str, border_color: str, symbol: SymbolType, x: int | float, y: int | float):
        super().__init__(team, position, x, y)
        self.symbol = symbol
        self.text = position
        self.text_color = text_color
        self.border_color = border_color
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
        self.rect = self.boundingRect().adjusted(self.border_width, self.border_width, -self.border_width, -self.border_width)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        painter.setBrush(QBrush(QColor('#bfffffff')))
        if self.symbol == SymbolType.letter:
            painter.setFont(self.font_letter_symbol)
        elif self.symbol == SymbolType.triangle_top or self.symbol == SymbolType.triangle_bot:
            painter.setFont(self.font_triangle_symbol)

        if self.isSelected():
            painter.setPen(QPen(QColor(Qt.red), self.border_width, s=Qt.DotLine, c=Qt.RoundCap, j=Qt.RoundJoin))
            if self.symbol == SymbolType.letter:
                painter.drawEllipse(self.rect)
        elif self.hover:
            painter.setPen(QPen(QColor(self.border_color), self.border_width, s=Qt.DotLine, c=Qt.RoundCap, j=Qt.RoundJoin))
            if self.symbol == SymbolType.letter:
                painter.drawEllipse(self.rect)
        else:
            painter.setPen(QPen(QColor(self.border_color), self.border_width, s=Qt.SolidLine, c=Qt.RoundCap, j=Qt.RoundJoin))
        if self.symbol == SymbolType.letter:
            if (self.text == '' or self.text == ' ') and not (self.hover or self.isSelected()):
                painter.setPen(QPen(QColor(self.border_color), self.border_width, s=Qt.DotLine, c=Qt.RoundCap, j=Qt.RoundJoin))
                painter.drawEllipse(self.rect)
            else:
                painter.setPen(QPen(QColor(self.text_color)))
                painter.drawText(self.rect, Qt.AlignCenter, self.text)
        elif self.symbol == SymbolType.cross:
            painter.drawLines([self.line1, self.line2])
        elif self.symbol == SymbolType.triangle_bot:
            painter.drawPolygon(QPolygonF(self.poligon_bot))
            painter.setPen(QPen(QColor(self.text_color)))
            painter.drawText(QRectF(0, - 3, self.width, self.height + 3), Qt.AlignCenter, self.text)
        elif self.symbol == SymbolType.triangle_top:
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
            dialog = DialogSecondTeamPlayerSettings(self.scene().main_window.dialog_windows_text_color, self.text,
                                                    self.text_color, self.border_color, self.symbol,
                                                    parent=self.scene().main_window)
            result = dialog.exec()
            if result:
                if dialog.player_symbol == SymbolType.letter:
                    self.text = dialog.player_text
                    self.text_color = dialog.player_text_color
                    self.symbol = dialog.player_symbol
                elif dialog.player_symbol == SymbolType.cross:
                    self.border_color = dialog.player_color
                    self.symbol = dialog.player_symbol
                else:
                    self.text = dialog.player_text
                    self.border_color = dialog.player_color
                    self.text_color = dialog.player_text_color
                    self.symbol = dialog.player_symbol