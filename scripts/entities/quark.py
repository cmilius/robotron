from scripts.entities.pregnant_enemy import PregnantEnemy
from scripts.projectiles.enforcer_projectiles import EnforcerProjectiles
import logging

logger = logging.getLogger(__name__)


class Quark(PregnantEnemy):
    """
    Quarks move in a frandom pattern and drops off a single tank.
    """

    def __init__(self, game, pos, size):
        super().__init__(game, "quark", pos, size)  # inheret from PhysicsEntity class

    def update(self, movement=(0, 0)):
        """
        Move the quark.

        :param movement: Movement in (x, y). Default (0, 0)
        :return: None
        """
        self.spawn_counter += 1

        if (self.spawn_time - self.spawn_counter <= 180) and not self.full_anim:
            self.full_anim = True  # used to stop this from setting the variable endlessly
            self.num_frames = 7  # use all the frames once close to spawning an entity

        # spawn tanks
        if self.spawn_counter == self.spawn_time:
            # spawn the tank
            # TODO


            self.kill()

        # if reached its target, calculate a new target
        self.target_posit = self.reached_target(target_pos=self.target_posit)
        super().move_to_target(target_pos=self.target_posit,
                               movement=movement,
                               scaler=1,
                               move_dir=None)
