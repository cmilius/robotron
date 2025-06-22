import pygame
import logging

logger = logging.getLogger(__name__)

# CONSTANTS
PROJECTILE_SPEED = 16


class HeroProjectiles(pygame.sprite.Sprite):
    def __init__(self, game, p_type, pos, direction):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.p_type = p_type
        self.pos = pos
        self.direction = direction
        self.explode_logic = ["horizontal", False]  # [direction, mirror flag]

        # Rotate the image based on direction
        if (self.direction[0] or self.direction[1]) and (self.direction[2] or self.direction[3]) and not\
                (self.direction[0] + self.direction[1] + self.direction[2] + self.direction[3] == 1):
            self.image = pygame.transform.rotate(self.game.assets[self.p_type], 45)  # NorthEast, SouthWest
            self.explode_logic = ["diagonal", False]
            if (self.direction[0] and self.direction[2]) or (self.direction[1] and self.direction[3]):  # NorthWest, SouthEast
                self.image = pygame.transform.flip(self.image, True, False)
                self.explode_logic = ["diagonal", True]
        elif self.direction[2] or self.direction[3]:  # North, South
            self.image = pygame.transform.rotate(self.game.assets[self.p_type], 90)
            self.explode_logic = ["horizontal", False]
        else:  # East, West
            self.image = self.game.assets[self.p_type]
            self.explode_logic = ["vertical", False]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 6, 1)

    def update(self):
        projectile_speed = PROJECTILE_SPEED

        # Directions truth tables
        #     [True, False, True, False]: "Northwest"
        #     [True, False, False, True]: "Southwest"
        #     [False, True, True, False]: "Northeast"
        #     [False, True, False, True]: "Southeast"

        # dir[1] = east, dir[0] = west
        # dir[3] = north, dir[2] = south

        x_dir = (self.direction[1] - self.direction[0]) * projectile_speed
        y_dir = (self.direction[3] - self.direction[2]) * projectile_speed

        self.rect.x += x_dir
        self.rect.y += y_dir

        # Once the projectile leaves the map, kill
        if self.rect.left < 0 \
                or self.rect.right > self.game.display.get_width() \
                or self.rect.top > self.game.display.get_height() \
                or self.rect.bottom < 0:
            self.kill()

