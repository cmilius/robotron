import sys
import pygame
import logging
import random

from scripts.entities.hero import Hero
from scripts.entities.spawner import Spawner
from scripts.utils import load_image
from scripts.hud import HUD
from scripts.entities.spritesheet import SpriteSheet
from scripts.scoring import Scoring
from scripts.animations import ExplodeAnimations, ConvergenceAnimations, FloatingAnimations

logging.basicConfig(format='%(name)s %(levelname)s %(asctime)s %(module)s (line: %(lineno)d) -- %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

# New game values
SCORE_COUNT = 0
WAVE_COUNT = 0
LIFE_COUNT = 5


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("robotron")
        self.screen = pygame.display.set_mode((1280, 960))  # Top-left is 0-0
        # Put assets onto the display. Display will then be projected onto the screen for a more pixel-art look.
        self.display = pygame.Surface((640, 480))

        self.clock = pygame.time.Clock()

        self.hero_movement = [False, False, False, False]  # [left, right, up, down]
        self.hero_shooting = [False, False, False, False]  # [left, right, up, down]

        self.assets = {
            "enforcer_projectile": load_image("projectiles/enforcer_projectile.png"),
            "projectile": load_image("projectiles/hero_projectile.png"),
            "skull_and_bones": load_image("skull_and_bones.png")
        }

        # pixel size of sprite
        self.grunt_size = (9, 13)
        self.hulk_size = (29, 27)
        self.dad_size = (29, 27)
        self.mom_size = (29, 27)
        self.mike_size = (29, 27)
        self.prog_size = (29, 27)
        self.spheroid_size = (16, 15)
        self.enforcer_size = (30, 37)
        self.brain_size = (30, 37)

        # Load the sprite sheets
        self.hero_animations = SpriteSheet("data/images/entities/hero_spritesheet.png")
        self.human_family_animations = SpriteSheet("data/images/entities/human_family_spritesheet.png")
        self.robotrons_animations = SpriteSheet("data/images/entities/robotrons_spritesheet.png")

        # initialize game counters
        self.score_count = SCORE_COUNT
        self.wave_count = WAVE_COUNT
        self.life_count = LIFE_COUNT

        # initalize the score counter
        self.scoring = Scoring(self)

        # initialize the HUD
        self.hud = HUD(self)

        # Animation containers
        self.active_animations = []
        self.converge_list = []
        self.floating_animations = FloatingAnimations(self)

        #
        self.spawn_timer = 90  # tied to the duration set in ConvergenceAnimation
        self.spawn_counter = 0
        self.pause_entity_movement = True  # This flag is active when entities are spawning into the map, blocks entity updates+movement

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
        self.brains_group = pygame.sprite.Group()

        # Family group
        self.family_group = pygame.sprite.Group()

    def run(self):
        while True:
            self.display.fill((0, 0, 0))  # black background

            if self.game_restart:
                # if the game has been restarted, set all the counters back to the their original values.
                self.score_count = SCORE_COUNT
                self.wave_count = WAVE_COUNT
                self.life_count = LIFE_COUNT
                for entity in self.grunts_group:
                    # this will trigger the spawn enemies code.
                    entity.kill()
                self.game_over = False
                self.game_restart = False
                self.pause_entity_movement = True

            # Spawn enemies
            if not self.grunts_group:  # TODO: This will eventually need to be a 'everything except hulks' group
                self.pause_entity_movement = True
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
                # reset the family score multiplier
                self.scoring.reset_score_mult()
                # spawn new wave
                self.wave_count += 1
                self.spawner.spawn_enemies()
                self.spawner.spawn_family()
                for entity in self.allsprites:
                    if entity.e_type != "mike" and entity.e_type != "mom" and entity.e_type != "dad":
                        # if the entity is not a family member, spawn them on the screen using ConvergenceAnimations
                        self.converge_list.append(ConvergenceAnimations(self, entity,
                                                                        (random.choice(["vertical", "horizontal"]), 0)))

            # collision detection
            #   hero_projectile-to-enemy
            enemy_hit = pygame.sprite.groupcollide(self.hero_projectiles, self.enemy_group, True, False)
            if enemy_hit:
                # returns {<Projectiles Sprite(in 0 groups)>: [<Grunt Sprite(in 3 groups)>]}
                affected_enemy = list(enemy_hit.values())[0][0]  # determine the affected enemy
                for projectile in enemy_hit:
                    explode_logic = projectile.explode_logic  # explode logic is dictated by the projectile direction
                self.scoring.update_score(affected_enemy.e_type)
                affected_enemy.hit_by_projectile()
                if affected_enemy.e_type != "hulk":
                    self.active_animations.append(ExplodeAnimations(self, affected_enemy, explode_logic))
            #  hero_projectile-to-enemy_projectile
            projectile_hit = pygame.sprite.groupcollide(self.hero_projectiles, self.enemy_projectiles, True, True)
            if projectile_hit:
                self.scoring.update_score("projectile")
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
                    if self.life_count != 0:
                        # this is here because otherwise you end up with a -1 life indication at the GAME OVER screen
                        self.life_count -= 1
                    if self.life_count == 0:
                        self.game_over = True
                    else:
                        # respawn the hero at the center of the screen and toggle invulnerability
                        self.hero.move_to_center()
                        self.hero.respawn_invuln = 90  # set the hero invulnerable for 1.5 seconds
                        self.converge_list.append(ConvergenceAnimations(self, self.hero,
                                                                            (random.choice(["vertical", "horizontal"]),
                                                                             0)))
            #   hulk-to-family
            hulk_to_fam = pygame.sprite.groupcollide(self.hulks_group, self.family_group, False, True)
            if hulk_to_fam:
                # {<Hulk Sprite(in 3 groups)>: [<Dad Sprite(in 0 groups)>]}
                self.hud.add_family_death(list(hulk_to_fam.values())[0][0].pos)

            # brain-to-family
            brain_to_fam = pygame.sprite.groupcollide(self.brains_group, self.family_group, False, True)
            for brain in brain_to_fam:
                # spawn a prog
                brain.spawn_prog()
                self.hud.add_family_death(list(brain_to_fam.values())[0][0].pos)
            
            #   hero-to-family
            family_saved = pygame.sprite.groupcollide(self.hero_group, self.family_group, False, True)
            if family_saved:
                self.scoring.update_score("family", pos=self.hero.pos)

            if not self.game_over and not self.pause_entity_movement:
                # Update hero
                self.hero.update(movement=self.hero_movement,
                                 shooting=self.hero_shooting)

                # Update groups
                self.hero_projectiles.update()
                self.enemy_projectiles.update()
                self.enemy_group.update()
                self.family_group.update()

            # draw sprites
            if not self.pause_entity_movement:
                self.allsprites.draw(self.display)
            if self.pause_entity_movement:
                # robots should spawn into the world with the family already there, like aliens invading.
                self.family_group.draw(self.display)
                if self.spawn_counter == self.spawn_timer:
                    self.pause_entity_movement = False
                    self.spawn_counter = 0
                else:
                    self.spawn_counter += 1

            if self.game_over:
                # GAME OVER text drawn here to ensure it is drawn on top of all the other sprites.
                self.hud.game_over()

            # event manager
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.hero_movement[0] = True
                    if event.key == pygame.K_d:
                        self.hero_movement[1] = True
                    if event.key == pygame.K_w:
                        self.hero_movement[2] = True
                    if event.key == pygame.K_s:
                        self.hero_movement[3] = True
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
                    if event.key == pygame.K_a:
                        self.hero_movement[0] = False
                    if event.key == pygame.K_d:
                        self.hero_movement[1] = False
                    if event.key == pygame.K_w:
                        self.hero_movement[2] = False
                    if event.key == pygame.K_s:
                        self.hero_movement[3] = False
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

            for animation in self.active_animations:
                animation.animate_slices()
                if animation.finished:
                    self.active_animations.remove(animation)
            for animation in self.converge_list:
                animation.animate_slices()
                if animation.finished:
                    self.converge_list.remove(animation)

            # Scale up the pixel art by bliting the smaller display onto the larger screen.
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            # update the screen
            pygame.display.flip()
            self.clock.tick(60)  # framerate


if __name__ == "__main__":
    Game().run()
