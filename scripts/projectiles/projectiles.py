import pygame


class Projectiles(pygame.sprite.Sprite):
    def __init__(self, game, p_type, pos, direction):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.p_type = p_type
        self.pos = pos
        self.direction = direction
        # If the projectile is going up or down, rotate the image.
        if self.direction[2] or self.direction[3]:
            self.image = pygame.transform.rotate(self.game.assets[self.p_type], 90)
        else:
            self.image = self.game.assets[self.p_type]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 6, 4)

    def update(self):
        projectile_speed = 8

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

