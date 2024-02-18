from PySide6.QtCore import Qt
from enum import Enum


class AppTheme(Enum):
    dark = 1
    light = 2


class Modes(Enum):
    move = 1
    erase = 2
    route = 3
    block = 4
    motion = 5
    rectangle = 6
    ellipse = 7
    pencil = 8
    label = 9


class PlaybookType(Enum):
    football = 1
    flag = 2


class TeamType(Enum):
    offence = 1
    kickoff = 2
    punt_kick = 3
    field_goal_off = 4
    defence = 5
    kick_ret = 6
    punt_ret = 7
    field_goal_def = 8
    offence_add = 9


class FillType(Enum):
    white = 1
    full = 2
    left = 3
    right = 4
    mid = 5


class SymbolType(Enum):
    letter = 1
    cross = 2
    triangle_bot = 3
    triangle_top = 4