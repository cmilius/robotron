from scripts.entities.entities import PhysicsEntity
import logging

logger = logging.getLogger(__name__)

class Prog(PhysicsEntity):
    """
    Progs are spawn by spheroids, and fire projectiles at the hero while slowly moving in a random pattern.
    """

    def __init__(self, game, pos, size):
        super().__init__(game, self.__class__.__name__.lower(), pos, size)
        self.animations = self.game.human_family_animations.animations[self.e_type] # they were originally humans
        self.image = self.animations[self.action][0] 

        self.target_posit = self.random_movement()

        self.block_actions = True  # block movement until the prog has fully spawned
        self.spawn_frames = 6  # the number of animations frames in the prog spawn
        self.frame_counter = 0
        self.anim_frame_delay = 0

    def animate(self, frame_movement):
        """
        Given a list frame_movement, update the entity animations.

        :param list frame_movement: The direction vector the entity is moving in.
        :return: None
        """

    def update(self, movement=(0, 0)):
        # if reached its target, calculate a new target
        self.target_posit = self.reached_target(target_pos=self.target_posit)

        super().move_to_target(target_pos=self.target_posit,
                            movement=movement,
                            scaler=.7,
                            move_dir=None)
