import sys
import pygame
import logging

from scripts.entities import Hero, Grunt
from scripts.spawner import Spawner
from scripts.utils import load_image, load_images

logging.basicConfig(format='%(name)s %(levelname)s %(asctime)s %(module)s (line: %(lineno)d) -- %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("robotron")
        self.screen = pygame.display.set_mode((640, 480))  # Top-left is 0-0
        # Put assets onto the display. Display will then be projected onto the screen for a more pixel-art look.
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.movement = [0, 0]  # [x, y]

        self.assets = {
            "hero": load_image("entities/hero.png"),
            "grunt": load_image("entities/grunt.png")
        }

        # init wave counter
        self.wave_counter = 1

        self.allsprites = pygame.sprite.Group()

        # Create the hero
        self.hero_size = (20, 27)  # pixel size
        self.hero = Hero(self, (150, 106.5), self.hero_size)
        self.hero_group = pygame.sprite.Group()
        self.hero_group.add(self.hero)
        self.allsprites.add(self.hero)

        # Spawn grunts
        self.grunt_size = (29, 27)  # pixel size
        # TODO: below will be eventually be moved to a "start wave" function
        self.grunts_group = pygame.sprite.Group()
        self.spawner = Spawner(self)
        self.grunt_positions = self.spawner.grunt_spawn()
        for pos in self.grunt_positions:
            grunt = Grunt(self, pos, self.grunt_size)
            self.grunts_group.add(grunt)
            self.allsprites.add(grunt)

    def run(self):
        grunt_move_timer = 0
        while True:
            self.display.fill((0, 0, 0))  # black background

            # hero functions
            self.hero.update((self.movement[0], self.movement[1]))

            # grunt functions
            grunt_move_timer += 1
            if grunt_move_timer == 20:
                self.grunts_group.update()
                grunt_move_timer = 0

            # draw sprites
            self.allsprites.draw(self.display)

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
