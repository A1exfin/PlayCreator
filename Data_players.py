from Custom_scene import Field


class PlayersData:
    def __init__(self, field):

        self.player_size = 20
        self.field = field
        if False:
            self.current_scene = Field
        self.center_center_football = self.field.football_field_width / 2 - self.player_size / 2
        self.center_center_flag = self.field.flag_field_width / 2 - self.player_size / 2

        self.offence_football = (
            ('offence', 'C', '#000000', '#000000', 'white', self.center_center_football, - self.player_size / 2),
            ('offence', 'RG', '#000000', '#000000', 'white', self.center_center_football + 23, - self.player_size / 2),
            ('offence', 'RT', '#000000', '#000000', 'white', self.center_center_football + 46, - self.player_size / 2),
            ('offence', 'LG', '#000000', '#000000', 'white', self.center_center_football - 23, - self.player_size / 2),
            ('offence', 'LT', '#000000', '#000000', 'white', self.center_center_football - 46, - self.player_size / 2),
            ('offence', 'X', '#000000', '#000000', 'white', self.center_center_football + 230, - self.player_size / 2),
            ('offence', 'Y', '#000000', '#000000', 'white', self.center_center_football + 130, - self.player_size / 2 + 13),
            ('offence', 'Z', '#000000', '#000000', 'white', self.center_center_football - 230, - self.player_size / 2),
            ('offence', 'H', '#000000', '#000000', 'white', self.center_center_football - 130, - self.player_size / 2 + 13),
            ('offence', 'Q', '#000000', '#000000', 'white', self.center_center_football, - self.player_size / 2 + 50),
            ('offence', 'F', '#000000', '#000000', 'white', self.center_center_football, - self.player_size / 2 + 75)
        )

        self.additional_player_football = ('offence_add', 'V', '#000000', '#000000', 'white', self.center_center_football + 90, - self.player_size / 2 + 13)

        self.defence_football = (
            ('defence', 'Т', '#000000', '#000000', 'letter', self.center_center_football - 10, - self.player_size / 2 - 25),  # 1 tech
            ('defence', 'Т', '#000000', '#000000', 'letter', self.center_center_football + 33, - self.player_size / 2 - 25),  # 3 tech
            ('defence', 'E', '#000000', '#000000', 'letter', self.center_center_football + 56, - self.player_size / 2 - 25),  # RT
            ('defence', 'E', '#000000', '#000000', 'letter', self.center_center_football - 56, - self.player_size / 2 - 25),  # LE
            ('defence', 'M', '#000000', '#000000', 'letter', self.center_center_football + 33, - self.player_size / 2 - 50),
            ('defence', 'S', '#000000', '#000000', 'letter', self.center_center_football - 33, - self.player_size / 2 - 50),
            ('defence', 'W', '#000000', '#000000', 'letter', self.center_center_football - 130, - self.player_size / 2 - 50),
            ('defence', '$', '#000000', '#000000', 'letter', self.center_center_football + 130, - self.player_size / 2 - 50),
            ('defence', 'C', '#000000', '#000000', 'letter', self.center_center_football + 230, - self.player_size / 2 - 65),  # RC
            ('defence', 'C', '#000000', '#000000', 'letter', self.center_center_football - 230, - self.player_size / 2 - 65),  # LC
            ('defence', 'F', '#000000', '#000000', 'letter', self.center_center_football, - self.player_size / 2 - 120)
        )

        self.kickoff_football = (
            ('kickoff', '', '#000000', '#000000', 'white', self.center_center_football + 45, - self.player_size / 2),
            ('kickoff', '', '#000000', '#000000', 'white', self.center_center_football + 90, - self.player_size / 2),
            ('kickoff', '', '#000000', '#000000', 'white', self.center_center_football + 135, - self.player_size / 2),
            ('kickoff', '', '#000000', '#000000', 'white', self.center_center_football + 180, - self.player_size / 2),
            ('kickoff', '', '#000000', '#000000', 'white', self.center_center_football + 225, - self.player_size / 2),
            ('kickoff', '', '#000000', '#000000', 'white', self.center_center_football - 45, - self.player_size / 2),
            ('kickoff', '', '#000000', '#000000', 'white', self.center_center_football - 90, - self.player_size / 2),
            ('kickoff', '', '#000000', '#000000', 'white', self.center_center_football - 135, - self.player_size / 2),
            ('kickoff', '', '#000000', '#000000', 'white', self.center_center_football - 180, - self.player_size / 2),
            ('kickoff', '', '#000000', '#000000', 'white', self.center_center_football - 225, - self.player_size / 2),
            ('kickoff', '', '#000000', '#000000', 'white', self.center_center_football - 25, - self.player_size / 2 + 75)
        )

        self.kickoff_return = (
            ('kick_ret', '', '#000000', '#000000', 'triangle_bot', self.center_center_football - 180,
             - self.player_size / 2 - 3 * self.field.football_five_yard),  # first line
            ('kick_ret', '', '#000000', '#000000', 'triangle_bot', self.center_center_football - 90,
             - self.player_size / 2 - 3 * self.field.football_five_yard),  # first line
            ('kick_ret', '', '#000000', '#000000', 'triangle_bot', self.center_center_football,
             - self.player_size / 2 - 3 * self.field.football_five_yard),  # first line
            ('kick_ret', '', '#000000', '#000000', 'triangle_bot', self.center_center_football + 90,
             - self.player_size / 2 - 3 * self.field.football_five_yard),  # first line
            ('kick_ret', '', '#000000', '#000000', 'triangle_bot', self.center_center_football + 180,
             - self.player_size / 2 - 3 * self.field.football_five_yard),  # first line
            ('kick_ret', '', '#000000', '#000000', 'triangle_bot', self.center_center_football - 135,
             - self.player_size / 2 - 3 * self.field.football_ten_yard),  # second line
            ('kick_ret', '', '#000000', '#000000', 'triangle_bot', self.center_center_football,
             - self.player_size / 2 - 3 * self.field.football_ten_yard),  # second line
            ('kick_ret', '', '#000000', '#000000', 'triangle_bot', self.center_center_football + 135,
             - self.player_size / 2 - 3 * self.field.football_ten_yard),  # second line
            ('kick_ret', '', '#000000', '#000000', 'triangle_bot', self.center_center_football - 95,
             - self.player_size / 2 - 9 * self.field.football_five_yard),  # third line
            ('kick_ret', '', '#000000', '#000000', 'triangle_bot', self.center_center_football + 95,
             - self.player_size / 2 - 9 * self.field.football_five_yard),  # third line
            ('kick_ret', '', '#000000', '#000000', 'triangle_bot', self.center_center_football,
             self.field.football_ten_yard + 2 * self.field.football_one_yard)
        )

        self.punt_football = (
            ('punt_kick', 'C', '#000000', '#000000', 'white', self.center_center_football, - self.player_size / 2),
            ('punt_kick', '', '#000000', '#000000', 'white', self.center_center_football + 23, - self.player_size / 2),
            ('punt_kick', '', '#000000', '#000000', 'white', self.center_center_football + 46, - self.player_size / 2),
            ('punt_kick', '', '#000000', '#000000', 'white', self.center_center_football - 23, - self.player_size / 2),
            ('punt_kick', '', '#000000', '#000000', 'white', self.center_center_football - 46, - self.player_size / 2),
            ('punt_kick', '', '#000000', '#000000', 'white', self.center_center_football + 230, - self.player_size / 2),
            ('punt_kick', '', '#000000', '#000000', 'white', self.center_center_football + 69, - self.player_size / 2 + 13),
            ('punt_kick', '', '#000000', '#000000', 'white', self.center_center_football - 230, - self.player_size / 2),
            ('punt_kick', '', '#000000', '#000000', 'white', self.center_center_football - 69, - self.player_size / 2 + 13),
            ('punt_kick', '', '#000000', '#000000', 'white', self.center_center_football + 25, - self.player_size / 2 + 75),
            ('punt_kick', '', '#000000', '#000000', 'white', self.center_center_football, - self.player_size / 2 + 150)
        )

        self.punt_return = (
            ('punt_ret', '', '#000000', '#000000', 'triangle_bot', self.center_center_football - 10, - self.player_size / 2 - 25),  # 1 tech
            ('punt_ret', '', '#000000', '#000000', 'triangle_bot', self.center_center_football + 33, - self.player_size / 2 - 25),  # 3 tech
            ('punt_ret', '', '#000000', '#000000', 'triangle_bot', self.center_center_football + 56, - self.player_size / 2 - 25),  # RT
            ('punt_ret', '', '#000000', '#000000', 'triangle_bot', self.center_center_football - 56, - self.player_size / 2 - 25),  # LE
            ('punt_ret', '', '#000000', '#000000', 'triangle_bot', self.center_center_football + 86, - self.player_size / 2 - 25),
            ('punt_ret', '', '#000000', '#000000', 'triangle_bot', self.center_center_football - 86, - self.player_size / 2 - 25),
            ('punt_ret', '', '#000000', '#000000', 'triangle_bot', self.center_center_football - 100, - self.player_size / 2 - 115),
            ('punt_ret', '', '#000000', '#000000', 'triangle_bot', self.center_center_football + 100, - self.player_size / 2 - 115),
            ('punt_ret', '', '#000000', '#000000', 'triangle_bot', self.center_center_football + 225, - self.player_size / 2 - 25),  # RC
            ('punt_ret', '', '#000000', '#000000', 'triangle_bot', self.center_center_football - 225, - self.player_size / 2 - 25),  # LC
            ('punt_ret', '', '#000000', '#000000', 'triangle_bot', self.center_center_football, self.field.football_ten_yard + self.field.football_five_yard - self.player_size / 2)
        )

        self.field_goal_off_football = (
            ('field_goal_off', 'C', '#000000', '#000000', 'white', self.center_center_football, - self.player_size / 2),
            ('field_goal_off', '', '#000000', '#000000', 'white', self.center_center_football + 23, - self.player_size / 2),
            ('field_goal_off', '', '#000000', '#000000', 'white', self.center_center_football + 46, - self.player_size / 2),
            ('field_goal_off', '', '#000000', '#000000', 'white', self.center_center_football - 23, - self.player_size / 2),
            ('field_goal_off', '', '#000000', '#000000', 'white', self.center_center_football - 46, - self.player_size / 2),
            ('field_goal_off', '', '#000000', '#000000', 'white', self.center_center_football + 92, - self.player_size / 2 + 13),
            ('field_goal_off', '', '#000000', '#000000', 'white', self.center_center_football + 69, - self.player_size / 2),
            ('field_goal_off', '', '#000000', '#000000', 'white', self.center_center_football - 92, - self.player_size / 2 + 13),
            ('field_goal_off', '', '#000000', '#000000', 'white', self.center_center_football - 69, - self.player_size / 2),
            ('field_goal_off', '', '#000000', '#000000', 'white', self.center_center_football + 12, - self.player_size / 2 + 75),
            ('field_goal_off', '', '#000000', '#000000', 'white', self.center_center_football - 20, - self.player_size / 2 + 90)
        )

        self.field_goal_def = (
            ('field_goal_def', '', '#000000', '#000000', 'triangle_bot', self.center_center_football - 10, - self.player_size / 2 - 25),  # 1 tech
            ('field_goal_def', '', '#000000', '#000000', 'triangle_bot', self.center_center_football + 33, - self.player_size / 2 - 25),  # 3 tech
            ('field_goal_def', '', '#000000', '#000000', 'triangle_bot', self.center_center_football + 56, - self.player_size / 2 - 25),  # RT
            ('field_goal_def', '', '#000000', '#000000', 'triangle_bot', self.center_center_football - 56, - self.player_size / 2 - 25),  # LE
            ('field_goal_def', '', '#000000', '#000000', 'triangle_bot', self.center_center_football + 86, - self.player_size / 2 - 25),
            ('field_goal_def', '', '#000000', '#000000', 'triangle_bot', self.center_center_football - 86, - self.player_size / 2 - 25),
            ('field_goal_def', '', '#000000', '#000000', 'triangle_bot', self.center_center_football - 75, - self.player_size / 2 - 65),
            ('field_goal_def', '', '#000000', '#000000', 'triangle_bot', self.center_center_football + 75, - self.player_size / 2 - 65),
            ('field_goal_def', '', '#000000', '#000000', 'triangle_bot', self.center_center_football + 109, - self.player_size / 2 - 25),  # RC
            ('field_goal_def', '', '#000000', '#000000', 'triangle_bot', self.center_center_football - 109, - self.player_size / 2 - 25),  # LC
            ('field_goal_def', '', '#000000', '#000000', 'triangle_bot', self.center_center_football, - self.player_size / 2 - 65)
        )

        self.offence_flag = (
            ('offence', 'C', '#000000', '#000000', 'white', self.center_center_flag, -self.player_size / 2),
            ('offence', 'X', '#000000', '#000000', 'white', self.center_center_flag + self.field.flag_width_one_yard * 10, -self.player_size / 2),
            ('offence', 'Z', '#000000', '#000000', 'white', self.center_center_flag - self.field.flag_width_one_yard * 10, -self.player_size / 2),
            ('offence', 'Y', '#000000', '#000000', 'white', self.center_center_flag + self.field.flag_width_one_yard * 5, -self.player_size / 2),
            ('offence', 'Q', '#000000', '#000000', 'white', self.center_center_flag, -self.player_size / 2 + self.field.flag_one_yard * 5)
        )

        self.additional_player_flag = ('offence_add', 'H', '#000000', '#000000', 'white',
                                       self.center_center_football + self.field.flag_width_one_yard * 2.5,
                                       - self.player_size / 2)

        self.defence_flag = (
            ('defence', 'M', '#000000', '#000000', 'letter', self.center_center_flag, -self.player_size / 2 - self.field.flag_one_yard * 7),
            ('defence', 'C', '#000000', '#000000', 'letter', self.center_center_flag + self.field.flag_width_one_yard * 10, -self.player_size / 2 - self.field.flag_one_yard * 5),
            ('defence', 'C', '#000000', '#000000', 'letter', self.center_center_flag - self.field.flag_width_one_yard * 10, -self.player_size / 2 - self.field.flag_one_yard * 5),
            ('defence', 'S', '#000000', '#000000', 'letter', self.center_center_flag + self.field.flag_width_one_yard * 7, -self.player_size / 2 - self.field.flag_one_yard * 9),
            ('defence', 'S', '#000000', '#000000', 'letter', self.center_center_flag - self.field.flag_width_one_yard * 7, -self.player_size / 2 - self.field.flag_one_yard * 9)
        )