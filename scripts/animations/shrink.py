import pygame

class ShrinkAnimations:
    def __init__(self, game, sprite):
        """
        Container for the shrink animation. Given a sprite, get the image, location, and size.
        Then call the shrink function to reduce the sprite image over a period of time.

        :param game: pygame
        :param sprite: the affected sprite that will be shrunk
        """
        self.game = game
        self.sprite = sprite
        self.surf = sprite.image
        self.pos_x = self.sprite.pos[0]
        self.pos_y = self.sprite.pos[1]

        self.orig_size = self.surf.get_size() # get the original size of the image
        self.start_time = pygame.time.get_ticks()
        self.duration = 1000  # duration of animation in ms
        self.finished = False

    def shrink(self):
        """
        Continually shrink the surface over a period of time.

        :return: None
        """
        now = pygame.time.get_ticks()
        elapsed = now - self.start_time
        # Normalized time (0 to 1) over the duration.
        t = min(elapsed / self.duration, 1.0)
        scaler = t * 100  # scale up the time from 0 to 100, for the percentage value

        self.finished = t >= 1.0

        shrink_ratio = (100-scaler)/100  # turn the time into a decimal
        surf = pygame.transform.scale(self.surf, (shrink_ratio*self.orig_size[0], shrink_ratio*self.orig_size[1]))
        self.game.display.blit(surf, (self.pos_x, self.pos_y))