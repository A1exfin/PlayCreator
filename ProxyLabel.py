from PySide6.QtWidgets import QPlainTextEdit, QGraphicsProxyWidget
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QCursor, QPen, QBrush, QPainter, QPixmap, QColor


class TextEdit(QPlainTextEdit):
    def __init__(self, proxy, font, color):
        super().__init__()
        self.font = font
        self.proxy = proxy
        self.color = color
        self.setFont(self.font)
        # self.setTextColor(QColor(color))
        self.setStyleSheet(f'''background-color: transparent;\n
                               Border:0px dashed black;\n
                               color:{self.color};\n''')
        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setReadOnly(False)
        self.setMaximumWidth(self.proxy.max_width)
        self.setMaximumHeight(self.proxy.max_height)
        self.setMinimumWidth(self.proxy.min_width)
        self.setMinimumHeight(self.proxy.min_height)
        # self.setPlainText('123\n345\n436')

    def mouseDoubleClickEvent(self, event):
        # if self.proxy.scene().mode == 'move' and event.button() == Qt.LeftButton and not self.proxy.selected:
        if self.proxy.scene().mode == 'move' and event.button() == Qt.LeftButton and not self.keyboardGrabber():
            # self.setCursorWidth(1)
            # self.proxy.selected = True
            self.proxy.scene().current_label = self
            self.grabKeyboard()
            self.setReadOnly(False)
            self.proxy.scene().labelDoubleClicked.emit(self)
            self.update()
        # elif self.proxy.scene().mode == 'move' and event.button() == Qt.LeftButton and self.proxy.selected:
        elif self.proxy.scene().mode == 'move' and event.button() == Qt.LeftButton and self.keyboardGrabber():
            self.selectAll()
        else:
            pass

    # def mousePressEvent(self, event):
    #     if self.proxy.scene().mode == 'move':
    #         print('1')
    #         super().mousePressEvent(event)
    #     else:
    #         self.clear_focus()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and event.modifiers() == Qt.ShiftModifier:
            super().keyPressEvent(event)
        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.clear_focus()
            self.proxy.scene().labelEditingFinished.emit(self)
        else:
            super().keyPressEvent(event)
        self.update()

    def clear_focus(self):
        self.setReadOnly(True)
        self.clearFocus()
        # self.proxy.clearFocus()
        # self.proxy.scene().clearFocus()
        self.releaseKeyboard()
        self.proxy.scene().current_label = None
        # self.setCursorWidth(0)
        # self.proxy.selected = False
        self.update()

    def focusOutEvent(self, event):
        '''Завершение редактирования надписи при клике по сцене'''
        if self.proxy.scene().main_window.fontComboBox.hasFocus() \
                or self.proxy.scene().main_window.comboBox_font_size.hasFocus()\
                or self.proxy.scene().main_window.pushButton_bold.hasFocus()\
                or self.proxy.scene().main_window.pushButton_italic.hasFocus()\
                or self.proxy.scene().main_window.pushButton_underline.hasFocus()\
                or self.proxy.scene().main_window.pushButton_current_color.hasFocus()\
                or self.proxy.scene().main_window.pushButton_color_0.hasFocus()\
                or self.proxy.scene().main_window.pushButton_color_1.hasFocus()\
                or self.proxy.scene().main_window.pushButton_color_2.hasFocus()\
                or self.proxy.scene().main_window.pushButton_color_3.hasFocus()\
                or self.proxy.scene().main_window.pushButton_color_4.hasFocus()\
                or self.proxy.scene().main_window.pushButton_color_5.hasFocus()\
                or self.proxy.scene().main_window.pushButton_color_6.hasFocus()\
                or self.proxy.scene().main_window.pushButton_color_7.hasFocus()\
                or self.proxy.scene().main_window.pushButton_color_8.hasFocus()\
                or self.proxy.scene().main_window.pushButton_color_9.hasFocus()\
                or self.proxy.scene().main_window.pushButton_color_10.hasFocus()\
                or self.proxy.scene().main_window.pushButton_color_11.hasFocus():
            pass
        else:
            self.clear_focus()
            self.proxy.scene().labelEditingFinished.emit(self)
        super().focusOutEvent(event)

    def focusInEvent(self, event):
        # print('focus in')
        super().focusInEvent(event)

    def update_height(self):
        line_height = self.fontMetrics().height()
        lines_number = self.document().lineCount()
        margin = self.document().documentMargin()
        height = line_height * lines_number + 2 * (margin + 4)
        if height <= self.proxy.max_height:
            self.proxy.height = height
        elif height > self.proxy.max_height:
            self.proxy.height = self.proxy.max_height
        self.proxy.setGeometry(QRectF(self.proxy.x, self.proxy.y, self.proxy.width, self.proxy.height))
        self.proxy.update_borders_pos()


class ProxyWidget(QGraphicsProxyWidget):
    border_width = 5
    min_width = 20
    min_height = 20
    max_width = 500
    max_height = 195
    # cursor = {'left': Qt.SizeHorCursor,
    #           'right': Qt.SizeHorCursor,
    #           'move': Qt.SizeAllCursor,
    #           'edited': Qt.IBeamCursor,
    #           'erase': QCursor(QPixmap('Cursors/eraser.cur'), 0, 0)}

    def __init__(self, pos, font, color):
        super().__init__()
        self.x = int(pos.x())
        self.y = int(pos.y()) - 15
        self.width = 200
        self.height = 65
        self.widget = TextEdit(self, font, color)
        self.borders = {}
        self.cursor = {'left': Qt.SizeHorCursor,
                       'right': Qt.SizeHorCursor,
                       'move': Qt.SizeAllCursor,
                       'edited': Qt.IBeamCursor,
                       'erase': QCursor(QPixmap('Interface/Cursors/eraser.cur'), 0, 0)}
        self.setAcceptHoverEvents(True)
        self.hover = False
        # self.selected = True
        self.border_selected = None
        self.startPos = None
        self.setWidget(self.widget)
        self.setGeometry(QRectF(self.x, self.y, self.width, self.height))
        self.update_borders_pos()
        self.widget.setFocus()

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def update_borders_pos(self):
        self.borders['left'] = QRectF(self.scenePos().x(), self.scenePos().y() + self.border_width,
                                      self.border_width, self.height - 2 * self.border_width)
        self.borders['right'] = QRectF(self.scenePos().x() + self.width - self.border_width,
                                       self.scenePos().y() + self.border_width,
                                       self.border_width, self.height - 2 * self.border_width)
        QRectF(self.scenePos().x(), self.scenePos().y(),
               self.border_width, self.border_width)  # top_left
        QRectF(self.scenePos().x() + self.border_width, self.scenePos().y(),
               self.width - 2 * self.border_width, self.border_width)  # top_mid
        QRectF(self.scenePos().x() + self.width - self.border_width, self.scenePos().y(),
               self.border_width, self.border_width)  # top_right
        QRectF(self.scenePos().x(), self.scenePos().y() + self.height - self.border_width,
               self.border_width, self.border_width)  # bot_left
        QRectF(self.scenePos().x() + self.border_width, self.scenePos().y() + self.height - self.border_width,
               self.width - 2 * self.border_width, self.border_width)  # bot_mid
        QRectF(self.scenePos().x() + self.width - self.border_width, self.scenePos().y() + self.height - self.border_width,
               self.border_width, self.border_width)  # bot_right

    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        painter.setPen(QPen(Qt.transparent))
        painter.setBrush(QBrush(Qt.transparent))
        painter.setRenderHints(QPainter.Antialiasing)
        for border, rect in self.borders.items():
            painter.drawRect(QRectF(rect.x() - self.scenePos().x(), rect.y() - self.scenePos().y(), rect.width(), rect.height()))
        # if self.selected:
        if self.widget.hasFocus() and self.widget.keyboardGrabber():
            painter.setPen(QPen(Qt.red, 2, Qt.DashLine, c=Qt.RoundCap))
            painter.setBrush(QBrush(Qt.transparent))
            rec = self.boundingRect()
            painter.drawRect(rec)
        elif self.hover:
            painter.setPen(QPen(QColor('#ff990b'), 2, Qt.DashLine, c=Qt.RoundCap))
            painter.setBrush(QBrush(Qt.transparent))
            rec = self.boundingRect()
            painter.drawRect(rec)

    def check_border_under_cursor(self, point):
        for border, rect in self.borders.items():
            if rect.contains(point):
                return border
        return None

    def hoverEnterEvent(self, event):
        # print('---------------------------')
        # print(f'active {self.widget.isActiveWindow()}')
        # print(f'focus {self.widget.hasFocus()}')
        # print(f'keyGrabber {self.widget.keyboardGrabber()}')
        # print(f'label {self.widget}')
        if self.scene().mode == 'move' or self. scene().mode == 'erase':
            self.hover = True
            self.update()
            super().hoverEnterEvent(event)

    def hoverMoveEvent(self, event):
        if self.widget.keyboardGrabber() and self.scene().mode == 'move':
            border_under_cursor = self.check_border_under_cursor(event.scenePos())
            if border_under_cursor is None:
                cursor = self.cursor['edited']
            else:
                cursor = self.cursor[border_under_cursor]
        elif self.scene().mode == 'erase':
            cursor = self.cursor['erase']
        else:
            cursor = self.cursor['move']
        self.setCursor(cursor)
        self.update()
        super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event):
        if self.scene().mode == 'move' or self.scene().mode == 'erase':
            self.hover = False
            self.update()
            super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if self.scene().mode == 'erase':
            self.setCursor(Qt.ArrowCursor)  # Возврат стандартного курсора сразу после клика
            self.deleteLater()
            self.scene().labels.remove(self)
            self.scene().current_label = None
        self.border_selected = self.check_border_under_cursor(event.scenePos())
        if self.scene().mode == 'move' and not self.border_selected and event.button() == Qt.LeftButton and not self.widget.keyboardGrabber():
            self.startPos = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.border_selected and self.widget.keyboardGrabber():
            self.interactiveResize(event.scenePos())
        elif self.scene().mode == 'move' and not self.widget.keyboardGrabber():
            if self.startPos:
                delta_x = event.pos().x() - self.startPos.x()
                delta_y = event.pos().y() - self.startPos.y()
                self.x = self.pos().x() + delta_x
                self.y = self.pos().y() + delta_y
            self.setPos(QPointF(self.x, self.y))
            self.update_borders_pos()
            self.update()
        elif not self.border_selected and self.widget.keyboardGrabber():
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.scene().mode == 'move':
            self.border_selected = None
            self.startPos = None
        else:
            super().mouseReleaseEvent(event)

    def interactiveResize(self, mouse_pos):
        self.widget.blockSignals(True)  # для того что бы во время ручного изменения ширины фиксировалась высота
        self.widget.update_height()
        if self.border_selected == 'left':
            delta_x = mouse_pos.x() - self.scenePos().x()
            if delta_x < 0 and self.width >= self.max_width:
                pass
            elif delta_x > 0 and self.width <= self.min_width:
                pass
            else:
                self.x += delta_x
                self.width -= delta_x
        elif self.border_selected == 'right':
            delta_x = mouse_pos.x() - self.width - self.scenePos().x()
            if delta_x > 0 and self.width >= self.max_width:
                pass
            elif delta_x < 0 and self.width <= self.min_width + 5:
                pass
            else:
                self.width += delta_x
        self.setGeometry(QRectF(self.x, self.y, self.width, self.height))
        self.update_borders_pos()
        self.update()
        self.widget.blockSignals(False)