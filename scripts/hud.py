import pygame
import logging

logging.basicConfig(format='%(name)s %(levelname)s %(asctime)s %(module)s (line: %(lineno)d) -- %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


class HUD:
    """
    Handles the heads-up display (HUD) for the game. Displays the score, wave number & life count.
    """

    def __init__(self, game, score_count=0, wave_count=1, life_count=3):
        pygame.init()
        pygame.font.init()  # Initialize the font module

        # HUD setup
        self.font = pygame.font.SysFont('Consolas', 14)  # Load the Consolas font
        self.game_over_font = pygame.font.SysFont('Consolas', 14*3)  # Load the Consolas font

        # init variables
        self.game = game
        self.score_count = score_count
        self.wave_count = wave_count
        self.life_count = life_count
        
        # border setup
        self.border_color = (255, 0, 0)  # Red
        self.border_thickness = 5
        self.border_padding = 15

    def render(self, display):
        """Render the HUD on the screen.

        :param screen: The main game screen
        """

        # Draw a border around the game window with padding at the top and bottom
        rect = display.get_rect()
        pygame.draw.rect(display, self.border_color, 
                         (rect.left, 
                          rect.top + self.border_padding, 
                          rect.width, 
                          rect.height - 2 * self.border_padding),  #The height of the rectangle, adjusted by subtracting twice the border_padding (once for the top and once for the bottom).
                         self.border_thickness)
        
        # Draw the score
        score_text = self.font.render(f'SCORE: {self.score_count}', True, (255, 255, 255))
        display.blit(score_text, (5, 0)) 

        # Draw the wave number
        wave_text = self.font.render(f'WAVE: {self.wave_count}', True, (255, 255, 255))
        display.blit(wave_text, (5, rect.height - 15))

        # Draw the life count
        life_text = self.font.render(f'LIVES: {self.life_count}', True, (255, 255, 255))
        display.blit(life_text, (rect.width - 70, rect.top))

        # Update the display
        display.blit(pygame.transform.scale(display, display.get_size()), (0, 0))

    def set_score_count(self, score_count):
        """
        Assign the HUD's score.

        :param score: Current score
        """
        self.score_count = score_count

    def set_life_count(self, life_count):
        """
        Assign the HUD's life count.

        :param life_count: New life count
        """
        self.life_count = life_count

    def set_wave_count(self, wave_count):
        """
        Assign the HUD's wave count.

        :param life_count: New wave count
        """
        self.wave_count = wave_count

    def game_over(self):
        """
        You lose.

        :return: None
        """
        game_over_text = self.game_over_font.render(f"GAME OVER", True, (255, 0, 0))
        restart_text = self.font.render(f"To restart the game, press 'R'", True, (255, 0, 0))
        self.game.display.blit(game_over_text, (self.game.display.get_width()/2-game_over_text.get_width()/2,
                                                self.game.display.get_height()/2-game_over_text.get_height()/2))
        self.game.display.blit(restart_text,
                               (self.game.display.get_width()/2-restart_text.get_width()/2,
                                self.game.display.get_height()/2+game_over_text.get_height()/2+restart_text.get_height()))
