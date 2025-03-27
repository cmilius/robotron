from robotron.scripts.entities.entities import PhysicsEntity
from robotron.scripts.projectiles.enforcer_projectiles import EnforcerProjectiles
import logging

logger = logging.getLogger(__name__)


class Enforcer(PhysicsEntity):
    """
    Enforcers are spawn by spheroids, and fire projectiles at the hero while slowly moving in a random pattern.
    """

    def __init__(self, game, pos, size):
        super().__init__(game, "enforcer", pos, size)

        self.projectile_reload = 0
        self.projectile_timer = 60  # fire rate

        self.target_posit = self.random_movement()

    def fire_projectile(self):
        """
        Fire projectiles at the hero
        :return: None
        """
        hero_position = [self.game.hero.rect[0], self.game.hero.rect[1]]

        fire_direction = list(self.direction_to_target(hero_position))

        projectile = EnforcerProjectiles(self.game, "enforcer_projectile", self.pos, fire_direction)
        self.game.enemy_projectiles.add(projectile)
        self.game.allsprites.add(projectile)

    def update(self, movement=(0, 0)):
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
