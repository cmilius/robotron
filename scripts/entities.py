import pygame
import logging

logger = logging.getLogger(__name__)


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        """
        Generates an entity that can interact with other entities and elements in the world.

        :param game: pygame object
        :param str e_type: entity type
        :param tuple pos: position on the screen
        :param tuple size: pixel size of the element
        """
        self.game = game
        self.type = e_type
        self.pos = list(pos)  # convert any iterable into a list, so multiple entities will be handled seperately
        self.size = size

    def update(self, movement=(0, 0)):
        """
        Udate the physics entity movement.

        :param movement: Movement in (x, y). Default (0, 0)
        :return: None
        """
        frame_movement = (movement[0], movement[1])

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]

    def render(self, surf):
        """
        Render the physics object onto the provided surface.

        :param surf: Pygame surface
        :return: None
        """
        surf.blit(self.game.assets["player"], self.pos)
