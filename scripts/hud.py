import pygame
import logging

logging.basicConfig(format='%(name)s %(levelname)s %(asctime)s %(module)s (line: %(lineno)d) -- %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

# CONSTANTS
HUD_FONT_SIZE = 14
GAME_OVER_FONT_SIZE = 14 * 3
BORDER_COLOR = (255, 0, 0)  # red
TEXT_COLOR_WHITE = (255, 255, 255)
TEXT_COLOR_RED = (255, 0, 0)
BORDER_THICKNESS = 5
BORDER_PADDING = 15
ANIMATION_TIME = 160  # frames, 3 seconds


class HUD:
    """
    Handles the heads-up display (HUD) for the game. Displays the score, wave number & life count.
    """

    def __init__(self, game):
        pygame.init()
        pygame.font.init()  # Initialize the font module

        # HUD setup
        self.font = pygame.font.SysFont('Consolas', HUD_FONT_SIZE)  # Load the Consolas font
        self.game_over_font = pygame.font.SysFont('Consolas', GAME_OVER_FONT_SIZE)  # Load the Consolas font

        # init variables
        self.game = game
        self.skull_and_bones = self.game.assets["skull_and_bones"]
        self.skull_anim = {}  # holds the animation details
        
        # border setup
        self.border_color = BORDER_COLOR
        self.border_thickness = BORDER_THICKNESS
        self.border_padding = BORDER_PADDING

        self.display_rect = game.display.get_rect()
        # The height of the rectangle
        # adjusted by subtracting twice the border_padding (once for the top and once for the bottom).
        self.hud_rect = pygame.Rect(self.display_rect.left,
                          self.display_rect.top + self.border_padding,
                          self.display_rect.width,
                          self.display_rect.height - 2 * self.border_padding)
        # Define the area inside of the hud_rect as the active_area, where entities and projectiles can move
        self.active_area = pygame.Rect(self.display_rect.left + self.border_thickness,
                                       self.display_rect.top + self.border_padding + self.border_thickness,
                                       self.display_rect.width - 2 * self.border_thickness,
                                       self.display_rect.height - 2 * self.border_padding - 2 * self.border_thickness)

    def render(self, display):
        """Render the HUD on the screen.

        :param display: The main game screen
        """

        # Draw a border around the game window with padding at the top and bottom
        pygame.draw.rect(surface=display,
                         color=self.border_color,
                         rect=self.hud_rect,
                         width=self.border_thickness)
        
        # Draw the score
        score_text = self.font.render(f'SCORE: {self.game.score_count}', True, TEXT_COLOR_WHITE)
        display.blit(score_text, (5, 0)) 

        # Draw the wave number
        wave_text = self.font.render(f'WAVE: {self.game.wave_count}', True, TEXT_COLOR_WHITE)
        display.blit(wave_text, (5, self.display_rect.height - 15))

        # Draw the life count
        life_text = self.font.render(f'LIVES: {self.game.life_count}', True, TEXT_COLOR_WHITE)
        display.blit(life_text, (self.display_rect.width - 70, self.display_rect.top))

        # Update the display
        display.blit(pygame.transform.scale(display, display.get_size()), (0, 0))

        # draw any family-saved score point indicators
        self.game.scoring.draw_family_saved_score()

        # draw any family_killed skull_and_bones
        self.draw_family_death()

    def game_over(self):
        """
        You lose.

        :return: None
        """
        game_over_text = self.game_over_font.render(f"GAME OVER", True, TEXT_COLOR_RED)
        restart_text = self.font.render(f"Press 'R' to restart.", True, TEXT_COLOR_RED)
        self.game.display.blit(game_over_text, (self.game.display.get_width()/2-game_over_text.get_width()/2,
                                                self.game.display.get_height()/2-game_over_text.get_height()/2))
        self.game.display.blit(restart_text,
                               (self.game.display.get_width()/2-restart_text.get_width()/2,
                                self.game.display.get_height()/2+game_over_text.get_height()/2+restart_text.get_height()))

    def add_family_death(self, pos):
        """
        Add the killed family member to a dictionary that will render a death animation.

        :param pos: Position of the killed family member as (x, y)
        :return: None
        """
        self.skull_anim[int(pos[0])] = [self.skull_and_bones, list(pos), ANIMATION_TIME]  # 3 seconds

    def draw_family_death(self):
        """
        Display a skull and crossbones over any family member that is killed by robots.

        :return: None
        """
        if self.skull_anim:
            self.skull_anim = self.game.floating_animations.float_anim(self.skull_anim)

