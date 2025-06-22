import random
import logging
from scripts.entities.entities import PhysicsEntity
from scripts.entities.enforcer import Enforcer

logger = logging.getLogger(__name__)

# CONSTANTS
SPAWN_TIME = random.randint(480, 600)  # frames, spawn sub-entities between 8 and 10 seconds

class PregnantEnemy(PhysicsEntity):
    """
    Pregnant enemies are entities that will spawn other entities, such as the spheroid and the quark.
    These have advanced animations that depend on their spawn countdown state.
    """

    def __init__(self, game, e_type, pos, size):
        super().__init__(game, e_type, pos, size)  # inheret the PhysicsEntity class
        self.block_actions = False  # override parent class variabled
        self.full_anim = False  # used to stop the full animation trigger logic from looping endlessly
        self.frame_counter = 4  # init this enemy at its largest size so it is easy to see spawning in

        self.num_frames = 4  # start by only iterating through the initial images (zero index)
        self.image = self.game.robotrons_animations.animations[self.e_type][str(self.frame_counter)][0]

        # Assigned in the specific class, number of sub-entities this entity will spawn
        self.number_of_children = None

        self.target_posit = self.random_movement()
        self.spawn_counter = 0
        self.spawn_time = SPAWN_TIME

    def animate(self, frame_movement=None):
        """
        Update the entity animations.

        :param list frame_movement: The direction vector the entity is moving in,
        not used by these entities but needed by the super() class
        :return: None
        """
        self.special_animation()

    def special_animation(self):
        self.anim_frame_delay += 1
        if self.anim_frame_delay == 8:
            # the dictionary is indexed by a number, indicating the current "frame" of the spawn
            # I did it this because each piece of the spawn changes size
            self.image = self.game.robotrons_animations.animations[self.e_type][str(self.frame_counter)][0]
            # TODO: extract the frame_size of the image to adjust the hitbox
            # self.rect = self.game.robotrons_animations.animations[self.e_type][]
            self.frame_counter += 1
            self.anim_frame_delay = 0
            if self.frame_counter == self.num_frames + 1:  # +1 index to make sure the last image gets used
                self.frame_counter = 0


