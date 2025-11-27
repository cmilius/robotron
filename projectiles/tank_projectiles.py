import pygame

#CONSTANTS
DEFAULT_PROJECTILE_SCALER = 2  # How fast the projectile moves
ALIVE_TIMER = 600  # frames, how long the projectile will stay alive. After this, kill() projectile

class TankProjectiles(pygame.sprite.Sprite):
    def __init__(self, game, p_type, pos):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.p_type = p_type
        self.pos = pos

        self.image = self.game.assets[self.p_type]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 10, 10)

        self.frame_movement = self.fire_to_target(target_pos=(self.game.hero.rect[0], self.game.hero.rect[1]))
        self.h_wall = False  # horizontal collision detection
        self.v_wall = False  # vertical collision detection

        self.alive_timer = ALIVE_TIMER

        # These delays are to prevent the projectile from getting stuck against the wall on a bounce
        self.flip_delay_h = 0
        self.flip_delay_v = 0

    def fire_to_target(self, target_pos, scaler=DEFAULT_PROJECTILE_SCALER):
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
        """
        The tank projectile should bounce off walls and last for 5 seconds.

        :return: None
        """
        # Remove the projectile after a period of time.
        self.alive_timer -= 1
        if self.alive_timer <= 0:
            self.kill()

        # Delay the bounce off walls to prevent the projectile from getting stuck in a loop
        if self.flip_delay_h > 0:
            self.flip_delay_h -= 1
        if self.flip_delay_v > 0:
            self.flip_delay_v -= 1

        # Update the position of the projectile
        self.rect.x += self.frame_movement[0]
        self.rect.y += self.frame_movement[1]

        # projectiles bounce off of walls
        buffer = 2
        if self.rect.left + buffer < self.game.active_area.left:
            self.v_wall = True
        if self.rect.right + buffer > self.game.active_area.right:
            self.v_wall = True
        if self.rect.top + buffer < self.game.active_area.top:
            self.h_wall = True
        if self.rect.bottom + buffer > self.game.active_area.bottom:
            self.h_wall = True

        # if the projectile hits one of the walls, flip the movement in that direction
        if self.v_wall and not self.flip_delay_v:
            self.frame_movement[0] *= -1
            self.flip_delay_v = 60
            self.v_wall = False
        if self.h_wall and not self.flip_delay_h:
            self.frame_movement[1] *= -1
            self.flip_delay_h = 60
            self.h_wall = False

