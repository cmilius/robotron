import pygame
import random

# CONSTANTS
SPEED = 1                   # Scales how fast the projectile moves
DIRECTION_MAX_FRAMES = 20   # max number of frames before a direction change

class BrainProjectile(pygame.sprite.Sprite):
    def __init__(self, game, p_type, pos):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.pos = pygame.math.Vector2(pos)

        self.image = self.game.assets[p_type]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 13, 13)

        # self.frame_movement = self.fire_to_target(target_pos=(self.game.hero.rect[0], self.game.hero.rect[1]))

        self.frame_counter = DIRECTION_MAX_FRAMES
        self.frame_max = DIRECTION_MAX_FRAMES

        self.target_pos = [self.game.hero.rect[0], self.game.hero.rect[1]]

    def update(self):

        if self.frame_counter < self.frame_max:
            # continue in the same direction
            self.frame_counter += 1
        else:
            # Decide randomly whether to home in on the player or go to a random position
            if random.choice([True, False]):
                self.target_pos = [self.game.hero.rect[0], self.game.hero.rect[1]]
            else:
                x = random.randint(self.game.active_area.left, self.game.active_area.right)
                y = random.randint(self.game.active_area.top, self.game.active_area.bottom)
                self.target_pos = [x, y]

            # Calcualate the number of frames the projectile will move
            self.frame_max = random.randint(0, DIRECTION_MAX_FRAMES) 
            self.frame_counter = 0

        # Move towards the target position
        direction_vector = pygame.math.Vector2(self.target_pos[0] - self.pos[0],
                                               self.target_pos[1] - self.pos[1])
        if direction_vector.length() != 0:
            direction_vector = direction_vector.normalize() * SPEED
            self.pos += direction_vector
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))