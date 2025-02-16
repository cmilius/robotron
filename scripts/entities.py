import pygame
import random
import logging

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
        frame_movement = [movement[0], movement[1]]

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


class Hero(PhysicsEntity):
    def __init__(self, game, pos, size):
        self.game = game
        self.pos = pos
        self.size = size
        super().__init__(self.game, "hero", self.pos, self.size)


class Grunt(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, "grunt", pos, size)  # inheret the PhysicsEntity class

    def update(self, movement=(0, 0)):
        """
        The grunt should slowly move torwards the hero entity.

        :param movement: Movement in (x, y). Default (0, 0)
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
        scaler = 2
        frame_movement = [frame_movement[0] * scaler,
                          frame_movement[1] * scaler]

        super().update(movement=frame_movement)

class Hulk(PhysicsEntity):
    """
        Large, indestructible robots that wander the screen, killing humans and trapping the player.
    """

    def __init__(self, game, pos, size):
        super().__init__(game, "hulk", pos, size)  # inheret the PhysicsEntity class

    def update(self, movement=(0, 0)):
        """
        Moves the hulk

        :param movement: Movement in (x, y). Default (0, 0)
        :return: None
        """

        # Determine player's location and your location
        player_pos = self.game.player.rect()
        hulk_pos = self.rect()

        frame_movement = [movement[0], movement[1]]

        # x-movement logic
        if player_pos[0] > hulk_pos[0]:
            frame_movement[0] = 1
        elif player_pos[0] < hulk_pos[0]:
            frame_movement[0] = -1
            
        # y-movement logic
        if player_pos[1] > hulk_pos[1]:
            frame_movement[1] = 1
        elif player_pos[1] < hulk_pos[1]:
            frame_movement[1] = -1

        # scale the movement, can be used later to increase difficulty if desired.
        # Throw in random.random() so the hulks have slightly various movespeeds.
        # This also stops them from instantly merging.
        frame_movement = [frame_movement[0] * .5 * random.random(),
                          frame_movement[1] * .5 * random.random()]

        super().update(movement=frame_movement)
