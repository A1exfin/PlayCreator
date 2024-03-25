from enum import Enum


class TeamType(Enum):
    offence = 0
    kickoff = 1
    punt_kick = 2
    field_goal_off = 3
    defence = 4
    kick_ret = 5
    punt_ret = 6
    field_goal_def = 7
    offence_add = 8