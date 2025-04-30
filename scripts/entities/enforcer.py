from scripts.entities.entities import PhysicsEntity
from scripts.projectiles.enforcer_projectiles import EnforcerProjectiles
import logging

logger = logging.getLogger(__name__)


class Enforcer(PhysicsEntity):
    """
    Enforcers are spawn by spheroids, and fire projectiles at the hero while slowly moving in a random pattern.
    """

    def __init__(self, game, pos, size):
        super().__init__(game, "enforcer", pos, size)
        self.image = self.game.robotrons_animations.animations[self.e_type]["1"][0]

        self.projectile_reload = 0
        self.projectile_timer = 60  # fire rate

        self.target_posit = self.random_movement()

        self.block_actions = True  # block movement until the enforcer has fully spawned
        self.spawn_frames = 6  # the number of animations frames in the enforcer spawn
        self.frame_counter = 0
        self.anim_frame_delay = 0

    def fire_projectile(self):
        """
        Fire projectiles at the hero.

        :return: None
        """
        if not self.block_actions:
            projectile = EnforcerProjectiles(self.game, "enforcer_projectile", self.pos)
            self.game.enemy_projectiles.add(projectile)
            self.game.allsprites.add(projectile)

    def animate(self, frame_movement):
        """
        Given a list frame_movement, update the entity animations.

        :param list frame_movement: The direction vector the entity is moving in.
        :return: None
        """
        if self.block_actions:
            # spawn the enforcer
            self.anim_frame_delay += 1
            if self.anim_frame_delay == 30:
                self.iterate_animation_frames()
                # the enforcer dictionary is indexed by a number, indicating the current "frame" of the spawn
                # I did it this because each piece of the spawn changes size
                self.image = self.game.robotrons_animations.animations[self.e_type][str(self.frame_counter)][0]
                # TODO: extract the frame_size of the image to adjust the hitbox as the entity is spawning
                # self.rect = self.game.robotrons_animations.animations[self.e_type][]
                self.frame_counter += 1
                self.anim_frame_delay = 0
                if self.frame_counter == self.spawn_frames:
                    self.block_actions = False

    def update(self, movement=(0, 0)):
        if self.block_actions:
            # play the spawn-in animation for the enforcer
            self.animate([None])
        if not self.block_actions:
            # once the enforcer is fully spawned in, resume normal functions
            self.projectile_reload += 1
            if self.projectile_reload == self.projectile_timer:
                # fire torwards the player
                self.fire_projectile()
                self.projectile_reload = 0

            # if reached its target, calculate a new target
            self.target_posit = self.reached_target(target_pos=self.target_posit)

            super().move_to_target(target_pos=self.target_posit,
                               movement=movement,
                               scaler=.7,
                               move_dir=None)
