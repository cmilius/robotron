import math
import pygame


class EnforcerProjectiles(pygame.sprite.Sprite):
    def __init__(self, game, p_type, pos):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.p_type = p_type
        self.pos = pos

        self.image = self.game.assets[self.p_type]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 13, 13)

        self.frame_movement = self.fire_to_target(target_pos=(self.game.hero.rect[0], self.game.hero.rect[1]))
        self.h_wall = False  # horizontal collision detection
        self.v_wall = False  # vertical collision detection

    def fire_to_target(self, target_pos, scaler=2):
        """
        Fire the projectile at the hero entity.

        :param target_pos: [x, y] position for the projectile to fire at
        :param float scaler: Scales how fast the projectile moves
        :return: None
        """
        target_pos = list(target_pos)

        # Determine the entity_position
        e_pos = (self.pos[0], self.pos[1])

        frame_movement = [0, 0]  # init

        # The vector needs to be scaled down to the appropriate speed by the maximum of the difference in positions
        max_diff = max(abs(target_pos[0] - e_pos[0]), abs(target_pos[1] - e_pos[1]))
        frame_movement[0] = (target_pos[0] - e_pos[0]) / max_diff
        frame_movement[1] = (target_pos[1] - e_pos[1]) / max_diff

        # scale the movement, can be used later to increase difficulty if desired.
        return [frame_movement[0] * scaler,
                frame_movement[1] * scaler]

    def update(self):

        self.rect.x += self.frame_movement[0]
        self.rect.y += self.frame_movement[1]

        # projectiles move along walls until hitting the corner
        buffer = 2
        if (self.rect.left - buffer) < 0 or (self.rect.right + buffer) > self.game.display.get_width():
            self.v_wall = True
        if (self.rect.top - buffer) < 0 or (self.rect.bottom + buffer) > self.game.display.get_height():
            self.h_wall = True

        # if the projectile hits a corner, kill
        if self.h_wall and self.v_wall:
            self.kill()

        # if the projectile hits one of the walls, stop movement in that direction
        elif self.v_wall and not self.h_wall:
            self.frame_movement[0] = 0
        elif self.h_wall and not self.v_wall:
            self.frame_movement[1] = 0

        # prevent projectiles from appearing to sticking to the wall if the movement value is < 1
        if self.v_wall and self.frame_movement[1] < 1:
            self.frame_movement[1] = math.copysign(1, self.frame_movement[1])
        if self.h_wall and self.frame_movement[0] < 1:
            self.frame_movement[0] = math.copysign(1, self.frame_movement[0])

