import pygame
import random
import logging

logger = logging.getLogger(__name__)

WAVE_INTENSITY = {
    "robots": {1: 5,
               2: 8,
               3: 11
               }
}


class Spawner:
    def __init__(self, game):
        """
        Constructor to pull in Game class.
        """
        self.game = game
        self.display = self.game.display
        self.level = self.game.wave_counter

    @staticmethod
    def get_valid_position(size, exclude_range):
        """ Return valid positions within the display."""
        valid_positions = [i for i in range(size) if not (exclude_range[0] <= i < exclude_range[1])]
        return random.choice(valid_positions)

    def robot_spawn(self):
        """
        Spawn robots.

        :return: List of randomized positions
        """

        mod_surf_size_x = self.display.get_width() - self.game.robot_size[0]
        mod_surf_size_y = self.display.get_height() - self.game.robot_size[1]
        num_robots = WAVE_INTENSITY["robots"][self.level]
        posits = []

        # need to define an exclusion zone around the player spawn area  #TODO: ADD PLAYER POSITION
        x_exclude = [self.game.player_size[0] - 100, self.game.player_size[0] + 100]
        y_exclude = [self.game.player_size[1] - 100, self.game.player_size[1] + 100]

        for i in range(0, num_robots):
            posits.append(((random.choice([x for x in range(mod_surf_size_x) if x not in x_exclude])),
                           random.choice([y for y in range(mod_surf_size_y) if y not in y_exclude])))
        return posits
