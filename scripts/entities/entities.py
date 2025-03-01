import pygame
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
        self.move_entity(movement=movement)

    def move_entity(self, movement=(0, 0)):
        frame_movement = [movement[0], movement[1]]

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def move_to_target(self, target_pos, movement=(0, 0), scaler=1, move_dir=None):
        """
        Move the entity torward the target.

        :param target_pos: [x, y] position for the entity to move torwards
        :param movement: default movement (0, 0)
        :param float scaler: Scales how fast the enemy moves in relation to the target.
        :param str move_dir: "x" or "y". Selects which direction the entity will move in.
        :return: None
        """
        target_pos = list(target_pos)
        # Determine the entity_position
        e_pos = (self.rect.x, self.rect.y)

        frame_movement = [movement[0], movement[1]]

        # x-movement logic
        if target_pos[0] > e_pos[0]:
            frame_movement[0] = 1
        elif target_pos[0] < e_pos[0]:
            frame_movement[0] = -1
        # y-movement logic
        if target_pos[1] > e_pos[1]:
            frame_movement[1] = 1
        elif target_pos[1] < e_pos[1]:
            frame_movement[1] = -1

        # scale the movement, can be used later to increase difficulty if desired.
        frame_movement = [frame_movement[0] * scaler,
                          frame_movement[1] * scaler]

        if move_dir is not None:
            if move_dir == "x":
                frame_movement[1] = 0
            elif move_dir == "y":
                frame_movement[0] = 0
            else:
                logger.warning(f"Movement direction input must be either 'x' or 'y'. Current input: {move_dir}")

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




