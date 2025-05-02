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

        self.number_of_children = random.randint(2, 5)
        self.pause_mvmt = False  # pause the movement briefly when spawning an enforcer
        self.pause_timer = 0
        self.pause_limit = 60  # pause for 1 second

    def update(self, movement=(0, 0)):
        """
        Move the spheroid. # TODO: how to keep it near the edges

        :param movement: Movement in (x, y). Default (0, 0)
        :return: None
        """
        self.spawn_counter += 1  # 'countdown' clock for spawning enforcers

        if self.pause_mvmt:
            # spheroid pauses movement before/during/after spawning enforcer. This handles the pause countdown logic
            self.pause_timer += 1
            if self.pause_timer == self.pause_limit:
                self.pause_mvmt = False
                self.pause_timer = 0

        # Once the spheroid is close to spawning an enforcer, start playing the full animation
        if (self.spawn_time - self.spawn_counter <= 180) and not self.full_anim:
            self.full_anim = True  # used to stop this from setting the variable endlessly
            self.num_frames = 7  # use all the frames once close to spawning an entity

        # when the spheroid is about to spawn an enforcer, stop movement
        if (self.spawn_time - self.spawn_counter) <= 30:
            self.pause_mvmt = True

        # spawn enforcers
        if self.spawn_counter == self.spawn_time:
            # spawn the enforcer
            # TODO: tried to spawn it in the center of the spheroid,
            #  but this still needs some tweaking due to top-left nature of pygame
            enforcer = Enforcer(self.game, (self.pos[0]+self.game.enforcer_size[0]/2,
                                            self.pos[1]+self.game.enforcer_size[1]/2),
                                self.game.enforcer_size)
            self.game.enemy_group.add(enforcer)
            self.game.allsprites.add(enforcer)

            # spheroid logic
            self.number_of_children -= 1
            if self.number_of_children == 0:
                self.kill()
            self.spawn_counter = 0
            self.spawn_time = random.randint(120, 360)  # speed up the spawn times

        # if reached its target, calculate a new target
        self.target_posit = self.reached_target(target_pos=self.target_posit)

        if not self.pause_mvmt:
            super().move_to_target(target_pos=self.target_posit,
                                   movement=movement,
                                   scaler=.7,
                                   move_dir=None)
        else:
            # move_entity with default 0 movement called, to pause movement while still updating animations
            super().move_entity()

