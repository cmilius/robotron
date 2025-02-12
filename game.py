import sys
import pygame
import logging

from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_images

logging.basicConfig(format='%(name)s %(levelname)s %(asctime)s %(module)s (line: %(lineno)d) -- %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Robotron")
        self.screen = pygame.display.set_mode((640, 480))  # Top-left is 0-0
        # Put assets onto the display. Display will then be projected onto the screen for a more pixel-art look.
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.movement = [0, 0]  # [x, y]

        self.assets = {
            "player": load_image("entities/player.png")
        }

        # Create the player
        self.player = PhysicsEntity(self, "player", (50, 50), (20, 27))


    def run(self):
        while True:
            self.display.fill((0, 0, 0))  # black background

            # player functions
            self.player.update((self.movement[0], self.movement[1]))
            self.player.render(self.display)

            # event manager
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.movement[1] = -1
                    if event.key == pygame.K_s:
                        self.movement[1] = 1
                    if event.key == pygame.K_a:
                        self.movement[0] = -1
                    if event.key == pygame.K_d:
                        self.movement[0] = 1
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.movement[1] = 0
                    if event.key == pygame.K_s:
                        self.movement[1] = 0
                    if event.key == pygame.K_a:
                        self.movement[0] = 0
                    if event.key == pygame.K_d:
                        self.movement[0] = 0

            # Scale up the pixel art by bliting the smaller display onto the larger screen.
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)  # framerate


if __name__ == "__main__":
    Game().run()
