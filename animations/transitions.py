import pygame
import random
import copy

# CONSTANTS
# !!! WARNING !!!!
# Changing the transition animation will require changing the transition timers in the main game loop
SQUARE_DURATION = 1000  # milliseconds, how long it takes for a square to get to the edge
TOTAL_DURATION = 1000  # milliseconds, how long until the final square will be drawn which ends the animation
SQUARE_SPACING = 0.04  # controls new squares being drawn
# SQUARE_SPACING is dictated by the ratio of drawn to total width. Smaller number = more squares

class TransitionBase:
    def __init__(self, center, width, height, color, start_time, duration):
        """
        Initializes a Square object that will expand over time.

        :param center: The center of the game display
        :param width: Width of the game display
        :param height: Height of the game display
        :param color: The color of the square (RGB tuple).
        :param start_time: Milliseconds, when the square animation starts
        :param duration: Milliseconds, time for the square to start to when it reaches it's full size
        """
        self.center = center
        self.width = width
        self.height = height
        self.color = color
        self.start_time = start_time
        self.duration = duration

        self.ratio = 0  # Goes from 0 to 1, reprents size of the square relative to final size in decimal
        self.can_spawn_new = True  # Flag if new squares can be spawned

    def update_ratio(self, now):
        """
        Update the ratio of the square based on the elapsed time.

        :param now: Time in milliseconds
        :return: Elapsed time since the square was spawned
        """
        elapsed = now - self.start_time
        # normalize time (0 to 1) over the duration
        self.ratio = min(elapsed / self.duration, 1)
        return elapsed

    def draw(self, surface):
        """
        Draw the square on the given surface.

        :param surface: pygame.Surface to blit our squares on
        :return: None
        """
        # determine the size of the square by expanding over a period of time to the full width/height
        x_size = self.width * self.ratio
        y_size = self.height * self.ratio
        rect = (self.center[0] - (x_size // 2), self.center[1] - (y_size // 2), x_size, y_size)
        pygame.draw.rect(surface, self.color, rect)

    def square_spacing(self, square_spacing):
        return (self.width * self.ratio) / self.width > square_spacing

    def draw_final(self, surface, t):
        x_size = self.width * t
        y_size = self.height * t
        rect = (self.center[0] - (x_size // 2), self.center[1] - (y_size // 2), x_size, y_size)
        pygame.draw.rect(surface, (255, 255, 255), rect)

class CenterSquare(TransitionBase):
    def __init__(self, center, width, height, color, start_time, duration):
        super().__init__(center, width, height, color, start_time, duration)

    def draw(self, surface):
        # determine the size of the square by expanding over a period of time to the full width/height
        x_size = self.width * self.ratio
        y_size = self.height * self.ratio
        rect = (self.center[0] - (x_size // 2), self.center[1] - (y_size // 2), x_size, y_size)
        pygame.draw.rect(surface, self.color, rect)

    def draw_final(self, surface, t):
        x_size = self.width * t
        y_size = self.height * t
        rect = (self.center[0] - (x_size // 2), self.center[1] - (y_size // 2), x_size, y_size)
        pygame.draw.rect(surface, (255, 255, 255), rect)

class VerticalSquare(TransitionBase):
    def __init__(self, center, width, height, color, start_time, duration):
        super().__init__(center, width, height, color, start_time, duration)

    def draw(self, surface):
        # determine the size of the square by expanding over a period of time to the full width/height
        x_size = self.width * self.ratio
        y_size = self.height
        rect = (self.center[0] - (x_size // 2), self.center[1] - (y_size // 2), x_size, y_size)
        pygame.draw.rect(surface, self.color, rect)

    def draw_final(self, surface, t):
        x_size = self.width * t
        y_size = self.height
        rect = (self.center[0] - (x_size // 2), self.center[1] - (y_size // 2), x_size, y_size)
        pygame.draw.rect(surface, (255, 255, 255), rect)

class HorizontalSquare(TransitionBase):
    def __init__(self, center, width, height, color, start_time, duration):
        super().__init__(center, width, height, color, start_time, duration)

    def draw(self, surface):
        # determine the size of the square by expanding over a period of time to the full width/height
        x_size = self.width
        y_size = self.height * self.ratio
        rect = (self.center[0] - (x_size // 2), self.center[1] - (y_size // 2), x_size, y_size)
        pygame.draw.rect(surface, self.color, rect)

    def draw_final(self, surface, t):
        x_size = self.width
        y_size = self.height * t
        rect = (self.center[0] - (x_size // 2), self.center[1] - (y_size // 2), x_size, y_size)
        pygame.draw.rect(surface, (255, 255, 255), rect)

class LeftSquare(TransitionBase):
    def __init__(self, center, width, height, color, start_time, duration):
        super().__init__(center, width, height, color, start_time, duration)
        self.side = random.choice(["left", "right"])

    def draw(self, surface):
        # determine the size of the square by expanding over a period of time to the full width/height
        x_size = self.width * self.ratio
        y_size = self.height
        rect = (0, self.center[1] - (y_size // 2), x_size, y_size)
        pygame.draw.rect(surface, self.color, rect)

    def draw_final(self, surface, t):
        x_size = self.width * t
        y_size = self.height
        rect = (0, self.center[1] - (y_size // 2), x_size, y_size)
        pygame.draw.rect(surface, (255, 255, 255), rect)

class RightSquare(TransitionBase):
    def __init__(self, center, width, height, color, start_time, duration):
        super().__init__(center, width, height, color, start_time, duration)

    def draw(self, surface):
        # determine the size of the square by expanding over a period of time to the full width/height
        x_size = self.width * self.ratio
        y_size = self.height
        rect = (self.width-x_size, self.center[1] - (y_size // 2), x_size, y_size)
        pygame.draw.rect(surface, self.color, rect)

    def draw_final(self, surface, t):
        x_size = self.width * t
        y_size = self.height
        rect = (self.width-x_size, self.center[1] - (y_size // 2), x_size+10, y_size)  # +10 to cover up any lag
        pygame.draw.rect(surface, (255, 255, 255), rect)

class TopSquare(TransitionBase):
    def __init__(self, center, width, height, color, start_time, duration):
        super().__init__(center, width, height, color, start_time, duration)

    def draw(self, surface):
        # determine the size of the square by expanding over a period of time to the full width/height
        x_size = self.width
        y_size = self.height * self.ratio
        rect = (self.center[0] - (x_size // 2), 0, x_size, y_size)
        pygame.draw.rect(surface, self.color, rect)

    def draw_final(self, surface, t):
        x_size = self.width
        y_size = self.height * t
        rect = (self.center[0] - (x_size // 2), 0, x_size, y_size)
        pygame.draw.rect(surface, (255, 255, 255), rect)

class BotSquare(TransitionBase):
    def __init__(self, center, width, height, color, start_time, duration):
        super().__init__(center, width, height, color, start_time, duration)

    def draw(self, surface):
        # determine the size of the square by expanding over a period of time to the full width/height
        x_size = self.width
        y_size = self.height * self.ratio
        rect = (self.center[0] - (x_size // 2), self.height-y_size, x_size, y_size)
        pygame.draw.rect(surface, self.color, rect)

    def draw_final(self, surface, t):
        x_size = self.width
        y_size = self.height * t
        rect = (self.center[0] - (x_size // 2), self.height - y_size, x_size, y_size+10)  # +10 to cover up any lag
        pygame.draw.rect(surface, (255, 255, 255), rect)

TRANSITION_OPTIONS = [
    VerticalSquare,
    HorizontalSquare,
    LeftSquare,
    RightSquare,
    TopSquare,
    BotSquare
]

class Transitions:
    def __init__(self, game):
        """
        Top-level class for controlling the animation of the growing squares transition animation.

        :param game: pygame.game object
        """
        self.game = game
        # determine the animation type
        if self.game.first_wave:
            self.square_type = CenterSquare
        else:
            self.square_type = random.choice(TRANSITION_OPTIONS)
        self.real_start = pygame.time.get_ticks()  # timer for the final square
        self.square_dur = SQUARE_DURATION  # milliseconds, how long it takes for a square to get to the edge
        self.total_dur = TOTAL_DURATION  # milliseconds, how long until the final square will be drawn
        self.square_spacing = SQUARE_SPACING  # controls new squares being drawn,
        # dictated by the ratio of drawn to total width. smaller number = more squares drawn

        # screen dimensions
        self.width = self.game.display.get_width()
        self.height = self.game.display.get_height()
        self.center = (self.width // 2, self.height // 2)

        # square logic
        self.squares_list = []  # list of squares that will be drawn
        self.first = True  # triggers the first square, which is generated outside the for loop
        self.last_done = False  # indicates that the last square has been created, stopping all further squares
        self.final_start = None  # the start time of the final square
        self.finished = False  # indicates that the last square has finished its animation, ending this class animation

        # Create a surface to draw our squares onto. This surface will then be blit onto the game.display
        self.transition_surf = self.create_transition_surface()

        self.game.audio.play("level_transition")

    def create_transition_surface(self):
        """
        Create a new surface that will blit on top of game.display.

        :return: pygame.Surface
        """
        if self.game.first_wave:
            # if it is the first wave, create a black background (default behaviour of Surface)
            surf = pygame.Surface(self.game.display.get_size())
        else:
            # else, make the background transparent to keep showing the HUD and other game elements
            surf = pygame.Surface(self.game.display.get_size(), pygame.SRCALPHA)
            surf.fill((0, 0, 0, 0))
        return surf

    def add_square(self):
        """
        Add a square to the stack.
        Each square will have a randomly generated color.

        :return: None
        """
        color = tuple(random.choices(range(256), k=3))

        square = self.square_type(center=self.center,
                                  width=self.width,
                                  height=self.height,
                                  color=color,
                                  start_time=pygame.time.get_ticks(),
                                  duration=self.square_dur
                                  )
        self.squares_list.append(square)

    def normal_squares(self, now):
        """
        Draw the squares transition using pygame.rect

        :param now: pygame.time.get_ticks()
        :return: None
        """
        # use copy.copy() to safely edit lists in a loop
        square_copy = copy.copy(self.squares_list)
        for square in square_copy:

            elapsed = square.update_ratio(now)  # update the ratio of the square
            square.draw(self.transition_surf)

            # Add more squares based on how much the previous square has grown, until the last square has been drawn
            if square.square_spacing(self.square_spacing) and square.can_spawn_new and not self.last_done:
                self.add_square()
                square.can_spawn_new = False

            # Keep the drawn squares on the screen for a period of time to allow the smaller squares to reach the edges
            if elapsed > self.square_dur + 1000:
                self.squares_list.remove(square)

    def final_square(self, now):
        """
        Draw the final square animation, a transparent square that reveals the game.display surface state underneath.

        :param now: pygame.time.ticks()
        :return: None
        """
        total_elapsed = now - self.real_start
        self.last_done = total_elapsed >= self.total_dur

        if self.last_done:
            if self.final_start is None:
                self.final_start = pygame.time.get_ticks()
            elapsed = now - self.final_start
            final_t = min(elapsed / self.square_dur, 1)

            self.square_type(center=self.center,
                             width=self.width,
                             height=self.height,
                             color=(255, 255, 255),
                             start_time=self.final_start,
                             duration=self.square_dur
                             ).draw_final(self.transition_surf, final_t)
            self.transition_surf.set_colorkey((255, 255, 255))

            # signals to the game loop that the animation has completed
            if final_t >= 1:
                self.finished = True

    def iterate(self):
        """
        Update the square dimensions based on the amount of time they have been active.

        :return: None
        """
        now = pygame.time.get_ticks()

        # Add the initial square to the list to kick things off
        if self.first:
            self.add_square()
            self.first = False
        self.normal_squares(now)
        self.final_square(now)

        self.game.display.blit(self.transition_surf, (0, 0))
