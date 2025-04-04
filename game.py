import sys
import pygame
import logging

from scripts.entities.hero import Hero
from scripts.entities.spawner import Spawner
from scripts.utils import load_image
from scripts.hud import HUD
from scripts.entities.spritesheet import SpriteSheet

logging.basicConfig(format='%(name)s %(levelname)s %(asctime)s %(module)s (line: %(lineno)d) -- %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

# New game values
SCORE_COUNT = 0
WAVE_COUNT = 0
LIFE_COUNT = 3

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
            "spheroid": load_image("entities/spheroid.png"),
            "enforcer": load_image("entities/enforcer.png"),
            "enforcer_projectile": load_image("projectiles/enforcer_projectile.png"),
            "projectile": load_image("projectiles/hero_projectile.png")
        }

        # pixel size of sprite
        self.grunt_size = (29, 27)
        self.hulk_size = (29, 27)
        self.dad_size = (29, 27)
        self.mom_size = (29, 27)
        self.mike_size = (29, 27)
        self.spheroid_size = (16, 15)
        self.enforcer_size = (30, 37)

        # Load the sprite sheets
        self.hero_animations = SpriteSheet("data/images/entities/hero_spritesheet.png")
        self.human_family_animations = SpriteSheet("data/images/entities/human_family_spritesheet.png")
        self.robotrons_animations = SpriteSheet("data/images/entities/robotrons_spritesheet.png")

        # example use of the animations for reference, look in the json files in the data/images/entities folder for the animation names
        # self.display.blit(self.human_family_animations.animations['mike']['walk_right'][animation_frame_count], (20, 60))

        # initialize the HUD
        self.hud = HUD(self, SCORE_COUNT, WAVE_COUNT, LIFE_COUNT)

        # initialize game conditions
        self.game_over = False
        self.game_restart = False

        # initialize the group that will be used to draw all the sprites at once.
        self.allsprites = pygame.sprite.Group()

        # Create the hero
        self.hero_size = (20, 27)  # pixel size
        self.hero = Hero(self, (self.display.get_width()/2, self.display.get_height()/2), self.hero_size)
        self.hero_group = pygame.sprite.Group()
        self.hero_group.add(self.hero)
        self.allsprites.add(self.hero)

        # Projectile holder
        self.hero_projectiles = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()

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

            if self.game_restart:
                # if the game has been restarted, set all the counters back to the their original values.
                self.hud.score_count = SCORE_COUNT
                self.hud.wave_count = WAVE_COUNT
                self.hud.life_count = LIFE_COUNT
                for entity in self.grunts_group:
                    # this will trigger the spawn enemies code.
                    entity.kill()
                self.game_over = False
                self.game_restart = False

            # Spawn enemies
            if not self.grunts_group:  # TODO: This will eventually need to be a 'everything except hulks' group
                # empty out any previous wave stuff
                for enemy in self.enemy_group:
                    enemy.kill()
                for projectile in self.hero_projectiles:
                    projectile.kill()
                for projectile in self.enemy_projectiles:
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
            #   hero_projectile-to-enemy
            enemy_hit = pygame.sprite.groupcollide(self.hero_projectiles, self.enemy_group, True, False)
            if enemy_hit:
                # returns {<Projectiles Sprite(in 0 groups)>: [<Grunt Sprite(in 3 groups)>]}
                affected_enemy = list(enemy_hit.values())[0][0]  # determine the affected enemy
                affected_enemy.hit_by_projectile()
            #   enemy-to-hero
            hero_collision = pygame.sprite.spritecollide(self.hero, self.enemy_group, False)
            hero_shot = pygame.sprite.spritecollide(self.hero, self.enemy_projectiles, False)
            if hero_shot:
                # need to kill the projectile that hit the hero,
                #  otherwise it could cause instant game-over if the hero is at the center of the screen
                affected_projectile = hero_shot[0]  # determine the projectile
                affected_projectile.kill()
            if hero_collision or hero_shot:
                if not self.hero.respawn_invuln:
                    # check if the hero is invulnerable due to respawn
                    # if the player is not invulnerable, they lose a life.
                    if self.hud.life_count != 0:
                        # this is here because otherwise you end up with a -1 life indication at the GAME OVER screen
                        self.hud.life_count -= 1
                    if self.hud.life_count == 0:
                        self.game_over = True
                    else:
                        # respawn the hero at the center of the screen and toggle invulnerability
                        self.hero.move_to_center()
                        self.hero.respawn_invuln = 120  # set the hero invulnerable for 2 seconds
            #   hulk-to-family
            pygame.sprite.groupcollide(self.hulks_group, self.family_group, False, True)
            #   hero-to-family
            pygame.sprite.groupcollide(self.hero_group, self.family_group, False, True)

            if not self.game_over:
                # Update hero
                self.hero.update(movement=(self.movement[0], self.movement[1]),
                                 shooting=self.hero_shooting)

                # Update groups
                self.hero_projectiles.update()
                self.enemy_projectiles.update()
                self.enemy_group.update()
                self.family_group.update()

            # draw sprites
            self.allsprites.draw(self.display)
            if self.game_over:
                # GAME OVER text drawn here to ensure it is drawn on top of all the other sprites.
                self.hud.game_over()

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
                    if event.key == pygame.K_r:
                        if self.game_over:
                            # if the game is over, restart the game.
                            self.game_restart = True
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
