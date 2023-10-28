from PyQt5.Qt import *


class ActionLine(QGraphicsLineItem):
    def __init__(self, line, pen, player, mode):
        super().__init__(line)
        self.player = player
        self.pen = pen
        self.setPen(self.pen)
        self.setAcceptHoverEvents(True)
        self.action_number = player.current_action_number
        self.action = mode
        self.hover = False
        self.object_name = f'{self.player.position}_{self.action}_{self.action_number}'

    def mousePressEvent(self, event):
        # print(self.object_name)
        # self.setSelected(False)
        self.ungrabMouse()
        if self.scene().mode == 'route' and (self.action == 'route' or self.action == 'motion') and event.button() == Qt.LeftButton:
            self.scene().allow_painting = True
            self.scene().start_pos = event.scenePos()
            self.player.setSelected(True)
            self.scene().current_player = self.player
            self.scene().action_number_temp = self.action_number
            self.scene().action_number_temp, self.player.current_action_number \
                = self.player.current_action_number, self.scene().action_number_temp
        elif self.scene().mode == 'block' and self.action == 'motion' and event.button() == Qt.LeftButton:
            self.scene().allow_painting = True
            self.scene().start_pos = event.scenePos()
            self.player.setSelected(True)
            self.scene().current_player = self.player
            self.scene().action_number_temp = self.action_number
            self.scene().action_number_temp, self.player.current_action_number \
                = self.player.current_action_number, self.scene().action_number_temp
        elif self.scene().mode == 'erase':
            group = self.scene().createItemGroup(self.player.actions[f'action_number:{self.action_number}'])
            self.scene().removeItem(group)
            self.player.actions.pop(f'action_number:{self.action_number}')

    def mouseDoubleClickEvent(self, event):
        '''обязательно переопределить чтобы не срабатывал двойной клик за пределами сцены,
        который считается кликом по линии (не знаю почему так работает)'''
        self.ungrabMouse()

    def paint(self, painter, option, widget=None):
        painter.setRenderHints(QPainter.HighQualityAntialiasing)
        # if self.hover:
        #     self.setPen(QPen(QColor(Qt.red), self.pen.width()))
        # else:
        #     self.setPen(QPen(self.pen))
        super().paint(painter, option, widget)
        self.scene().update()  # Нужно для полного удаления действия со сцены СРАЗУ после клика по линии

    # def hoverEnterEvent(self, event):
    #     for action in self.player.actions[f'action_number:{self.action_number}']:
    #         action.hover = True
    #
    # def hoverLeaveEvent(self, event):
    #     for action in self.player.actions[f'action_number:{self.action_number}']:
    #         action.hover = False