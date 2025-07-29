import math
import pygame


# CONSTANTS
DEFAULT_SCALER = 2  # Scales how fast the projectile moves
SLOWED_TIMER = 3  # number of seconds the slow rate occur over
FRAME_COUNTER = 20  # number of frames before each SLOW_RATE is applied
SLOW_RATE = 0.8  # the rate that the projectile speed should be reduced by

class EnforcerProjectiles(pygame.sprite.Sprite):
    def __init__(self, game, p_type, pos):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.p_type = p_type
        self.pos = pygame.math.Vector2(pos)

        self.image = self.game.assets[self.p_type]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 13, 13)

        self.frame_movement = self.fire_to_target(target_pos=(self.game.hero.rect[0], self.game.hero.rect[1]))
        self.h_wall = False  # horizontal collision detection
        self.v_wall = False  # vertical collision detection

        self.slowed_timer = SLOWED_TIMER
        self.slow_rate = SLOW_RATE
        self.frame_counter = FRAME_COUNTER

    def fire_to_target(self, target_pos, scaler=DEFAULT_SCALER):
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
        return pygame.math.Vector2(frame_movement[0] * scaler,
                                   frame_movement[1] * scaler)

    def update(self):

        # Calculate the new speed of the projectile based on time components
        # the projectile should smoothly slow down a certain amount after being fired.
        if self.slowed_timer >= 0:
            if self.frame_counter >= 0:
                self.frame_counter -= 1
            else:
                self.frame_movement *= self.slow_rate
                self.frame_counter = FRAME_COUNTER
                self.slowed_timer -= 1

        # Calculate the new position using float math to account for small changes, then round for Rect logic
        self.pos += self.frame_movement
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        # projectiles move along walls until hitting the corner
        buffer = 2
        if self.rect.left + buffer < self.game.active_area.left:
            self.v_wall = True
        if self.rect.right + buffer > self.game.active_area.right:
            self.v_wall = True
        if self.rect.top + buffer < self.game.active_area.top:
            self.h_wall = True
        if self.rect.bottom + buffer > self.game.active_area.bottom:
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

