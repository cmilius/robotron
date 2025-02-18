import sys
import pygame
import logging

from scripts.entities import Hero, Grunt, Hulk
from scripts.spawner import Spawner
from scripts.utils import load_image, load_images
from scripts.hud import HUD

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
        self.hero_shooting = [False, False, False, False]  # [left, right, up, down]

        self.assets = {
            "hero": load_image("entities/hero.png"),
            "grunt": load_image("entities/grunt.png"),
            "hulk": load_image("entities/hulk.png"),
            "projectile": load_image("projectile.png")
        }

        # init counts
        self.score_count = 0
        self.wave_counter = 1
        self.life_count = 3

        # initialize the HUD
        self.hud = HUD(self.score_count, self.wave_counter, self.life_count)

        self.allsprites = pygame.sprite.Group()

        # Create the hero
        self.hero_size = (20, 27)  # pixel size
        self.hero = Hero(self, (150, 106.5), self.hero_size)
        self.hero_group = pygame.sprite.Group()
        self.hero_group.add(self.hero)
        self.allsprites.add(self.hero)

        # Projectile holder
        self.hero_projectiles = pygame.sprite.Group()

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

        #spawn hulks
        self.hulk_size = (29, 27)  # pixel size
        self.hulks_group = pygame.sprite.Group()
        self.hulk_positions = self.spawner.grunt_spawn()

        for pos in self.hulk_positions:
            hulk = Hulk(self, pos, self.hulk_size)
            self.hulks_group.add(hulk)
            self.allsprites.add(hulk)

    def run(self):
        grunt_move_timer = 0
        while True:
            self.display.fill((0, 0, 0))  # black background

            # hero functions
            # TODO: can we merge hero_projectiles and hero_group to only do a single group update() here?
            self.hero.update(movement=(self.movement[0], self.movement[1]),
                             shooting=self.hero_shooting)

            # grunt functions
            grunt_move_timer += 1
            if grunt_move_timer == 20:
                self.grunts_group.update()
                grunt_move_timer = 0

            # Update projectiles
            self.hero_projectiles.update()

            # hulk functions
            self.hulks_group.update()

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
                    if event.key == pygame.K_LEFT:
                        self.hero_shooting[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.hero_shooting[1] = True
                    if event.key == pygame.K_UP:
                        self.hero_shooting[2] = True
                    if event.key == pygame.K_DOWN:
                        self.hero_shooting[3] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.movement[1] = 0
                    if event.key == pygame.K_s:
                        self.movement[1] = 0
                    if event.key == pygame.K_a:
                        self.movement[0] = 0
                    if event.key == pygame.K_d:
                        self.movement[0] = 0
                    if event.key == pygame.K_LEFT:
                        self.hero_shooting[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.hero_shooting[1] = False
                    if event.key == pygame.K_UP:
                        self.hero_shooting[2] = False
                    if event.key == pygame.K_DOWN:
                        self.hero_shooting[3] = False

            # draw the HUD
            self.hud.render(self.display)

            # Scale up the pixel art by bliting the smaller display onto the larger screen.
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            # update the screen
            pygame.display.flip()
            self.clock.tick(60)  # framerate

if __name__ == "__main__":
    Game().run()
