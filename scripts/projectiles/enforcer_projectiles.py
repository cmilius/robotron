import pygame


class EnforcerProjectiles(pygame.sprite.Sprite):
    def __init__(self, game, p_type, pos):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.p_type = p_type
        self.pos = pos

        self.image = self.game.assets[self.p_type]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.game.enforcer_size[0], self.game.enforcer_size[1])

        self.frame_movement = self.fire_to_target(target_pos=(self.game.hero.rect[0], self.game.hero.rect[1]))

    def fire_to_target(self, target_pos, scaler=2):
        """
        Move the entity torward the target.

        :param target_pos: [x, y] position for the entity to move torwards
        :param float scaler: Scales how fast the enemy moves in relation to the target.
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

        # Once the projectile leaves the map, kill
        if self.rect.left < 0 \
                or self.rect.right > self.game.display.get_width() \
                or self.rect.top > self.game.display.get_height() \
                or self.rect.bottom < 0:
            self.kill()
