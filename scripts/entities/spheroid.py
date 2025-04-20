from scripts.entities.entities import PhysicsEntity
from scripts.entities.enforcer import Enforcer
import random
import logging

logger = logging.getLogger(__name__)


class Spheroid(PhysicsEntity):
    """
    These enemies stay near the edges of the screen and generate Enforcers
    every few seconds. Eventually, they will vanish after
    dropping off so many Enforcer robots.
    """
    def __init__(self, game, pos, size):
        super().__init__(game, "spheroid", pos, size)  # inheret from PhysicsEntity class
        self.image = self.game.robotrons_animations.animations[self.e_type][self.action][0]

        self.number_of_enforcers = random.randint(2, 5)

        self.target_posit = self.random_movement()
        self.spawn_counter = 0
        self.spawn_time = random.randint(60, 300)  # between 1 and 5 seconds.
        # If changed here, be sure to change in update() func as well

    def update(self, movement=(0, 0)):
        """
        Move the spheroid. # TODO: how to keep it near the edges

        :param movement: Movement in (x, y). Default (0, 0)
        :return: None
        """
        self.spawn_counter += 1

        # spawn enforcers
        if self.spawn_counter == self.spawn_time:
            # spawn the enforcer
            enforcer = Enforcer(self.game, (self.pos[0], self.pos[1]), self.game.enforcer_size)
            self.game.enemy_group.add(enforcer)
            self.game.allsprites.add(enforcer)

            # spheroid logic
            self.number_of_enforcers -= 1
            if self.number_of_enforcers == 0:
                self.kill()
            self.spawn_counter = 0
            self.spawn_time = random.randint(60, 300)

        # if reached its target, calculate a new target
        self.target_posit = self.reached_target(target_pos=self.target_posit)
        super().move_to_target(target_pos=self.target_posit,
                               movement=movement,
                               scaler=1,
                               move_dir=None)
