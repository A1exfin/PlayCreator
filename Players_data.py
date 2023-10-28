from Custom_scene import Field


class PlayersData:
    def __init__(self, field):

        self.player_size = 20
        self.field = field
        if False:
            self.field = Field
        self.center_center_football = self.field.football_field_width / 2 - self.player_size / 2
        self.center_center_flag = self.field.flag_field_width / 2 - self.player_size / 2
        self.kickoff_line = 7.5 * self.field.football_ten_yard - self.player_size / 2
        self.first_line_ret_team = self.field.football_field_length_center - self.player_size / 2
        self.second_line_ret_team = self.field.football_field_length_center - self.player_size / 2 -\
                                    self.field.football_ten_yard - self.field.football_five_yard
        self.third_line_ret_team = self.field.football_field_length_center - self.player_size / 2 -\
                                   3 * self.field.football_ten_yard
        self.offence_football = [['offence', i] for i in range(11)]
        self.additional_player_football = ('offence', '11', 'WR', self.center_center_football + 90, - self.player_size / 2 + 13, self.player_size, self.player_size)
        self.defence_football = [['defence', i] for i in range(11)]
        self.kickoff_football = [['kickoff', i] for i in range(11)]
        self.kickoff_return_football = [['kick_ret', i] for i in range(11)]
        self.punt_football = [['punt_kick', i] for i in range(11)]
        self.punt_return_football = [['punt_ret', i] for i in range(11)]
        self.field_goal_off_football = [['field_goal_off', i] for i in range(11)]
        self.field_goal_def_football = [['field_goal_def', i] for i in range(11)]

        self.offence_football_coordinates = (
            ('center', self.center_center_football,
             - self.player_size / 2,
             self.player_size, self.player_size),
            ('RG', self.center_center_football + 23,
             - self.player_size / 2,
             self.player_size, self.player_size),
            ('RT', self.center_center_football + 46,
             - self.player_size / 2,
             self.player_size, self.player_size),
            ('LG', self.center_center_football - 23,
             - self.player_size / 2,
             self.player_size, self.player_size),
            ('LT', self.center_center_football - 46,
             - self.player_size / 2,
             self.player_size, self.player_size),
            ('X', self.center_center_football + 230,
             - self.player_size / 2,
             self.player_size, self.player_size),
            ('Y', self.center_center_football + 130,
             - self.player_size / 2 + 13,
             self.player_size, self.player_size),
            ('Z', self.center_center_football - 230,
             - self.player_size / 2,
             self.player_size, self.player_size),
            ('H', self.center_center_football - 130,
             - self.player_size / 2 + 13,
             self.player_size, self.player_size),
            ('Q', self.center_center_football,
             - self.player_size / 2 + 50,
             self.player_size, self.player_size),
            ('F', self.center_center_football,
             - self.player_size / 2 + 75,
             self.player_size, self.player_size),)

        self.defence_football_coordinates = (
            ('Т', self.center_center_football - 10,  # 1 tech
             - self.player_size / 2 - 25,
             self.player_size, self.player_size),
            ('T', self.center_center_football + 33,  # 3 tech
             - self.player_size / 2 - 25,
             self.player_size, self.player_size),
            ('E', self.center_center_football + 56,  # RT
             - self.player_size / 2 - 25,
             self.player_size, self.player_size),
            ('E', self.center_center_football - 56,  # LE
             - self.player_size / 2 - 25,
             self.player_size, self.player_size),
            ('M', self.center_center_football + 33,
             - self.player_size / 2 - 50,
             self.player_size, self.player_size),
            ('S', self.center_center_football - 33,
             - self.player_size / 2 - 50,
             self.player_size, self.player_size),
            ('W', self.center_center_football - 130,
             - self.player_size / 2 - 50,
             self.player_size, self.player_size),
            ('$', self.center_center_football + 130,
             - self.player_size / 2 - 50,
             self.player_size, self.player_size),
            ('C', self.center_center_football + 230,  # RC
             - self.player_size / 2 - 65,
             self.player_size, self.player_size),
            ('C', self.center_center_football - 230,  # LC
             - self.player_size / 2 - 65,
             self.player_size, self.player_size),
            ('FS', self.center_center_football,  # FS
             - self.player_size / 2 - 120,
             self.player_size, self.player_size),)

        self.kickoff_football_coordinates = (
            ('rs1', self.center_center_football + 45,
             self.kickoff_line,
             self.player_size, self.player_size),
            ('rs2', self.center_center_football + 90,
             self.kickoff_line,
             self.player_size, self.player_size),
            ('rs3', self.center_center_football + 135,
             self.kickoff_line,
             self.player_size, self.player_size),
            ('rs4', self.center_center_football + 180,
             self.kickoff_line,
             self.player_size, self.player_size),
            ('rs5', self.center_center_football + 225,
             self.kickoff_line,
             self.player_size, self.player_size),
            ('ls1', self.center_center_football - 45,
             self.kickoff_line,
             self.player_size, self.player_size),
            ('ls2', self.center_center_football - 90,
             self.kickoff_line,
             self.player_size, self.player_size),
            ('ls3', self.center_center_football - 135,
             self.kickoff_line,
             self.player_size, self.player_size),
            ('ls4', self.center_center_football - 180,
             self.kickoff_line,
             self.player_size, self.player_size),
            ('ls5', self.center_center_football - 225,
             self.kickoff_line,
             self.player_size, self.player_size),
            ('K', self.center_center_football - 25,
             self.kickoff_line + 75,
             self.player_size, self.player_size), )

        self.kickoff_return_coordinates = (
            ('fl1', self.center_center_football - 180,
             self.first_line_ret_team,
             self.player_size, self.player_size),
            ('fl2', self.center_center_football - 90,
             self.first_line_ret_team,
             self.player_size, self.player_size),
            ('fl3', self.center_center_football,
             self.first_line_ret_team,
             self.player_size, self.player_size),
            ('fl4', self.center_center_football + 90,
             self.first_line_ret_team,
             self.player_size, self.player_size),
            ('fl5', self.center_center_football + 180,
             self.first_line_ret_team,
             self.player_size, self.player_size),
            ('sl1', self.center_center_football - 135,
             self.second_line_ret_team,
             self.player_size, self.player_size),
            ('sl2', self.center_center_football,
             self.second_line_ret_team,
             self.player_size, self.player_size),
            ('sl3', self.center_center_football + 135,
             self.second_line_ret_team,
             self.player_size, self.player_size),
            ('tl1', self.center_center_football - 95,
             self.third_line_ret_team,
             self.player_size, self.player_size),
            ('tl2', self.center_center_football + 95,
             self.third_line_ret_team,
             self.player_size, self.player_size),
            ('R', self.center_center_football,
             self.field.football_ten_yard + 2 * self.field.football_one_yard,
             self.player_size, self.player_size), )

        self.punt_coordinates = (
            ('center', self.center_center_football,
             - self.player_size / 2,
             self.player_size, self.player_size),
            ('RG', self.center_center_football + 23,
             - self.player_size / 2,
             self.player_size, self.player_size),
            ('RT', self.center_center_football + 46,
             - self.player_size / 2,
             self.player_size, self.player_size),
            ('LG', self.center_center_football - 23,
             - self.player_size / 2,
             self.player_size, self.player_size),
            ('LT', self.center_center_football - 46,
             - self.player_size / 2,
             self.player_size, self.player_size),
            ('X', self.center_center_football + 230,
             - self.player_size / 2,
             self.player_size, self.player_size),
            ('Y', self.center_center_football + 69,
             - self.player_size / 2 + 13,
             self.player_size, self.player_size),
            ('Z', self.center_center_football - 230,
             - self.player_size / 2,
             self.player_size, self.player_size),
            ('H', self.center_center_football - 69,
             - self.player_size / 2 + 13,
             self.player_size, self.player_size),
            ('', self.center_center_football + 25,
             - self.player_size / 2 + 75,
             self.player_size, self.player_size),
            ('P', self.center_center_football,
             - self.player_size / 2 + 150,
             self.player_size, self.player_size), )

        self.punt_return_coordinates = (
            ('Т', self.center_center_football - 10,  # 1 tech
             - self.player_size / 2 - 25,
             self.player_size, self.player_size),
            ('T', self.center_center_football + 33,  # 3 tech
             - self.player_size / 2 - 25,
             self.player_size, self.player_size),
            ('E', self.center_center_football + 56,  # RT
             - self.player_size / 2 - 25,
             self.player_size, self.player_size),
            ('E', self.center_center_football - 56,  # LE
             - self.player_size / 2 - 25,
             self.player_size, self.player_size),
            ('M', self.center_center_football + 86,
             - self.player_size / 2 - 25,
             self.player_size, self.player_size),
            ('S', self.center_center_football - 86,
             - self.player_size / 2 - 25,
             self.player_size, self.player_size),
            ('W', self.center_center_football - 100,
             - self.player_size / 2 - 115,
             self.player_size, self.player_size),
            ('$', self.center_center_football + 100,
             - self.player_size / 2 - 115,
             self.player_size, self.player_size),
            ('C', self.center_center_football + 225,  # RC
             - self.player_size / 2 - 25,
             self.player_size, self.player_size),
            ('C', self.center_center_football - 225,  # LC
             - self.player_size / 2 - 25,
             self.player_size, self.player_size),
            ('PR', self.center_center_football,  # FS
             self.field.football_ten_yard + self.field.football_five_yard - self.player_size / 2,
             self.player_size, self.player_size), )

        self.field_goal_off_coordinates = (
            ('center', self.center_center_football,
             - self.player_size / 2,
             self.player_size, self.player_size),
            ('RG', self.center_center_football + 23,
             - self.player_size / 2,
             self.player_size, self.player_size),
            ('RT', self.center_center_football + 46,
             - self.player_size / 2,
             self.player_size, self.player_size),
            ('LG', self.center_center_football - 23,
             - self.player_size / 2,
             self.player_size, self.player_size),
            ('LT', self.center_center_football - 46,
             - self.player_size / 2,
             self.player_size, self.player_size),
            ('X', self.center_center_football + 92,
             - self.player_size / 2 + 13,
             self.player_size, self.player_size),
            ('Y', self.center_center_football + 69,
             - self.player_size / 2,
             self.player_size, self.player_size),
            ('Z', self.center_center_football - 92,
             - self.player_size / 2 + 13,
             self.player_size, self.player_size),
            ('W', self.center_center_football - 69,
             - self.player_size / 2,
             self.player_size, self.player_size),
            ('H', self.center_center_football + 10,
             - self.player_size / 2 + 75,
             self.player_size, self.player_size),
            ('K', self.center_center_football - 25,
             - self.player_size / 2 + 100,
             self.player_size, self.player_size),)

        self.field_goal_def_coordinates = (
            ('Т', self.center_center_football - 10,  # 1 tech
             - self.player_size / 2 - 25,
             self.player_size, self.player_size),
            ('T', self.center_center_football + 33,  # 3 tech
             - self.player_size / 2 - 25,
             self.player_size, self.player_size),
            ('E', self.center_center_football + 56,  # RT
             - self.player_size / 2 - 25,
             self.player_size, self.player_size),
            ('E', self.center_center_football - 56,  # LE
             - self.player_size / 2 - 25,
             self.player_size, self.player_size),
            ('M', self.center_center_football + 86,
             - self.player_size / 2 - 25,
             self.player_size, self.player_size),
            ('S', self.center_center_football - 86,
             - self.player_size / 2 - 25,
             self.player_size, self.player_size),
            ('W', self.center_center_football - 75,
             - self.player_size / 2 - 65,
             self.player_size, self.player_size),
            ('$', self.center_center_football + 75,
             - self.player_size / 2 - 65,
             self.player_size, self.player_size),
            ('C', self.center_center_football + 109,  # RC
             - self.player_size / 2 - 25,
             self.player_size, self.player_size),
            ('C', self.center_center_football - 109,  # LC
             - self.player_size / 2 - 25,
             self.player_size, self.player_size),
            ('KR', self.center_center_football,  # FS
             - self.player_size / 2 - 65,
             self.player_size, self.player_size),)

        self.offence_flag = [['offence', i] for i in range(5)]
        self.defence_flag = [['defence', i] for i in range(5)]

        self.offence_flag_coordinates = (
            ('center', self.center_center_flag,
             -self.player_size / 2,
             self.player_size, self.player_size),
            ('X', self.center_center_flag + self.field.flag_width_one_yard * 10,
             -self.player_size / 2,
             self.player_size, self.player_size),
            ('Z', self.center_center_flag - self.field.flag_width_one_yard * 10,
             -self.player_size / 2,
             self.player_size, self.player_size),
            ('Y', self.center_center_flag + self.field.flag_width_one_yard * 5,
             -self.player_size / 2,
             self.player_size, self.player_size),
            ('Q', self.center_center_flag,
             -self.player_size / 2 + self.field.flag_one_yard * 5,
             self.player_size, self.player_size), )

        self.additional_player_flag = ('offence', 6, 'WR',
                                       self.center_center_football + self.field.flag_width_one_yard * 2.5,
                                       - self.player_size / 2, self.player_size, self.player_size)

        self.defence_flag_coordinates = (
            ('M', self.center_center_flag,
             -self.player_size / 2 - self.field.flag_one_yard * 7,
             self.player_size, self.player_size),
            ('C', self.center_center_flag + self.field.flag_width_one_yard * 10,
             -self.player_size / 2 - self.field.flag_one_yard * 5,
             self.player_size, self.player_size),
            ('C', self.center_center_flag - self.field.flag_width_one_yard * 10,
             -self.player_size / 2 - self.field.flag_one_yard * 5,
             self.player_size, self.player_size),
            ('S', self.center_center_flag + self.field.flag_width_one_yard * 7,
             -self.player_size / 2 - self.field.flag_one_yard * 9,
             self.player_size, self.player_size),
            ('S', self.center_center_flag - self.field.flag_width_one_yard * 7,
             -self.player_size / 2 - self.field.flag_one_yard * 9,
             self.player_size, self.player_size), )