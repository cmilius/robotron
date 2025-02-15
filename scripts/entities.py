import pygame
import random
import logging

logger = logging.getLogger(__name__)


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        """
        Generates an entity that can interact with other entities and elements in the world.

        :param game: pygame object
        :param str e_type: entity type. Should match the asset.
        :param tuple pos: position on the screen
        :param tuple size: pixel size of the element
        """
        self.game = game
        self.e_type = e_type
        self.pos = list(pos)  # convert any iterable into a list, so multiple entities will be handled seperately
        self.size = size

    def rect(self):
        """
        Return the rectangle that defines the shape of this entity. Used for collision detection.

        :return: pygame.Rect
        """
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, movement=(0, 0)):
        """
        Update the physics entity movement.

        :param movement: Movement in (x, y). Default (0, 0)
        :return: None
        """
        frame_movement = (movement[0], movement[1])

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]

    def render(self, surf):
        """
        Render the physics object onto the provided surface. Uses self.e_type to match an asset from the Game class.

        :param surf: Pygame surface
        :return: None
        """
        surf.blit(self.game.assets[self.e_type], self.pos)


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, "player", pos, size)  # inheret the PhysicsEntity class

    def update(self, movement=(0, 0)):
        super().update(movement=movement)


class Robot(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, "robot", pos, size)  # inheret the PhysicsEntity class

    def update(self, movement=(0, 0)):
        """
        The robot should slowly move torwards the player entity.

        :param movement: Movement in (x, y). Default (0, 0)
        :return: None
        """
        # Determine player location and robot location
        player_pos = self.game.player.rect()
        robot_pos = self.rect()

        frame_movement = [movement[0], movement[1]]

        # x-movement logic
        if player_pos[0] > robot_pos[0]:
            frame_movement[0] = 1
        elif player_pos[0] < robot_pos[0]:
            frame_movement[0] = -1
        # y-movement logic
        if player_pos[1] > robot_pos[1]:
            frame_movement[1] = 1
        elif player_pos[1] < robot_pos[1]:
            frame_movement[1] = -1

        # scale the movement, can be used later to increase difficulty if desired.
        # Throw in random.random() so the robots have slightly various movespeeds.
        # This also stops them from instantly merging.
        frame_movement = [frame_movement[0] * .7 * random.random(),
                          frame_movement[1] * .7 * random.random()]

        super().update(movement=frame_movement)

