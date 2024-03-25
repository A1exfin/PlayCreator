from Enums import TeamType, FillType, SymbolType

__all__ = ['PlayersData']


class PlayersData:
    def __init__(self, field_data):

        self.player_size = 20
        self.field_data = field_data
        self.center_center_football = self.field_data.football_field_width / 2 - self.player_size / 2
        self.center_center_flag = self.field_data.flag_field_width / 2 - self.player_size / 2

        self.offence_football = (
            (TeamType.offence, 'C', 'C', '#000000', '#000000', FillType.white, self.center_center_football, - self.player_size / 2),
            (TeamType.offence, 'RG', 'RG', '#000000', '#000000', FillType.white, self.center_center_football + 23, - self.player_size / 2),
            (TeamType.offence, 'RT', 'RT', '#000000', '#000000', FillType.white, self.center_center_football + 46, - self.player_size / 2),
            (TeamType.offence, 'LG', 'LG', '#000000', '#000000', FillType.white, self.center_center_football - 23, - self.player_size / 2),
            (TeamType.offence, 'LT', 'LT', '#000000', '#000000', FillType.white, self.center_center_football - 46, - self.player_size / 2),
            (TeamType.offence, 'X', 'X', '#000000', '#000000', FillType.white, self.center_center_football + 230, - self.player_size / 2),
            (TeamType.offence, 'Y', 'Y', '#000000', '#000000', FillType.white, self.center_center_football + 130, - self.player_size / 2 + 13),
            (TeamType.offence, 'Z', 'Z', '#000000', '#000000', FillType.white, self.center_center_football - 230, - self.player_size / 2),
            (TeamType.offence, 'H', 'H', '#000000', '#000000', FillType.white, self.center_center_football - 130, - self.player_size / 2 + 13),
            (TeamType.offence, 'Q', 'Q', '#000000', '#000000', FillType.white, self.center_center_football, - self.player_size / 2 + 50),
            (TeamType.offence, 'F', 'F', '#000000', '#000000', FillType.white, self.center_center_football, - self.player_size / 2 + 75)
        )

        self.additional_player_football = (TeamType.offence_add, 'V', 'V', '#000000', '#000000', FillType.white, self.center_center_football + 90, - self.player_size / 2 + 13)

        self.defence_football = (
            (TeamType.defence, 'Т', 'Т', '#000000', '#000000', SymbolType.letter, self.center_center_football - 10, - self.player_size / 2 - 25),  # 1 tech
            (TeamType.defence, 'Т', 'Т', '#000000', '#000000', SymbolType.letter, self.center_center_football + 33, - self.player_size / 2 - 25),  # 3 tech
            (TeamType.defence, 'E', 'E', '#000000', '#000000', SymbolType.letter, self.center_center_football + 56, - self.player_size / 2 - 25),  # RT
            (TeamType.defence, 'E', 'E', '#000000', '#000000', SymbolType.letter, self.center_center_football - 56, - self.player_size / 2 - 25),  # LE
            (TeamType.defence, 'M', 'M', '#000000', '#000000', SymbolType.letter, self.center_center_football + 33, - self.player_size / 2 - 50),
            (TeamType.defence, 'S', 'S', '#000000', '#000000', SymbolType.letter, self.center_center_football - 33, - self.player_size / 2 - 50),
            (TeamType.defence, 'W', 'W', '#000000', '#000000', SymbolType.letter, self.center_center_football - 130, - self.player_size / 2 - 50),
            (TeamType.defence, '$', '$', '#000000', '#000000', SymbolType.letter, self.center_center_football + 130, - self.player_size / 2 - 50),
            (TeamType.defence, 'C', 'C', '#000000', '#000000', SymbolType.letter, self.center_center_football + 230, - self.player_size / 2 - 65),  # RC
            (TeamType.defence, 'C', 'C', '#000000', '#000000', SymbolType.letter, self.center_center_football - 230, - self.player_size / 2 - 65),  # LC
            (TeamType.defence, 'F', 'F', '#000000', '#000000', SymbolType.letter, self.center_center_football, - self.player_size / 2 - 120)
        )

        self.kickoff_football = (
            (TeamType.kickoff, '', '', '#000000', '#000000', FillType.white, self.center_center_football + 45, - self.player_size / 2),
            (TeamType.kickoff, '', '', '#000000', '#000000', FillType.white, self.center_center_football + 90, - self.player_size / 2),
            (TeamType.kickoff, '', '', '#000000', '#000000', FillType.white, self.center_center_football + 135, - self.player_size / 2),
            (TeamType.kickoff, '', '', '#000000', '#000000', FillType.white, self.center_center_football + 180, - self.player_size / 2),
            (TeamType.kickoff, '', '', '#000000', '#000000', FillType.white, self.center_center_football + 225, - self.player_size / 2),
            (TeamType.kickoff, '', '', '#000000', '#000000', FillType.white, self.center_center_football - 45, - self.player_size / 2),
            (TeamType.kickoff, '', '', '#000000', '#000000', FillType.white, self.center_center_football - 90, - self.player_size / 2),
            (TeamType.kickoff, '', '', '#000000', '#000000', FillType.white, self.center_center_football - 135, - self.player_size / 2),
            (TeamType.kickoff, '', '', '#000000', '#000000', FillType.white, self.center_center_football - 180, - self.player_size / 2),
            (TeamType.kickoff, '', '', '#000000', '#000000', FillType.white, self.center_center_football - 225, - self.player_size / 2),
            (TeamType.kickoff, '', '', '#000000', '#000000', FillType.white, self.center_center_football - 25, - self.player_size / 2 + 75)
        )

        self.kick_ret_football = (
            (TeamType.kick_ret, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football - 180,
             - self.player_size / 2 - 3 * self.field_data.football_five_yard),  # first line
            (TeamType.kick_ret, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football - 90,
             - self.player_size / 2 - 3 * self.field_data.football_five_yard),  # first line
            (TeamType.kick_ret, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football,
             - self.player_size / 2 - 3 * self.field_data.football_five_yard),  # first line
            (TeamType.kick_ret, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football + 90,
             - self.player_size / 2 - 3 * self.field_data.football_five_yard),  # first line
            (TeamType.kick_ret, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football + 180,
             - self.player_size / 2 - 3 * self.field_data.football_five_yard),  # first line
            (TeamType.kick_ret, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football - 135,
             - self.player_size / 2 - 3 * self.field_data.football_ten_yard),  # second line
            (TeamType.kick_ret, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football,
             - self.player_size / 2 - 3 * self.field_data.football_ten_yard),  # second line
            (TeamType.kick_ret, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football + 135,
             - self.player_size / 2 - 3 * self.field_data.football_ten_yard),  # second line
            (TeamType.kick_ret, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football - 95,
             - self.player_size / 2 - 9 * self.field_data.football_five_yard),  # third line
            (TeamType.kick_ret, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football + 95,
             - self.player_size / 2 - 9 * self.field_data.football_five_yard),  # third line
            (TeamType.kick_ret, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football,
             self.field_data.football_ten_yard + 2 * self.field_data.football_one_yard)
        )

        self.punt_kick_football = (
            (TeamType.punt_kick, 'C', '', '#000000', '#000000', FillType.white, self.center_center_football, - self.player_size / 2),
            (TeamType.punt_kick, '', '', '#000000', '#000000', FillType.white, self.center_center_football + 23, - self.player_size / 2),
            (TeamType.punt_kick, '', '', '#000000', '#000000', FillType.white, self.center_center_football + 46, - self.player_size / 2),
            (TeamType.punt_kick, '', '', '#000000', '#000000', FillType.white, self.center_center_football - 23, - self.player_size / 2),
            (TeamType.punt_kick, '', '', '#000000', '#000000', FillType.white, self.center_center_football - 46, - self.player_size / 2),
            (TeamType.punt_kick, '', '', '#000000', '#000000', FillType.white, self.center_center_football + 230, - self.player_size / 2),
            (TeamType.punt_kick, '', '', '#000000', '#000000', FillType.white, self.center_center_football + 69, - self.player_size / 2 + 13),
            (TeamType.punt_kick, '', '', '#000000', '#000000', FillType.white, self.center_center_football - 230, - self.player_size / 2),
            (TeamType.punt_kick, '', '', '#000000', '#000000', FillType.white, self.center_center_football - 69, - self.player_size / 2 + 13),
            (TeamType.punt_kick, '', '', '#000000', '#000000', FillType.white, self.center_center_football + 25, - self.player_size / 2 + 75),
            (TeamType.punt_kick, '', '', '#000000', '#000000', FillType.white, self.center_center_football, - self.player_size / 2 + 150)
        )

        self.punt_ret_football = (
            (TeamType.punt_ret, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football - 10, - self.player_size / 2 - 25),  # 1 tech
            (TeamType.punt_ret, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football + 33, - self.player_size / 2 - 25),  # 3 tech
            (TeamType.punt_ret, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football + 56, - self.player_size / 2 - 25),  # RT
            (TeamType.punt_ret, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football - 56, - self.player_size / 2 - 25),  # LE
            (TeamType.punt_ret, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football + 86, - self.player_size / 2 - 25),
            (TeamType.punt_ret, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football - 86, - self.player_size / 2 - 25),
            (TeamType.punt_ret, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football - 100, - self.player_size / 2 - 115),
            (TeamType.punt_ret, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football + 100, - self.player_size / 2 - 115),
            (TeamType.punt_ret, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football + 225, - self.player_size / 2 - 25),  # RC
            (TeamType.punt_ret, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football - 225, - self.player_size / 2 - 25),  # LC
            (TeamType.punt_ret, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football, self.field_data.football_ten_yard + self.field_data.football_five_yard - self.player_size / 2)
        )

        self.field_goal_off_football = (
            (TeamType.field_goal_off, 'C', '', '#000000', '#000000', FillType.white, self.center_center_football, - self.player_size / 2),
            (TeamType.field_goal_off, '', '', '#000000', '#000000', FillType.white, self.center_center_football + 23, - self.player_size / 2),
            (TeamType.field_goal_off, '', '', '#000000', '#000000', FillType.white, self.center_center_football + 46, - self.player_size / 2),
            (TeamType.field_goal_off, '', '', '#000000', '#000000', FillType.white, self.center_center_football - 23, - self.player_size / 2),
            (TeamType.field_goal_off, '', '', '#000000', '#000000', FillType.white, self.center_center_football - 46, - self.player_size / 2),
            (TeamType.field_goal_off, '', '', '#000000', '#000000', FillType.white, self.center_center_football + 92, - self.player_size / 2 + 13),
            (TeamType.field_goal_off, '', '', '#000000', '#000000', FillType.white, self.center_center_football + 69, - self.player_size / 2),
            (TeamType.field_goal_off, '', '', '#000000', '#000000', FillType.white, self.center_center_football - 92, - self.player_size / 2 + 13),
            (TeamType.field_goal_off, '', '', '#000000', '#000000', FillType.white, self.center_center_football - 69, - self.player_size / 2),
            (TeamType.field_goal_off, '', '', '#000000', '#000000', FillType.white, self.center_center_football + 12, - self.player_size / 2 + 75),
            (TeamType.field_goal_off, '', '', '#000000', '#000000', FillType.white, self.center_center_football - 20, - self.player_size / 2 + 90)
        )

        self.field_goal_def_football = (
            (TeamType.field_goal_def, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football - 10, - self.player_size / 2 - 25),  # 1 tech
            (TeamType.field_goal_def, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football + 33, - self.player_size / 2 - 25),  # 3 tech
            (TeamType.field_goal_def, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football + 56, - self.player_size / 2 - 25),  # RT
            (TeamType.field_goal_def, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football - 56, - self.player_size / 2 - 25),  # LE
            (TeamType.field_goal_def, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football + 86, - self.player_size / 2 - 25),
            (TeamType.field_goal_def, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football - 86, - self.player_size / 2 - 25),
            (TeamType.field_goal_def, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football - 75, - self.player_size / 2 - 65),
            (TeamType.field_goal_def, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football + 75, - self.player_size / 2 - 65),
            (TeamType.field_goal_def, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football + 109, - self.player_size / 2 - 25),  # RC
            (TeamType.field_goal_def, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football - 109, - self.player_size / 2 - 25),  # LC
            (TeamType.field_goal_def, '', '', '#000000', '#000000', SymbolType.triangle_bot, self.center_center_football, - self.player_size / 2 - 65)
        )

        self.offence_flag = (
            (TeamType.offence, 'C', 'C', '#000000', '#000000', FillType.white, self.center_center_flag, -self.player_size / 2),
            (TeamType.offence, 'X', 'X', '#000000', '#000000', FillType.white, self.center_center_flag + self.field_data.flag_width_one_yard * 10, -self.player_size / 2),
            (TeamType.offence, 'Z', 'Z', '#000000', '#000000', FillType.white, self.center_center_flag - self.field_data.flag_width_one_yard * 10, -self.player_size / 2),
            (TeamType.offence, 'Y', 'Y', '#000000', '#000000', FillType.white, self.center_center_flag + self.field_data.flag_width_one_yard * 5, -self.player_size / 2),
            (TeamType.offence, 'Q', 'Q', '#000000', '#000000', FillType.white, self.center_center_flag, -self.player_size / 2 + self.field_data.flag_one_yard * 5)
        )

        self.additional_player_flag = (TeamType.offence_add, 'H', 'H', '#000000', '#000000', FillType.white,
                                       self.center_center_football + self.field_data.flag_width_one_yard * 2.5,
                                       - self.player_size / 2)

        self.defence_flag = (
            (TeamType.defence, 'M', 'M', '#000000', '#000000', SymbolType.letter, self.center_center_flag, -self.player_size / 2 - self.field_data.flag_one_yard * 7),
            (TeamType.defence, 'C', 'C', '#000000', '#000000', SymbolType.letter, self.center_center_flag + self.field_data.flag_width_one_yard * 10, -self.player_size / 2 - self.field_data.flag_one_yard * 5),
            (TeamType.defence, 'C', 'C', '#000000', '#000000', SymbolType.letter, self.center_center_flag - self.field_data.flag_width_one_yard * 10, -self.player_size / 2 - self.field_data.flag_one_yard * 5),
            (TeamType.defence, 'S', 'S', '#000000', '#000000', SymbolType.letter, self.center_center_flag + self.field_data.flag_width_one_yard * 7, -self.player_size / 2 - self.field_data.flag_one_yard * 9),
            (TeamType.defence, 'S', 'S', '#000000', '#000000', SymbolType.letter, self.center_center_flag - self.field_data.flag_width_one_yard * 7, -self.player_size / 2 - self.field_data.flag_one_yard * 9)
        )