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

        # TODO: need a way to limit the input to only 2.
        # I think some kind of variable to hold the last valid input.

        # Shoot West
        if self.direction[0] and not (self.direction[1] or self.direction[2] or self.direction[3]):
            self.rect.x -= projectile_speed
        # Shoot East
        if self.direction[1] and not (self.direction[0] or self.direction[2] or self.direction[3]):
            self.rect.x += projectile_speed
        # Shoot North
        if self.direction[2] and not (self.direction[0] or self.direction[1] or self.direction[3]):
            self.rect.y -= projectile_speed
        # Shoot South
        if self.direction[3] and not (self.direction[0] or self.direction[1] or self.direction[2]):
            self.rect.y += projectile_speed
        # Shoot Northeast
        if self.direction[1] and self.direction[2] and not (self.direction[0] or self.direction[3]):
            self.rect.x += projectile_speed
            self.rect.y -= projectile_speed
        # Shoot Northwest
        if self.direction[0] and self.direction[2] and not (self.direction[1] or self.direction[3]):
            self.rect.x -= projectile_speed
            self.rect.y -= projectile_speed
        # Shoot Southeast
        if self.direction[1] and self.direction[3] and not (self.direction[0] or self.direction[2]):
            self.rect.x += projectile_speed
            self.rect.y += projectile_speed
        # Shoot Southwest
        if self.direction[0] and self.direction[3] and not (self.direction[1] or self.direction[2]):
            self.rect.x -= projectile_speed
            self.rect.y += projectile_speed

        # Once the projectile leaves the map, kill
        if self.rect.left < 0 \
                or self.rect.right > self.game.display.get_width() \
                or self.rect.top > self.game.display.get_height() \
                or self.rect.bottom < 0:
            self.kill()

