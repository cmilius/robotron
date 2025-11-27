from entities.entities import PhysicsEntity
import logging
import random

logger = logging.getLogger(__name__)


class Electrode(PhysicsEntity):


    def __init__(self, game, pos, size):
        super().__init__(game, "electrode", pos, size)
        electrode_type = random.randint(0, 3)  # pick between 1 of 3 electrodes
        if electrode_type == 2:
            self.size = (5, 9)  # This will eventually be replaced when we extract sizes from the json
        self.image = self.game.robotrons_animations.animations[self.e_type][str(electrode_type)][random.randint(0,1)]

