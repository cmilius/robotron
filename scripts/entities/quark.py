from scripts.entities.entities import PhysicsEntity
from scripts.projectiles.enforcer_projectiles import EnforcerProjectiles
import logging

logger = logging.getLogger(__name__)


class Quark(PhysicsEntity):
    """
    Quarks move in a frandom pattern and drops off a single tank.
    """

    def __init__(self, game, pos, size):
        super().__init__(game, "quark", pos, size)
        self.image = self.game.robotrons_animations.animations[self.e_type][self.action][0]

        self.target_posit = self.random_movement()

    def update(self, movement=(0, 0)):
        # if reached its target, calculate a new target
        self.target_posit = self.reached_target(target_pos=self.target_posit)

        super().move_to_target(target_pos=self.target_posit,
                           movement=movement,
                           scaler=1,
                           move_dir=None)
