import pygame
import random
import logging
from .projectiles import Projectiles

logger = logging.getLogger(__name__)


class PhysicsEntity(pygame.sprite.Sprite):
    def __init__(self, game, e_type, pos, size):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.e_type = e_type
        self.pos = list(pos)
        self.size = size

        self.image = self.game.assets[self.e_type]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, movement=(0, 0)):
        """
        Update the physics entity movement.

        :param movement: Movement in (x, y). Default (0, 0)
        :return: None
        """
        self.move_entity(movement=movement)

    def move_entity(self, movement=(0, 0)):
        frame_movement = [movement[0], movement[1]]

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def move_to_hero(self, movement=(0, 0), scaler=1):
        """
        Move the entity torward the hero.

        :param movement: default movement (0, 0)
        :param float scaler: Scales how fast the enemy moves in relation to the player.
        :return: None
        """
        # Determine hero location and grunt location
        hero_pos = (self.game.hero.rect.x, self.game.hero.rect.y)
        grunt_pos = (self.rect.x, self.rect.y)

        frame_movement = [movement[0], movement[1]]

        # x-movement logic
        if hero_pos[0] > grunt_pos[0]:
            frame_movement[0] = 1
        elif hero_pos[0] < grunt_pos[0]:
            frame_movement[0] = -1
        # y-movement logic
        if hero_pos[1] > grunt_pos[1]:
            frame_movement[1] = 1
        elif hero_pos[1] < grunt_pos[1]:
            frame_movement[1] = -1

        # scale the movement, can be used later to increase difficulty if desired.
        frame_movement = [frame_movement[0] * scaler,
                          frame_movement[1] * scaler]

        self.move_entity(movement=frame_movement)

    def move_to_center(self):
        """
        Move the entity to the center of the screen.

        :return: None
        """
        cent_y = self.game.display.get_height() // 2
        cent_x = self.game.display.get_width() // 2
        hero_x = self.rect.x
        hero_y = self.rect.y
        self.move_entity(movement=[cent_x-hero_x, cent_y-hero_y])


class Hero(PhysicsEntity):
    def __init__(self, game, pos, size):
        self.game = game
        self.pos = list(pos)
        self.size = size
        super().__init__(self.game, "hero", self.pos, self.size)
        self.projectile_reload = 20  # frames
        self.projectile_timer = 10  # count up to projectile reload

        # used to track the last pressed keys for shooting
        self.h_stack = []
        self.v_stack = []

    def update(self, movement=(0, 0), shooting=(False, False, False, False)):
        super().update(movement=movement)

        self.shooting = list(shooting)
        # Find out which key was last pressed by the hero
        if self.shooting[0] and "left" not in self.h_stack:
            self.h_stack.append("left")
        elif not self.shooting[0] and "left" in self.h_stack:
            self.h_stack.remove("left")
        if self.shooting[1] and "right" not in self.h_stack:
            self.h_stack.append("right")
        elif not self.shooting[1] and "right" in self.h_stack:
            self.h_stack.remove("right")
        if self.h_stack:
            if self.h_stack[-1] == "left":
                self.shooting[0] = True
                self.shooting[1] = False
            else:
                self.shooting[0] = False
                self.shooting[1] = True
        if self.shooting[2] and "up" not in self.v_stack:
            self.v_stack.append("up")
        elif not self.shooting[2] and "up" in self.v_stack:
            self.v_stack.remove("up")
        if self.shooting[3] and "down" not in self.v_stack:
            self.v_stack.append("down")
        elif not self.shooting[3] and "down" in self.v_stack:
            self.v_stack.remove("down")
        if self.v_stack:
            if self.v_stack[-1] == "up":
                self.shooting[2] = True
                self.shooting[3] = False
            else:
                self.shooting[2] = False
                self.shooting[3] = True

        # only fire if the gun is reloaded
        if self.projectile_timer != self.projectile_reload:
            self.projectile_timer += 1
        if True in self.shooting and (self.projectile_timer == self.projectile_reload):
            projectile = Projectiles(self.game, "projectile", self.pos, self.shooting)
            self.game.hero_projectiles.add(projectile)
            self.game.allsprites.add(projectile)
            self.projectile_timer = 0  # cooldown to the projectile_reload framecount


class Grunt(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, "grunt", pos, size)  # inheret the PhysicsEntity class
        self.movement_timer = 0
        self.move_at_time = 20

    def update(self, movement=(0, 0)):
        """
        The grunt should slowly move torwards the hero entity.

        :param movement: Movement in (x, y). Default (0, 0)
        :return: None
        """
        self.movement_timer += 1
        if self.movement_timer == self.move_at_time:
            super().move_to_hero(movement=movement, scaler=3)
            self.movement_timer = 0

    def hit_by_projectile(self):
        self.kill()
        # TODO: add to score


class Hulk(PhysicsEntity):
    """
        Large, indestructible robots that wander the screen, killing humans and trapping the player.
    """

    def __init__(self, game, pos, size):
        super().__init__(game, "hulk", pos, size)  # inheret the PhysicsEntity class
        self.slowed_timer = 300
        self.timer = 300

    def update(self, movement=(0, 0)):
        """
        Moves the hulk

        :param movement: Movement in (x, y). Default (0, 0)
        :return: None
        """
        if self.timer == self.slowed_timer:
            movement_scaler = .3
        else:
            movement_scaler = .1
            self.timer += 1
        super().move_to_hero(movement=movement, scaler=movement_scaler)

    def hit_by_projectile(self):
        """
        Slows down the hulk.
        :return: None
        """
        self.timer = 0
