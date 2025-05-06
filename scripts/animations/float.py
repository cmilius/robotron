import copy

class FloatingAnimations:
    """
    Float a sprite/surface at the given position. For example: family scores and family skull_and_bones
    """
    def __init__(self, game):
        self.game = game

    def float_anim(self, data_dict):
        """
        Float the surface at the given position for the given amount of time.
        If the time_to_display == 0, remove it from the dictionary. Return the modified data_dict.

        :param data_dict: [surface, position, time_to_display]
        :return: dict
        """
        # use copy.copy() to safely alter the dictionary while iterating through it
        data_dict_copy = copy.copy(data_dict)

        for key in data_dict_copy:
            if data_dict_copy[key][2] > 0:
                self.game.display.blit(data_dict_copy[key][0], (data_dict_copy[key][1]))
                data_dict_copy[key][2] -= 1  # reduce the display countdown
                # float ominously
                data_dict_copy[key][1][0] -= .1
                data_dict_copy[key][1][1] -= .1
            if data_dict[key][2] == 0:
                # Remove from the dictionary once the timer has run out
                del data_dict[key]
        return data_dict