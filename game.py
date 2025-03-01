import sys
import pygame
import logging

from robotron.scripts.entities.hero import Hero
from robotron.scripts.entities.spawner import Spawner
from scripts.utils import load_image
from scripts.hud import HUD

logging.basicConfig(format='%(name)s %(levelname)s %(asctime)s %(module)s (line: %(lineno)d) -- %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("robotron")
        self.screen = pygame.display.set_mode((1280, 960))  # Top-left is 0-0
        # Put assets onto the display. Display will then be projected onto the screen for a more pixel-art look.
        self.display = pygame.Surface((640, 480))

        self.clock = pygame.time.Clock()

        self.movement = [0, 0]  # [x, y]
        self.hero_shooting = [False, False, False, False]  # [left, right, up, down]

        self.assets = {
            "hero": load_image("entities/hero.png"),
            "dad": load_image("entities/dad.png"),
            "mom": load_image("entities/mom.png"),
            "mike": load_image("entities/mike.png"),
            "grunt": load_image("entities/grunt.png"),
            "hulk": load_image("entities/hulk.png"),
            "projectile": load_image("projectile.png")
        }
        self.grunt_size = (29, 27)  # pixel size
        self.hulk_size = (29, 27)  # pixel size
        self.dad_size = (29, 27)  # pixel size
        self.mom_size = (29, 27)  # pixel size
        self.mike_size = (29, 27)  # pixel size

        # init counts
        self.score_count = 0
        self.wave_counter = 0
        self.life_count = 3

        # initialize the HUD
        self.hud = HUD(self.score_count, self.wave_counter, self.life_count)

        self.allsprites = pygame.sprite.Group()

        # Create the hero
        self.hero_size = (20, 27)  # pixel size
        self.hero = Hero(self, (self.display.get_width()/2, self.display.get_height()/2), self.hero_size)
        self.hero_group = pygame.sprite.Group()
        self.hero_group.add(self.hero)
        self.allsprites.add(self.hero)

        # Projectile holder
        self.hero_projectiles = pygame.sprite.Group()

        # Enemy groups
        self.spawner = Spawner(self)
        self.grunts_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.hulks_group = pygame.sprite.Group()

        # Family group
        self.family_group = pygame.sprite.Group()

    def run(self):
        while True:
            self.display.fill((0, 0, 0))  # black background

            # Spawn enemies
            if not self.grunts_group:  # TODO: This will eventually need to be a 'everything except hulks' group
                # empty out any previous wave stuff
                for enemy in self.enemy_group:
                    enemy.kill()
                for projectile in self.hero_projectiles:
                    projectile.kill()
                for family in self.family_group:
                    family.kill()  # :(
                # respawn the player
                self.hero.move_to_center()
                # spawn new wave
                self.hud.wave_count += 1
                self.spawner.spawn_enemies(self.hud.wave_count)
                self.spawner.spawn_family(self.hud.wave_count)

            # collision detection
            #   projectile-to-enemy
            enemy_hit = pygame.sprite.groupcollide(self.hero_projectiles, self.enemy_group, True, False)
            if enemy_hit:
                # returns {<Projectiles Sprite(in 0 groups)>: [<Grunt Sprite(in 3 groups)>]}
                affected_enemy = list(enemy_hit.values())[0][0]  # determine the affected enemy
                affected_enemy.hit_by_projectile()
            #   enemy-to-hero
            hero_collision = pygame.sprite.spritecollide(self.hero, self.enemy_group, False)
            if hero_collision:
                if self.hud.life_count == 0:
                    # TODO: game over
                    pass
                else:
                    # TODO: respawn logic: hero invulnerability, etc.
                    self.hud.life_count -= 1
                    self.hero.move_to_center()
            #   hulk-to-family
            pygame.sprite.groupcollide(self.hulks_group, self.family_group, False, True)
            #   hero-to-family
            pygame.sprite.groupcollide(self.hero_group, self.family_group, False, True)

            # Update hero
            self.hero.update(movement=(self.movement[0], self.movement[1]),
                             shooting=self.hero_shooting)

            # Update groups
            self.hero_projectiles.update()
            self.enemy_group.update()
            self.family_group.update()

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
