from typing import TYPE_CHECKING, Union
import os
from PySide6.QtWidgets import QGraphicsProxyWidget, QTextEdit, QFrame
from PySide6.QtCore import Qt, QRectF, QPointF, QEvent, QSize
from PySide6.QtGui import QCursor, QPen, QBrush, QPixmap, QColor, QFont, QTextCursor, QPainter, QTextCharFormat
from Enums import Modes
from DB_offline.models import LabelORM

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget, QGraphicsSceneMouseEvent, QGraphicsSceneHoverEvent, QStyleOptionGraphicsItem
    from PySide6.QtGui import QMouseEvent, QKeyEvent, QFocusEvent

__all__ = ['ProxyWidgetLabel']


class TextEdit(QTextEdit):
    def __init__(self, proxy,  text: str, font: QFont, color: str, parent=None):
        super().__init__(parent=parent)
        self.proxy = proxy
        self.setFont(font)
        self.setTextColor(color)
        self.setText(text)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet(f'''background-color: transparent;\n''')
        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setReadOnly(True)
        self.setMinimumSize(self.proxy.min_width, self.proxy.min_height)
        self.setMaximumSize(self.proxy.max_width, self.proxy.max_height)
        self.textChanged.connect(self.update_height)

    def mouseDoubleClickEvent(self, event: 'QMouseEvent'):
        if self.proxy.scene().mode == Modes.move and event.button() == Qt.LeftButton and self.isReadOnly():
            self.proxy.scene().current_label = self
            self.setReadOnly(False)
            text_cursor = self.textCursor()
            text_cursor.movePosition(QTextCursor.MoveOperation.End)
            self.setTextCursor(text_cursor)
            self.proxy.scene().labelDoubleClicked.emit(self)
        elif self.proxy.scene().mode == Modes.move and event.button() == Qt.LeftButton and not self.isReadOnly():
            super().mouseDoubleClickEvent(event)

    def clear_focus(self):
        text_cursor = self.textCursor()
        text_cursor.clearSelection()
        self.setTextCursor(text_cursor)
        self.setReadOnly(True)
        self.clearFocus()
        self.proxy.scene().current_label = None
        self.proxy.scene().labelEditingFinished.emit(self)

    def focusOutEvent(self, event: 'QFocusEvent'):
        self.clear_focus()
        super().focusOutEvent(event)

    def keyPressEvent(self, event: 'QKeyEvent'):
        if event.key() == Qt.Key_Return and event.modifiers() == Qt.ShiftModifier:
            super().keyPressEvent(event)
        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.clear_focus()
            self.proxy.scene().labelEditingFinished.emit(self)
        else:
            super().keyPressEvent(event)

    def update_height(self):
        lines_number = 0
        line_height = self.fontMetrics().height()
        margin = self.document().documentMargin()
        for block_number in range(self.document().blockCount()):
            block = self.document().findBlockByNumber(block_number)
            lines_number_in_block = block.layout().lineCount()
            lines_number += lines_number_in_block
        height = line_height * lines_number + 2 * (margin + 4)
        if height > self.proxy.max_height:
            height = self.proxy.max_height
        if self.proxy.y() + height > self.proxy.scene().current_field_border[1]:
            y = self.proxy.y() - (self.proxy.y() + height - self.proxy.scene().current_field_border[1])
        else:
            y = self.proxy.y()
        self.proxy.setGeometry(self.proxy.x(), y, self.proxy.rect().width(), height)
        self.proxy.update_borders_pos()

    def __repr__(self):
        return f'<{self.__class__.__name__} (text: {self.toPlainText()}; font: {self.font().family()}; font_size: {self.font().pointSize()};' \
               f' color: {self.textColor().name()}; B: {self.font().bold()}; I: {self.font().italic()}; U: {self.font().underline()}) at {hex(id(self))}>'


class ProxyWidgetLabel(QGraphicsProxyWidget):
    border_width = 5
    min_width = 52
    min_height = 20
    max_width = 500
    max_height = 195

    def __init__(self, text: str, font_type: str, font_size: int, font_bold: bool, font_italic: bool, font_underline: bool,
                 font_color: str, x: float, y: float, width: float = 200, height: float = 33, label_id_pk: int = None, scheme_id_fk: int = None):
        super().__init__()
        font = QFont(font_type)
        font.setPointSize(font_size)
        font.setBold(font_bold)
        font.setItalic(font_italic)
        font.setUnderline(font_underline)
        self.setWidget(TextEdit(self, text, font, font_color))
        self.setGeometry(x, y, width, height)
        self.label_id_pk = label_id_pk
        self.scheme_id_fk = scheme_id_fk
        self.start_pos = None
        self.borders = {}
        self.selected_border = None
        self.cursor = {'left': Qt.SizeHorCursor,
                       'right': Qt.SizeHorCursor,
                       'move': Qt.SizeAllCursor,
                       'edited': Qt.IBeamCursor,
                       'erase': QCursor(QPixmap('://Cursors/Cursors/eraser.cur'), 0, 0)}
        self.setAcceptHoverEvents(True)
        self.hover = False
        # Если надпись имеет id_pk (то есть она загружена из БД), то при её удалении со сцены, устанавливается этот флаг.
        # И при проходе циклом по надписям, которые хранятся в списке надписей сцены, при сохранении плейбука
        # обновляются ORM-объекты, при этом надписи с этим флагом удаляются из списка сцены, из ORM и затем из БД.
        self.is_deleted = False
        self.update_borders_pos()
        self.setZValue(3)

    def paint(self, painter: 'QPainter', option: 'QStyleOptionGraphicsItem', widget: 'QWidget'):
        super().paint(painter, option, widget)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setBrush(QBrush(Qt.transparent))
        # for border, rect in self.borders.items():  # Отладка прямоугольников изменния размера
        #     painter.drawRect(QRectF(rect.x() - self.scenePos().x(), rect.y() - self.scenePos().y(), rect.width(), rect.height()))
        if not self.widget().isReadOnly():
            painter.setPen(QPen(Qt.red, 2, Qt.DashLine, c=Qt.RoundCap))
            painter.drawRect(self.rect())
        elif self.hover:
            painter.setPen(QPen(QColor('#ff990b'), 2, Qt.DashLine, c=Qt.RoundCap))
            painter.drawRect(self.rect())
        rect = QRectF(self.x() - 10, self.y() - 10, self.rect().width() + 20, self.rect().height() + 20)
        self.scene().update(rect)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent'):
        # print(self)
        self.setZValue(20)
        if self.scene().mode == Modes.move and event.button() == Qt.LeftButton and not self.widget().isReadOnly():
            self.selected_border = self.check_border_under_cursor(event.scenePos())
        if self.scene().mode == Modes.move and event.button() == Qt.LeftButton and self.widget().isReadOnly():
            self.start_pos = event.scenePos()
        elif self.scene().mode == Modes.erase and event.button() == Qt.LeftButton:
            self.scene().current_label = None
            self.setCursor(Qt.ArrowCursor)  # Возврат стандартного курсора сразу после клика
            self.is_deleted = True if self.label_id_pk else self.scene().labels.remove(self)
            self.scene().removeItem(self)
        elif self.scene().mode == Modes.move and not self.widget().isReadOnly() and not self.selected_border:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent'):
        if self.scene().mode == Modes.move and self.selected_border and not self.widget().isReadOnly():
            self.interactive_resize(event.scenePos())
        elif self.scene().mode == Modes.move and self.start_pos and self.widget().isReadOnly():
            delta = event.scenePos() - self.start_pos
            if self.scene().check_field_x(self.x() + delta.x()) \
                    and self.scene().check_field_x(self.x() + self.rect().width() + delta.x()):
                self.moveBy(delta.x(), 0)
            if self.scene().check_field_y(self.y() + delta.y())\
                    and self.scene().check_field_y(self.y() + self.rect().height() + delta.y()):
                self.moveBy(0, delta.y())
            self.start_pos = event.scenePos()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent'):
        self.setZValue(3)
        self.update_borders_pos()
        if self.scene().mode == Modes.move and event.button() == Qt.LeftButton and self.widget().isReadOnly() and not self.selected_border:
            self.start_pos = None
        elif self.scene().mode == Modes.move and event.button() == Qt.LeftButton and not self.widget().isReadOnly() and self.selected_border:
            self.selected_border = None
        else:
            super().mouseReleaseEvent(event)

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent'):
        if self.scene().mode == Modes.move or self. scene().mode == Modes.erase:
            self.hover = True
            # self.update()
            # super().hoverEnterEvent(event)

    def hoverMoveEvent(self, event: 'QGraphicsSceneHoverEvent'):
        if not self.widget().isReadOnly() and self.scene().mode == Modes.move:
            border_under_cursor = self.check_border_under_cursor(event.scenePos())
            if border_under_cursor:
                cursor = self.cursor[border_under_cursor]
            else:
                cursor = self.cursor['edited']
        elif self.widget().isReadOnly() and self.scene().mode == Modes.move:
            cursor = self.cursor['move']
            self.hover = True
        elif self.scene().mode == Modes.erase:
            cursor = self.cursor['erase']
            self.hover = True
        else:
            cursor = Qt.ArrowCursor
            self.hover = False
        self.setCursor(cursor)
        # self.update()
        # super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent'):
        if self.scene().mode == Modes.move or self.scene().mode == Modes.erase:
            self.hover = False
            # self.update()

    def update_borders_pos(self):
        self.borders['left'] = QRectF(self.x(), self.y(), self.border_width, self.rect().height())
        self.borders['right'] = QRectF(self.x() + self.rect().width() - self.border_width, self.y(),
                                       self.border_width, self.rect().height())

    def check_border_under_cursor(self, point: 'QPointF') -> Union['QRectF', None]:
        for border, rect in self.borders.items():
            if rect.contains(point):
                return border
        return None

    def interactive_resize(self, mouse_pos: 'QPointF'):
        x = self.x()
        width = self.rect().width()
        if self.selected_border == 'left':
            if self.scene().check_field_x(mouse_pos.x()):
                delta_x = mouse_pos.x() - self.x()
                if delta_x < 0 and self.rect().width() >= self.max_width:
                    pass
                elif delta_x > 0 and self.rect().width() <= self.min_width:
                    pass
                else:
                    x += delta_x
                    width -= delta_x
        elif self.selected_border == 'right':
            if self.scene().check_field_x(mouse_pos.x()):
                delta_x = mouse_pos.x() - self.rect().width() - self.x()
                if delta_x > 0 and self.rect().width() >= self.max_width:
                    pass
                elif delta_x < 0 and self.rect().width() <= self.min_width:
                    pass
                else:
                    width += delta_x
        self.setGeometry(QRectF(x, self.y(), width, self.rect().height()))
        self.widget().update_height()
        self.update_borders_pos()
        self.update()

    def __eq__(self, other):
        return self.label_id_pk == other.label_id_pk if isinstance(other, LabelORM) else super().__eq__(other)

    def __repr__(self):
        return f'\n\t<{self.__class__.__name__} (id_pk: {self.label_id_pk}; scheme_id_fk: {self.scheme_id_fk};' \
               f' x/y: {self.x()}/{self.y()}; width/height: {self.rect().width()}/{self.rect().height()};' \
               f' text: {self.widget().toPlainText()}; B: {self.widget().font().bold()}; I: {self.widget().font().italic()}; U: {self.widget().font().underline()};' \
               f' text_color: {self.widget().textColor().name()}; deleted: {self.is_deleted}) at {hex(id(self))}>'

    def return_data(self):
        return self.label_id_pk, self.scheme_id_fk, self.widget().toPlainText(),\
               self.widget().font().family(), self.widget().font().pointSize(),\
               self.widget().font().bold(), self.widget().font().italic(), self.widget().font().underline(),\
               self.widget().textColor().name(), self.x(), self.y(), self.rect().width(), self.rect().height()