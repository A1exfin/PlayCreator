from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtGui import QColor, QPainter, QPen, QCursor, QPixmap, QBrush
from PySide6.QtCore import Qt, QRectF
import os
from Dialog_windows import DialogFigureSettings
from Enums import Modes
from DB_offline.models import RectangleORM

__all__ = ['Rectangle']


class Rectangle(QGraphicsRectItem):
    # edited_border_width = 4
    pen_hover_color = QColor('#ffcb30')

    def __init__(self, x: float, y: float, width: float, height: float,
                 border: bool, border_width: int, border_color: str,
                 fill: bool, fill_opacity: str, fill_color: str,
                 rect_id_pk: int = None, scheme_id_fk: int = None):
        super().__init__(0, 0, 0, 0)  # так сделано что бы координаты, возвращаемые методами self.x() (self.scenePos.x()), хранились в коардинатах сцены, а прямоугольник отрисовывался правильно
        self.rect_id_pk = rect_id_pk
        self.scheme_id_fk = scheme_id_fk
        self.border = border
        self.border_color = border_color
        self.border_width = border_width
        self.fill = fill
        self.fill_color = fill_color
        self.fill_opacity = fill_opacity
        if self.border:
            self.pen = QPen(QColor(border_color), border_width, s=Qt.SolidLine, c=Qt.RoundCap, j=Qt.RoundJoin)
        else:
            self.pen = QPen(QColor(border_color), 0.0000001, s=Qt.SolidLine, c=Qt.RoundCap, j=Qt.RoundJoin)
        if self.fill:
            self.brush = QBrush(f'{fill_opacity}{fill_color[1:]}')
        else:
            self.brush = QBrush(Qt.transparent)
        self.start_pos = None
        self.borders = {}
        self.cursors = {'left': Qt.SizeHorCursor,
                        'right': Qt.SizeHorCursor,
                        'top': Qt.SizeVerCursor,
                        'bot': Qt.SizeVerCursor,
                        'top_left': Qt.SizeFDiagCursor,
                        'bot_right': Qt.SizeFDiagCursor,
                        'top_right': Qt.SizeBDiagCursor,
                        'bot_left': Qt.SizeBDiagCursor,
                        'move': Qt.SizeAllCursor,
                        'erase': QCursor(QPixmap('://Cursors/Cursors/eraser.cur'), 0, 0)}
        self.border_selected = None
        self.setAcceptHoverEvents(True)
        # Если прямоугольник имеет id_pk (то есть он загружен из БД), то при его удалении со сцены, устанавливается этот флаг.
        # И при проходе циклом по прямоугольникам, которые хранятся в списке прямоугольников сцены, при сохранении плейбука
        # обновляются ORM-объекты, при этом приямоугольники с этим флагом удаляются из списка сцены, из ORM и затем из БД.
        self.is_deleted = False
        self.hover = False
        self.setZValue(0)
        self.set_rect(x, y, width, height)

    def set_rect(self, x: float, y: float, width: float, height: float):
        self.setPos(x, y)
        self.setRect(QRectF(0, 0, width, height))

    def paint(self, painter, option, widget=None):
        painter.setRenderHints(QPainter.Antialiasing)
        self.setBrush(self.brush)
        if self.hover:
            self.setPen(QPen(self.pen_hover_color, self.pen.width(), self.pen.style(), self.pen.capStyle(), self.pen.joinStyle()))
        else:
            self.setPen(QPen(self.pen))
        super().paint(painter, option, widget)
        # painter.setPen(QPen(QColor(Qt.red), 1))
        # painter.setBrush(QBrush(Qt.red))
        # for border, rect in self.borders.items():
        #     painter.drawRect(QRectF(rect.x() - self.x(), rect.y() - self.y(), rect.width(), rect.height()))
        self.scene().update()

    def mousePressEvent(self, event):
        # print(self)
        self.border_selected = self.check_border_under_cursor(event.scenePos())
        if self.scene().mode == Modes.move and event.button() == Qt.LeftButton and not self.border_selected:
            self.setZValue(20)
            self.start_pos = event.scenePos()
        if self.scene().mode == Modes.erase and event.button() == Qt.LeftButton:
            self.setCursor(Qt.ArrowCursor)  # Возврат стандартного курсора сразу после клика
            if self.rect_id_pk:
                self.is_deleted = True
            else:
                self.scene().rectangles.remove(self)
            self.scene().removeItem(self)
            # self.scene().update()

    def mouseMoveEvent(self, event):
        if self.scene().mode == Modes.move and self.border_selected:
            self.interactive_resize(event.scenePos())
        elif self.scene().mode == Modes.move:
            if self.start_pos:
                delta = event.scenePos() - self.start_pos
                if self.scene().check_field_x(self.x() + delta.x()) \
                        and self.scene().check_field_x(self.x() + self.rect().width() + delta.x()):
                    self.moveBy(delta.x(), 0)
                if self.scene().check_field_y(self.y() + delta.y())\
                        and self.scene().check_field_y(self.y() + self.rect().height() + delta.y()):
                    self.moveBy(0, delta.y())
                self.start_pos = event.scenePos()
        # super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.scene().mode == Modes.move:
            self.border_selected = None
            self.start_pos = None
            self.setZValue(0)
        self.normalizate()
        self.update_borders_pos()
        # super().mouseReleaseEvent(event)

    def hoverEnterEvent(self, event):
        self.update_borders_pos()
        if self.scene().mode == Modes.move or self.scene().mode == Modes.erase:
            self.hover = True

    def hoverMoveEvent(self, event):
        border_under_cursor = self.check_border_under_cursor(event.scenePos())
        if self.scene().mode == Modes.erase:
            self.hover = True
            cursor = self.cursors['erase']
        elif self.scene().mode == Modes.move:
            if border_under_cursor:
                cursor = self.cursors[border_under_cursor]
            else:
                cursor = self.cursors['move']
                # cursor = Qt.ArrowCursor
            self.hover = True
        else:
            cursor = Qt.ArrowCursor
            self.hover = False
        self.setCursor(cursor)

    def hoverLeaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self.hover = False

    def mouseDoubleClickEvent(self, event):
        if self.scene().mode == Modes.move:
            dialog = DialogFigureSettings(Modes.rectangle, self.border, self.border_color, self.border_width,
                                          self.fill, self.fill_color, self.fill_opacity, parent=self.scene().main_window)
            result = dialog.exec()
            if result:
                self.border = dialog.border
                if self.border:
                    self.border_color = dialog.border_color
                    self.border_width = dialog.border_width
                    self.pen.setColor(self.border_color)
                    self.pen.setWidth(self.border_width)
                else:
                    self.pen.setWidthF(0.0000001)
                self.fill = dialog.fill
                if self.fill:
                    self.fill_color = dialog.fill_color
                    self.fill_opacity = dialog.fill_opacity
                    self.brush.setColor(QColor(f'{self.fill_opacity}{self.fill_color[1:]}'))
                else:
                    self.brush.setColor(Qt.transparent)

    def update_borders_pos(self):
        self.borders['left'] = QRectF(self.x() - self.border_width / 2 - 1, self.y() + self.border_width / 2,
                                      self.border_width + 1, self.rect().height() - self.border_width)
        self.borders['right'] = QRectF(self.x() + self.rect().width() - self.border_width / 2, self.y() + self.border_width / 2,
                                       self.border_width, self.rect().height() - self.border_width)
        self.borders['top_left'] = QRectF(self.x() - self.border_width / 2 - 1, self.y() - self.border_width / 2 - 1,
                                          self.border_width + 1, self.border_width + 1)  # top_left
        self.borders['top'] = QRectF(self.x() + self.border_width / 2, self.y() - self.border_width / 2 - 1,
                                     self.rect().width() - self.border_width, self.border_width + 1)  # top_mid
        self.borders['top_right'] = QRectF(self.x() + self.rect().width() - self.border_width / 2, self.y() - self.border_width / 2,
                                           self.border_width, self.border_width)  # top_right
        self.borders['bot_left'] = QRectF(self.x() - self.border_width / 2 - 1, self.y() + self.rect().height() - self.border_width / 2,
                                          self.border_width + 1, self.border_width)  # bot_left
        self.borders['bot'] = QRectF(self.x() + self.border_width / 2, self.y() + self.rect().height() - self.border_width / 2,
                                     self.rect().width() - self.border_width, self.border_width)  # bot_mid
        self.borders['bot_right'] = QRectF(self.x() + self.rect().width() - self.border_width / 2, self.y() + self.rect().height() - self.border_width / 2,
                                           self.border_width, self.border_width)  # bot_right

    def check_border_under_cursor(self, point):
        for border, rect in self.borders.items():
            if rect.contains(point):
                return border
        return None

    def normalizate(self):
        if self.rect().width() < 0:
            x, width = self.x() + self.rect().width(), - self.rect().width()
            self.set_rect(x, self.y(), width, self.rect().height())
        if self.rect().height() < 0:
            y, height = self.y() + self.rect().height(), - self.rect().height()
            self.set_rect(self.x(), y, self.rect().width(), height)

    def interactive_resize(self, mouse_pos):
        if self.border_selected == 'left':
            if self.scene().check_field_x(mouse_pos.x()):
                delta_x = mouse_pos.x() - self.x()
                x = self.x() + delta_x
                width = self.rect().width() - delta_x
                self.set_rect(x, self.y(), width, self.rect().height())
        elif self.border_selected == 'right':
            if self.scene().check_field_x(mouse_pos.x()):
                delta_x = mouse_pos.x() - self.rect().width() - self.x()
                width = self.rect().width() + delta_x
                self.set_rect(self.x(), self.y(), width, self.rect().height())
        elif self.border_selected == 'top':
            if self.scene().check_field_y(mouse_pos.y()):
                delta_y = mouse_pos.y() - self.y()
                y = self.y() + delta_y
                height = self.rect().height() - delta_y
                self.set_rect(self.x(), y, self.rect().width(), height)
        elif self.border_selected == 'bot':
            if self.scene().check_field_y(mouse_pos.y()):
                delta_y = mouse_pos.y() - self.rect().height() - self.y()
                height = self.rect().height() + delta_y
                self.set_rect(self.x(), self.y(), self.rect().width(), height)
        elif self.border_selected == 'top_left':
            if self.scene().check_field_x(mouse_pos.x()):
                delta_x = mouse_pos.x() - self.x()
                x = self.x() + delta_x
                width = self.rect().width() - delta_x
                self.set_rect(x, self.y(), width, self.rect().height())
            if self.scene().check_field_y(mouse_pos.y()):
                delta_y = mouse_pos.y() - self.y()
                y = self.y() + delta_y
                height = self.rect().height() - delta_y
                self.set_rect(self.x(), y, self.rect().width(), height)
        elif self.border_selected == 'top_right':
            if self.scene().check_field_x(mouse_pos.x()):
                delta_x = mouse_pos.x() - self.rect().width() - self.x()
                width = self.rect().width() + delta_x
                self.set_rect(self.x(), self.y(), width, self.rect().height())
            if self.scene().check_field_y(mouse_pos.y()):
                delta_y = mouse_pos.y() - self.y()
                y = self.y() + delta_y
                height = self.rect().height() - delta_y
                self.set_rect(self.x(), y, self.rect().width(), height)
        elif self.border_selected == 'bot_left':
            if self.scene().check_field_x(mouse_pos.x()):
                delta_x = mouse_pos.x() - self.x()
                x = self.x() + delta_x
                width = self.rect().width() - delta_x
                self.set_rect(x, self.y(), width, self.rect().height())
            if self.scene().check_field_y(mouse_pos.y()):
                delta_y = mouse_pos.y() - self.rect().height() - self.y()
                height = self.rect().height() + delta_y
                self.set_rect(self.x(), self.y(), self.rect().width(), height)
        elif self.border_selected == 'bot_right':
            if self.scene().check_field_x(mouse_pos.x()):
                delta_x = mouse_pos.x() - self.rect().width() - self.x()
                width = self.rect().width() + delta_x
                self.set_rect(self.x(), self.y(), width, self.rect().height())
            if self.scene().check_field_y(mouse_pos.y()):
                delta_y = mouse_pos.y() - self.rect().height() - self.y()
                height = self.rect().height() + delta_y
                self.set_rect(self.x(), self.y(), self.rect().width(), height)
        self.update_borders_pos()
        # self.update()

    def __eq__(self, other):
        return self.rect_id_pk == other.rect_id_pk if isinstance(other, RectangleORM) else super().__eq__(other)

    def __repr__(self):
        return f'\n\t<{self.__class__.__name__} (id_pk: {self.rect_id_pk}; scheme_id_fk: {self.scheme_id_fk};' \
               f' x/y: {self.x()}/{self.y()}; width/height: {self.rect().width()}/{self.rect().height()};' \
               f' border_color: {self.border_color}; fill_color: {self.fill_opacity}{self.fill_color[1:]};' \
               f' deleted: {self.is_deleted}) at {hex(id(self))}>'

    def return_data(self):
        return self.rect_id_pk, self.scheme_id_fk, self.x(), self.y(), self.rect().width(), self.rect().height(),\
               self.border, self.border_width, self.border_color, self.fill, self.fill_opacity, self.fill_color