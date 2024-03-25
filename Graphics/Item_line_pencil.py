from PySide6.QtWidgets import QGraphicsLineItem
from PySide6.QtGui import QColor, QPen
from PySide6.QtCore import Qt
from DB_offline.models import PencilLineORM

__all__ = ['PencilLine']


class PencilLine(QGraphicsLineItem):
    def __init__(self, x1: float, y1: float, x2: float, y2: float, line_thickness: int, line_color: str,
                 line_id_pk: int = None, scheme_id_fk: int = None):
        super().__init__(x1, y1, x2, y2)
        self.line_id_pk = line_id_pk
        self.scheme_id_fk = scheme_id_fk
        self.setPen(QPen(QColor(line_color), line_thickness, s=Qt.SolidLine, c=Qt.RoundCap, j=Qt.RoundJoin))
        # Если линия карандаша имеет id_pk (то есть она загружен из БД), то при её удалении со сцены, устанавливается этот флаг.
        # И при проходе циклом по линиям карандаша, которые хранятся в списке линий карандаша сцены, при сохранении плейбука
        # обновляются ORM-объекты, при этом линии карандаша с этим флагом удаляются из списка сцены, из ORM и затем из БД.
        self.is_deleted = False
        self.setZValue(0)

    # def mousePressEvent(self, event):
    #     print(self)

    def __eq__(self, other):
        return self.line_id_pk == other.line_id_pk if isinstance(other, PencilLineORM) else super().__eq__(other)

    def __repr__(self):
        return f'\n\t<{self.__class__.__name__} (id_pk: {self.line_id_pk}; scheme_id_fk: {self.scheme_id_fk};' \
               f' line_thickness: {self.pen().width()}; line_color: {self.pen().color().name()};' \
               f' deleted: {self.is_deleted}) at {hex(id(self))}>'

    def return_data(self):
        return self.line_id_pk, self.scheme_id_fk, self.line().x1(), self.line().y1(), self.line().x2(), self.line().y2(),\
               self.pen().width(), self.pen().color().name()