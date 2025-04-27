from scripts.entities.enforcer import Enforcer
from scripts.entities.pregnant_enemy import PregnantEnemy
import random
import logging

logger = logging.getLogger(__name__)


class Spheroid(PregnantEnemy):
    """
    These enemies stay near the edges of the screen and generate Enforcers
    every few seconds. Eventually, they will vanish after
    dropping off so many Enforcer robots.
    """
    def __init__(self, game, pos, size):
        super().__init__(game, "spheroid", pos, size)  # inheret from PhysicsEntity class

    def update(self, movement=(0, 0)):
        """
        Move the spheroid. # TODO: how to keep it near the edges

        :param movement: Movement in (x, y). Default (0, 0)
        :return: None
        """
        self.spawn_counter += 1

        if (self.spawn_time - self.spawn_counter <= 180) and not self.full_anim:
            self.full_anim = True  # used to stop this from setting the variable endlessly
            self.num_frames = 7  # use all the frames once close to spawning an entity

        # spawn enforcers
        if self.spawn_counter == self.spawn_time:
            # spawn the enforcer
            enforcer = Enforcer(self.game, (self.pos[0], self.pos[1]), self.game.enforcer_size)
            self.game.enemy_group.add(enforcer)
            self.game.allsprites.add(enforcer)

            # spheroid logic
            self.number_of_children -= 1
            if self.number_of_children == 0:
                self.kill()
            self.spawn_counter = 0
            self.spawn_time = random.randint(60, 300)  # speed up the spawn times

        # if reached its target, calculate a new target
        self.target_posit = self.reached_target(target_pos=self.target_posit)
        super().move_to_target(target_pos=self.target_posit,
                               movement=movement,
                               scaler=.7,
                               move_dir=None)
