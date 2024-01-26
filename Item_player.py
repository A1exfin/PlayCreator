from PySide6.QtWidgets import QGraphicsItem, QFileDialog
from PySide6.QtGui import QColor, QLinearGradient, QPen, QPainter, QFont, QPolygonF, QBrush
from PySide6.QtCore import QPointF, QRectF, QLineF, Qt
from Dialog_windows import DialogFirstTeamPlayerSettings, DialogSecondTeamPlayerSettings


class Player(QGraphicsItem):
    '''Класс для отрисовки игроков'''
    width = 20
    height = 20
    border_width = 2

    def __init__(self, team: str, position: str, x: int | float, y: int | float, current_action_number: int = 0):
        super().__init__()
        self.team = team
        self.position = position
        self.actions = {}
        self.current_action_number = current_action_number + 1
        self.start_pos = None
        self.object_name = f'{team}_player_{position}'
        self.hover = False
        self.setZValue(1)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setPos(x, y)

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def mousePressEvent(self, event):
        # print(f'{self.position = }, {self.text = }')
        # print(f'{self.actions = }')
        self.setZValue(20)
        if self.scene().mode == 'move':
            self.start_pos = event.scenePos()
            super().mousePressEvent(event)
            self.setSelected(True)
        elif (self.scene().mode == 'route' or self.scene().mode == 'block' or self.scene().mode == 'motion')\
                and not self.scene().allow_painting and event.button() == Qt.LeftButton:
            self.setSelected(True)
            self.scene().allow_painting = True
            self.scene().current_player = self
            self.scene().player_center_pos = self.get_start_pos_for_action()
        elif event.button() == Qt.RightButton:  # Для того чтобы маршрут не рисовался от игрока по которому кликнули правой кнопкой
            self.ungrabMouse()

    def mouseMoveEvent(self, event):
        self.delete_actions()
        if self.scene().mode == 'move':
            if self.start_pos:
                delta_x = event.scenePos().x() - self.start_pos.x()
                delta_y = event.scenePos().y() - self.start_pos.y()
                self.moveBy(delta_x, delta_y)
                self.start_pos = QPointF(event.scenePos())
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.setZValue(1)
        if self.scene().mode == 'move':
            self.start_pos = None
            super().mouseReleaseEvent(event)
            self.setSelected(False)

    def hoverEnterEvent(self, event):
        if self.scene().mode == 'move' or self.scene().mode == 'route' or\
                self.scene().mode == 'block' or self.scene().mode == 'motion':
            self.hover = True
        # super().hoverEnterEvent(event)

    def hoverMoveEvent(self, event):
        if self.scene().mode == 'move' or self.scene().mode == 'route' or\
                self.scene().mode == 'block' or self.scene().mode == 'motion':
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

    def __init__(self, team: str, position: str, text_color: str, fill_color: str, fill_type: str, x: int | float, y: int | float):
        super().__init__(team, position, x, y)
        if team == 'offence' or team == 'offence_add':
            self.text = position
        else:
            self.text = ''
        self.gradient = None
        self.fill_type = fill_type
        self.fill_color = fill_color
        self.text_color = text_color
        self.set_linear_gradient(self.fill_type)

    def paint(self, painter, option, widget=None):
        self.rect = self.boundingRect().adjusted(self.border_width, self.border_width, -self.border_width, -self.border_width)
        if False:
            painter = QPainter()
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
        self.scene().update()

    # def mousePressEvent(self, event):
    #     super().mousePressEvent(event)
    #     print(f'{self.position = }, {self.text = }')

    def mouseDoubleClickEvent(self, event):
        '''обязательно переопределить чтобы не срабатывал двойной клик за пределами сцены,
        который считается кликом по игроку (не знаю почему так работает)'''
        self.ungrabMouse()
        if self.scene().mode == 'move':
            dialog = DialogFirstTeamPlayerSettings(self.scene().main_window.dialog_windows_text_color, self.position, self.text,
                                                   self.fill_color, self.text_color, self.fill_type,
                                                   parent=self.scene().main_window)
            result = dialog.exec()
            if result:
                self.text = dialog.player_text
                self.fill_color = dialog.player_color
                self.text_color = dialog.player_text_color
                self.fill_type = dialog.button_group_fill_symbol_type.checkedButton().objectName()
                self.set_linear_gradient(dialog.button_group_fill_symbol_type.checkedButton().objectName())

    def set_linear_gradient(self, fill):
        if fill == 'white':
            self.gradient = QLinearGradient()
            self.gradient.setStart(0, 0)
            self.gradient.setFinalStop(20, 0)
            self.gradient.setColorAt(0, QColor(f'#afffffff'))
        elif fill == 'full':
            self.gradient = QLinearGradient()
            self.gradient.setStart(0, 0)
            self.gradient.setFinalStop(20, 0)
            self.gradient.setColorAt(0, QColor(f'#9f{self.fill_color[1:]}'))
        elif fill == 'left':
            self.gradient = QLinearGradient()
            self.gradient.setStart(10, 0)
            self.gradient.setFinalStop(10.001, 0)
            self.gradient.setColorAt(0, QColor(f'#9f{self.fill_color[1:]}'))
            self.gradient.setColorAt(1, QColor('#afffffff'))
        elif fill == 'right':
            self.gradient = QLinearGradient()
            self.gradient.setStart(10, 0)
            self.gradient.setFinalStop(10.001, 0)
            self.gradient.setColorAt(0, QColor('#afffffff'))
            self.gradient.setColorAt(1, QColor(f'#af{self.fill_color[1:]}'))
        elif fill == 'mid':
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

    def __init__(self, team: str, position: str, text_color: str, border_color: str, symbol: str, x: int | float, y: int | float):
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

    def paint(self, painter, option, widget=None):
        self.rect = self.boundingRect().adjusted(self.border_width, self.border_width, -self.border_width, -self.border_width)
        if False:
            painter = QPainter()
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        painter.setBrush(QBrush(QColor('#bfffffff')))
        if self.symbol == 'letter':
            painter.setFont(self.font_letter_symbol)
        elif self.symbol == 'triangle_top' or self.symbol == 'triangle_bot':
            painter.setFont(self.font_triangle_symbol)

        if self.isSelected():
            painter.setPen(QPen(QColor(Qt.red), self.border_width, s=Qt.DotLine, c=Qt.RoundCap, j=Qt.RoundJoin))
            if self.symbol == 'letter':
                painter.drawEllipse(self.rect)
        elif self.hover:
            painter.setPen(QPen(QColor(self.border_color), self.border_width, s=Qt.DotLine, c=Qt.RoundCap, j=Qt.RoundJoin))
            if self.symbol == 'letter':
                painter.drawEllipse(self.rect)
        else:
            painter.setPen(QPen(QColor(self.border_color), self.border_width, s=Qt.SolidLine, c=Qt.RoundCap, j=Qt.RoundJoin))
        if self.symbol == 'letter':
            if (self.text == '' or self.text == ' ') and not (self.hover or self.isSelected()):
                painter.setPen(QPen(QColor(self.border_color), self.border_width, s=Qt.DotLine, c=Qt.RoundCap, j=Qt.RoundJoin))
                painter.drawEllipse(self.rect)
            else:
                painter.setPen(QPen(QColor(self.text_color)))
                painter.drawText(self.rect, Qt.AlignCenter, self.text)
        elif self.symbol == 'x':
            painter.drawLines([self.line1, self.line2])
        elif self.symbol == 'triangle_bot':
            painter.drawPolygon(QPolygonF(self.poligon_bot))
            painter.setPen(QPen(QColor(self.text_color)))
            painter.drawText(QRectF(0, - 3, self.width, self.height + 3), Qt.AlignCenter, self.text)
        elif self.symbol == 'triangle_top':
            painter.drawPolygon(QPolygonF(self.poligon_top))
            painter.setPen(QPen(QColor(self.text_color)))
            painter.drawText(QRectF(0, 4, self.width, self.height - 4), Qt.AlignCenter, self.text)
        self.scene().update()

    def mouseDoubleClickEvent(self, event):
        '''обязательно переопределить чтобы не срабатывал двойной клик за пределами сцены,
        который считается кликом по игроку (не знаю почему так работает)'''
        self.ungrabMouse()
        if self.scene().mode == 'move':
            dialog = DialogSecondTeamPlayerSettings(self.scene().main_window.dialog_windows_text_color, self.text,
                                                    self.text_color, self.border_color, self.symbol,
                                                    parent=self.scene().main_window)
            result = dialog.exec()
            if result:
                if dialog.player_symbol == 'letter':
                    self.text = dialog.player_text
                    self.text_color = dialog.player_text_color
                    self.symbol = dialog.player_symbol
                elif dialog.player_symbol == 'x':
                    self.border_color = dialog.player_color
                    self.symbol = dialog.player_symbol
                else:
                    self.text = dialog.player_text
                    self.border_color = dialog.player_color
                    self.text_color = dialog.player_text_color
                    self.symbol = dialog.player_symbol

    # def set_symbol(self, symbol: str):
    #     self.symbol = symbol
    #     if symbol == 'letter':
    #         self.width = self.height = 24
    #     elif symbol == 'x':
    #         self.width = self.height = 24
    #     elif self.symbol == 'triangle_bot':
    #         self.width = self.height = 16
    #     elif self.symbol == 'triangle_top':
    #         self.width = self.height = 16