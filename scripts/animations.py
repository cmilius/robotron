import pygame
import logging

logger = logging.getLogger(__name__)


class ExplodeAnimations:
    """
    Animate sprite explosions by splitting an image into slices and animating their expansion
    based on the specified direction and mirroring.
    """
    def __init__(self, game, sprite, explode_logic=("horizontal", False)):
        self.game = game
        self.sprite = sprite
        self.explode_logic = explode_logic  # [direction, mirror flag]
        self.start_time = pygame.time.get_ticks()
        self.duration = 1000  # The total duration of the animation in milliseconds
        self.finished = False
        self.displacement = 25  # The displacement speed for the slices during animation
        self.alpha_start = 255  # The initial opacity value of the slices (fully opaque)
        self.alpha_end = 0  # The final opacity value of the slices (fully transparent)

        self.vertical_slices = []  # List of dictionaries representing the vertical slices of the sprite
        self.horizontal_slices = []  # List of dictionaries representing the horizontal slices of the sprite

        self.pos_x = self.sprite.pos[0]
        self.pos_y = self.sprite.pos[1]

        self.slice_count = 5  # The number of slices to split the sprite into.
        self.center_index = self.slice_count // 2  # The index of the center slice, used for calculating movement speeds

        img_width, img_height = sprite.image.get_size()
        slice_width = img_width // self.slice_count
        slice_height = img_height // self.slice_count

        for i in range(self.slice_count):
            # vertical slices
            if i == self.slice_count - 1:
                width = img_width - (i * slice_width)
            else:
                width = slice_width
            rect = pygame.Rect(i * slice_width, 0, width, img_height)
            surf = sprite.image.subsurface(rect).copy()
            self.vertical_slices.append({"surf": surf, "rect": rect.copy(), "dir": "h", "index": i})

        for i in range(self.slice_count):
            # horizontal slices
            if i == self.slice_count - 1:
                height = img_height - (i * slice_height)
            else:
                height = slice_height
            rect = pygame.Rect(0, i * slice_height, img_width, height)
            surf = sprite.image.subsurface(rect).copy()
            self.horizontal_slices.append({"surf": surf, "rect": rect.copy(), "dir": "v", "index": i})

    def animate_slices(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.start_time
        t = min(elapsed / self.duration, 1.0)
        self.finished = t >= 1.0  # finished flag if time is > 1 second

        # Determine which slices to animate based on the explode_direction
        if self.explode_logic[0] == "horizontal":
            slice_lists = [self.vertical_slices]
        elif self.explode_logic[0] == "vertical":
            slice_lists = [self.horizontal_slices]
        elif self.explode_logic[0] == "diagonal":
            slice_lists = [self.horizontal_slices]

        for slice_list in slice_lists:
            for s in slice_list:
                surf = s["surf"]
                rect = s["rect"]
                # Calculate the opacity value based on elapsed time
                alpha = int(self.alpha_start * (1 - t) + self.alpha_end * t)
                surf.set_alpha(alpha)

                # Calculate the displacement speed for each slice based on its distance from the center slice
                distance_from_center = abs(s["index"] - self.center_index)
                displace_scale = 1 + distance_from_center

                if self.explode_logic[0] == "horizontal" and s["dir"] == "h":
                    # Shrink width, move left/right
                    new_width = max(1, int(rect.width * (1 - t)))
                    new_surf = pygame.transform.scale(surf, (new_width, rect.height))
                    shift = int(self.displacement * displace_scale * t)

                    self.game.display.blit(new_surf, (rect.x + self.pos_x - shift, rect.y + self.pos_y))
                    self.game.display.blit(new_surf, (rect.x + self.pos_x + shift, rect.y + self.pos_y))

                elif self.explode_logic[0] == "vertical" and s["dir"] == "v":
                    # Shrink height, move up/down
                    new_height = max(1, int(rect.height * (1 - t)))
                    new_surf = pygame.transform.scale(surf, (rect.width, new_height))
                    shift = int(self.displacement * displace_scale * t)

                    self.game.display.blit(new_surf, (rect.x + self.pos_x, rect.y + self.pos_y - shift))
                    self.game.display.blit(new_surf, (rect.x + self.pos_x, rect.y + self.pos_y + shift))

                elif self.explode_logic[0] == "diagonal" and s["dir"] == "v":
                    # Shrink both, move diagonally
                    new_height = max(1, int(rect.height * (1 - t)))
                    new_width = max(1, int(rect.width * (1 - t)))
                    new_surf = pygame.transform.scale(surf, (new_width, new_height))
                    shift = int(self.displacement * displace_scale * t)

                    # Mirrored diagonal
                    if self.explode_logic[1]:
                        self.game.display.blit(new_surf, (rect.x + self.pos_x + shift, rect.y + self.pos_y - shift))
                        self.game.display.blit(new_surf, (rect.x + self.pos_x - shift, rect.y + self.pos_y + shift))
                    # Normal diagonal
                    else:
                        self.game.display.blit(new_surf, (rect.x + self.pos_x - shift, rect.y + self.pos_y - shift))
                        self.game.display.blit(new_surf, (rect.x + self.pos_x + shift, rect.y + self.pos_y + shift))


class ConvergenceAnimations:
    """
    A class to animate the convergence of sprite slices into the final image.
    The slices start in a displaced and shrunken state and converge to form the full image over 2 seconds.
    """

    def __init__(self, game, sprite, explode_direction=("horizontal", 0)):
        """
        Initializes the convergence animation with the specified parameters and splits the image into slices.


        :param sprite: The sprite to animate.
        :param explode_direction: A tuple containing the convergence direction ("horizontal", "vertical", or "diagonal")
                                        and mirroring flag (bool).
        """
        self.game = game
        self.sprite = sprite
        self.explode_direction = explode_direction  # Direction and mirroring flag
        self.start_time = pygame.time.get_ticks()  # Start time of the animation
        self.duration = 1500  # Duration of the convergence animation in ms

        # For convergence, we'll reverse the alpha transition:
        # Start with a lower alpha (from explosion state) and end with full opacity.
        self.alpha_start = 255  # Final (assembled) alpha
        self.alpha_end = 128    # Initial (exploded) alpha

        self.displacement = 25  # Maximum displacement (slices start displaced and converge)

        self.vertical_slices = []  # List for vertical slices (for horizontal convergence)
        self.horizontal_slices = []  # List for horizontal slices (for vertical/diagonal convergence)

        # The on-screen position of the sprite.
        self.pos_x = self.sprite.pos[0]
        self.pos_y = self.sprite.pos[1]

        self.slice_count = 5
        self.center_index = self.slice_count // 2

        # Split the image into slices based on its actual size.
        img_width, img_height = sprite.image.get_size()
        slice_width = img_width // self.slice_count
        slice_height = img_height // self.slice_count

        # Create vertical slices (for horizontal convergence).
        for i in range(self.slice_count):
            width = img_width - (i * slice_width) if i == self.slice_count - 1 else slice_width
            rect = pygame.Rect(i * slice_width, 0, width, img_height)
            surf = sprite.image.subsurface(rect).copy()
            self.vertical_slices.append({"surf": surf, "rect": rect.copy(), "dir": "h", "index": i})

        # Create horizontal slices (for vertical or diagonal convergence).
        for i in range(self.slice_count):
            height = img_height - (i * slice_height) if i == self.slice_count - 1 else slice_height
            rect = pygame.Rect(0, i * slice_height, img_width, height)
            surf = sprite.image.subsurface(rect).copy()
            self.horizontal_slices.append({"surf": surf, "rect": rect.copy(), "dir": "v", "index": i})

        self.finished = False

    def animate_slices(self):
        """
        Animates the convergence of the sprite slices.
        Slices are drawn such that they move from a displaced, shrunken state to their proper position and full size.
        If the sprite's e_type is "hero", slices from both vertical and horizontal splits are animated.
        """
        now = pygame.time.get_ticks()
        elapsed = now - self.start_time
        # Normalized time (0 to 1) over the duration.
        t = min(elapsed / self.duration, 1.0)
        # For convergence, we want the displacement to decrease over time:
        # At t = 0, rev_t is 1 (full displacement) and at t = 1, rev_t is 0.
        rev_t = 1 - t

        self.finished = t >= 1.0

        # Determine which slice lists to animate.
        # If the sprite is a hero, animate slices from both directions.
        if getattr(self.sprite, "e_type", None) == "hero":
            slice_lists = [self.vertical_slices, self.horizontal_slices]
        else:
            # Otherwise, use the specified explode_direction for convergence.
            if self.explode_direction[0] == "horizontal":
                slice_lists = [self.vertical_slices]
            elif self.explode_direction[0] == "vertical":
                slice_lists = [self.horizontal_slices]
            elif self.explode_direction[0] == "diagonal":
                slice_lists = [self.horizontal_slices]

        # Animate each slice in the selected lists.
        for slice_list in slice_lists:
            for s in slice_list:

                # Update the on-screen position of the sprite.
                # This is mostly used for the hero respawn, when the hero can move while invulnerable
                self.pos_x = self.sprite.pos[0]
                self.pos_y = self.sprite.pos[1]

                surf = s["surf"]
                rect = s["rect"]
                # Reverse the alpha transition: low alpha at start, full alpha at finish.
                alpha = int(self.alpha_start * t + self.alpha_end * rev_t)
                surf.set_alpha(alpha)

                # Calculate a displacement scale based on distance from the center slice.
                distance_from_center = abs(s["index"] - self.center_index)
                displace_scale = 1 + distance_from_center

                # Animate convergence based on the type of slice.
                if self.explode_direction[0] == "horizontal" or getattr(self.sprite, "e_type", None) == "hero":
                    # For vertical slices (s["dir"] == "h"), converge horizontally.
                    if s["dir"] == "h":
                        new_width = max(1, int(rect.width * t))
                        new_surf = pygame.transform.scale(surf, (new_width, rect.height))
                        shift = int(self.displacement * displace_scale * rev_t)
                        # Slices converge from left and right.
                        self.game.display.blit(new_surf, (rect.x + self.pos_x - shift, rect.y + self.pos_y))
                        self.game.display.blit(new_surf, (rect.x + self.pos_x + shift, rect.y + self.pos_y))
                if self.explode_direction[0] == "vertical" or getattr(self.sprite, "e_type", None) == "hero":
                    # For horizontal slices (s["dir"] == "v"), converge vertically.
                    if s["dir"] == "v":
                        new_height = max(1, int(rect.height * t))
                        new_surf = pygame.transform.scale(surf, (rect.width, new_height))
                        shift = int(self.displacement * displace_scale * rev_t)
                        # Slices converge from above and below.
                        self.game.display.blit(new_surf, (rect.x + self.pos_x, rect.y + self.pos_y - shift))
                        self.game.display.blit(new_surf, (rect.x + self.pos_x, rect.y + self.pos_y + shift))
                if self.explode_direction[0] == "diagonal" or getattr(self.sprite, "e_type", None) == "hero":
                    # For diagonal convergence, apply diagonal movement.
                    # (We assume the diagonal slices are stored in the horizontal_slices list.)
                    if s["dir"] == "v":
                        new_width = max(1, int(rect.width * t))
                        new_height = max(1, int(rect.height * t))
                        new_surf = pygame.transform.scale(surf, (new_width, new_height))
                        shift = int(self.displacement * displace_scale * rev_t)
                        # Convergence diagonally: slices move toward their proper positions.
                        self.game.display.blit(new_surf, (rect.x + self.pos_x - shift, rect.y + self.pos_y - shift))
                        self.game.display.blit(new_surf, (rect.x + self.pos_x + shift, rect.y + self.pos_y + shift))
                        # If mirroring is enabled, also converge from the opposite diagonal.
                        if self.explode_direction[1] == 1:
                            self.game.display.blit(new_surf, (rect.x + self.pos_x + shift, rect.y + self.pos_y - shift))
                            self.game.display.blit(new_surf, (rect.x + self.pos_x - shift, rect.y + self.pos_y + shift))