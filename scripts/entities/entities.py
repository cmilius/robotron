import pygame
import logging
import random

logger = logging.getLogger(__name__)


class PhysicsEntity(pygame.sprite.Sprite):
    def __init__(self, game, e_type, pos, size):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.e_type = e_type
        self.pos = list(pos)
        self.size = size
        self.action = "idle"

        # initialize the images
        if self.e_type == "hero":
            self.image = self.game.hero_animations.animations[self.e_type][self.action][0]
        elif self.e_type == "mom" or self.e_type == "dad" or self.e_type == "mike":
            self.image = self.game.human_family_animations.animations[self.e_type][self.action][0]
        else:
            self.image = self.game.robotrons_animations.animations[self.e_type][self.action][0]

        # animation variables, see _animate() for more information
        self.robo_anim = [0, 1, 0, 2]  # controls the animation frames
        self.frame = 0  # indexes the robo_anim list
        self.buffer_length = 20  # the time delay before the frame index will cycle
        self.buffer = 0  # the counter for buffer, will count to the buffer_length then cycle
        self.anim_length = len(self.robo_anim)  # The number of frames in the animation

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, movement=(0, 0)):
        """
        Update the physics entity movement.

        :param movement: Movement in (x, y). Default (0, 0)
        :return: None
        """
        self.move_entity(movement=movement)

    def _animate(self, entity=None):
        """
        Update the animation frames.
        There are two counters, the buffer and the frame. The buffer is the length of time in game frames, while the
        frame is the index of the animation.
        :param str entity: Type of entity, only required if == "grunt"
        :return: None
        """
        if entity == "grunt":
            # the grunt already moves on a "delay", so no buffer is required.
            self.frame += 1
            if self.frame == self.anim_length:
                self.frame = 0
            return
        self.buffer += 1
        if self.buffer_length == self.buffer:
            self.buffer = 0
            self.frame += 1
            if self.frame == self.anim_length:
                self.frame = 0

    def move_entity(self, movement=(0, 0)):
        frame_movement = [movement[0], movement[1]]

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        # update animations
        if self.e_type == "hero":
            # hero logic is handled in the Hero class
            pass
        elif self.e_type == "mom" or self.e_type == "dad" or self.e_type == "mike":
            self._animate()
            if frame_movement[0] > 0:
                self.action = "walk_right"
            elif frame_movement[0] < 0:
                self.action = "walk_left"
            if frame_movement[1] > 0 and not frame_movement[0]:
                self.action = "walk_down"
            elif frame_movement[1] < 0 and not frame_movement[0]:
                self.action = "walk_up"
            self.image = self.game.human_family_animations.animations[self.e_type][self.action][self.robo_anim[self.frame]]
        else:
            if self.e_type == "grunt":
                if frame_movement[0] or frame_movement[1]:
                    self.action = "walk"
                    self._animate("grunt")
                self.image = self.game.robotrons_animations.animations[self.e_type][self.action][self.robo_anim[self.frame]]
            if self.e_type == "hulk":
                self._animate()
                if frame_movement[0] == 0 and frame_movement[1] != 0:
                    self.action = "walk_vertical"
                elif frame_movement[0] > 0:
                    self.action = "walk_right"
                elif frame_movement[0] < 0:
                    self.action = "walk_left"
                self.image = self.game.robotrons_animations.animations[self.e_type][self.action][self.robo_anim[self.frame]]

    def direction_to_target(self, target_pos):
        """
        Given a target position, return a vector torwards that position.
        :return: (x, y) vector
        """
        target_pos = list(target_pos)
        # Determine the entity_position
        e_pos = (self.rect.x, self.rect.y)

        frame_movement = [0, 0]  # init

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

        return frame_movement

    def move_to_target(self, target_pos, movement=(0, 0), scaler=1, move_dir=None):
        """
        Move the entity torward the target.

        :param target_pos: [x, y] position for the entity to move torwards
        :param movement: default movement (0, 0)
        :param float scaler: Scales how fast the enemy moves in relation to the target.
        :param str or None move_dir: "x" or "y". Selects which direction the entity will move in.
        :return: None
        """
        target_pos = list(target_pos)

        frame_movement = list(self.direction_to_target(target_pos))

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

    def reached_target(self, target_pos):
        """
        Determine if the entity has reached it's target position within a given tolerance.
        If target reached, return new target_pos. Else, return the same target_pos
        :param target_pos: Target entity position
        :return: [x, y]
        """
        if abs(self.pos[0] - target_pos[0]) < 2\
                and abs(self.pos[1] - target_pos[1]) < 2:
            # calculate new target posit
            target_pos = self.random_movement()
        return target_pos

    def random_movement(self):
        """
        Pick a new position for the hulk to travel to.

        :return: [x, y]
        """
        posit = [random.choice(range(self.game.display.get_width())),
                 random.choice(range(self.game.display.get_height()))]
        return posit

    def hit_by_projectile(self):
        """
        Default enemy behaviour from being hit by a hero projectile is to remove it from groups with kill()

        :return: None
        """
        self.kill()


