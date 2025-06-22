from scripts.entities.entities import PhysicsEntity
from pygame import transform
import logging

logger = logging.getLogger(__name__)

# CONSTANTS
FIRE_RATE = 60  # frames, fires every second
TANK_SPEED_SCALER = 0.4  # Scales the speed of the tank


class Tank(PhysicsEntity):
    """
    Tanks are spawn by quarks, and fire bouncing projectiles at the hero while slowly moving in a random pattern.
    """

    def __init__(self, game, pos, size):
        super().__init__(game, "tank", pos, size)
        self.image = self.game.robotrons_animations.animations[self.e_type]["0"][0]
        self.spawn_frames = 4  # dictated by the spritesheet

        # override default animation logic
        self.anim_flipbook = [0, 1, 2, 3]  # dictated by the spritesheet
        self.flipbook_index = 0

        self.projectile_reload = 0
        self.projectile_timer = FIRE_RATE

        self.target_posit = self.random_movement()

    def animate(self, frame_movement):
        """
        Given a list frame_movement, update the entity animations.

        :param list frame_movement: The direction vector the entity is moving in.
        :return: None
        """
        if self.block_actions:
            super().spawn_animation()

    def update(self, movement=(0, 0)):
        if self.block_actions:
            # play the spawn-in animation for the enforcer
            self.animate([None])
        if not self.block_actions:
            # once the enforcer is fully spawned in, resume normal functions

            # update the tank animation
            self.iterate_animation_frames()

            # switch the image based on x-movement, to have the tank treads move the correct direction
            if self.pos[0] - self.target_posit[0] <= 0:
                # moving left to right
                self.image = self.game.robotrons_animations.animations[self.e_type]["walk"][
                    self.anim_flipbook[self.flipbook_index]]
            else:
                self.image = transform.flip(self.game.robotrons_animations.animations[self.e_type]["walk"][
                    self.anim_flipbook[self.flipbook_index]], True, False)

            # TODO: projectiles

            # if reached its target, calculate a new target
            self.target_posit = self.reached_target(target_pos=self.target_posit)

            super().move_to_target(target_pos=self.target_posit,
                               movement=movement,
                               scaler=TANK_SPEED_SCALER,
                               move_dir=None)
