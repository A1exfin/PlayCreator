from PySide6.QtGui import QPen, QColor

__all__ = ['FieldData']


class FieldData:
    def __init__(self):
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