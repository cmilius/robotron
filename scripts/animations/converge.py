import pygame

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
        self.explode_direction = explode_direction  # [direction, mirror flag]
        self.start_time = pygame.time.get_ticks()  # Start time of the animation
        self.duration = 1500  # Duration of the convergence animation in ms

        # Start as transparent and end with full opacity
        self.alpha_start = 255
        self.alpha_end = 128

        self.displacement = 25  # Maximum displacement away from the spawn location

        self.vertical_slices = []
        self.horizontal_slices = []

        # The position of the sprite
        self.pos_x = self.sprite.pos[0]
        self.pos_y = self.sprite.pos[1]

        self.slice_count = 5  # number of slices
        self.center_index = self.slice_count // 2  # calculate the center of the convergence based on the slice_count

        # Split the image into slices
        img_width, img_height = sprite.image.get_size()
        slice_width = img_width // self.slice_count
        slice_height = img_height // self.slice_count

        for i in range(self.slice_count):
            # vertical slices
            width = img_width - (i * slice_width) if i == self.slice_count - 1 else slice_width
            rect = pygame.Rect(i * slice_width, 0, width, img_height)
            surf = sprite.image.subsurface(rect).copy()
            self.vertical_slices.append({"surf": surf, "rect": rect.copy(), "dir": "h", "index": i})

        for i in range(self.slice_count):
            # horizontal slices
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

        # If the sprite is a hero, animate slices from all directions
        if getattr(self.sprite, "e_type", None) == "hero":
            slice_lists = [self.vertical_slices, self.horizontal_slices]
        else:
            # else the direction is picked at random by the entity itself
            if self.explode_direction[0] == "horizontal":
                slice_lists = [self.vertical_slices]
            elif self.explode_direction[0] == "vertical":
                slice_lists = [self.horizontal_slices]
            elif self.explode_direction[0] == "diagonal":
                slice_lists = [self.horizontal_slices]

        for slice_list in slice_lists:
            for s in slice_list:
                # Update the on-screen position of the sprite
                # This is mostly used for the hero respawn because the hero can move while invulnerable
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

                # Animate convergence based on the type of slice
                if self.explode_direction[0] == "horizontal" or getattr(self.sprite, "e_type", None) == "hero":
                    # For vertical slices (s["dir"] == "h"), converge horizontally.
                    if s["dir"] == "h":
                        new_width = max(1, int(rect.width * t))
                        new_surf = pygame.transform.scale(surf, (new_width, rect.height))
                        shift = int(self.displacement * displace_scale * rev_t)
                        # Slices converge from left and right
                        self.game.display.blit(new_surf, (rect.x + self.pos_x - shift, rect.y + self.pos_y))
                        self.game.display.blit(new_surf, (rect.x + self.pos_x + shift, rect.y + self.pos_y))
                if self.explode_direction[0] == "vertical" or getattr(self.sprite, "e_type", None) == "hero":
                    # For horizontal slices (s["dir"] == "v"), converge vertically.
                    if s["dir"] == "v":
                        new_height = max(1, int(rect.height * t))
                        new_surf = pygame.transform.scale(surf, (rect.width, new_height))
                        shift = int(self.displacement * displace_scale * rev_t)
                        # Slices converge from above and below
                        self.game.display.blit(new_surf, (rect.x + self.pos_x, rect.y + self.pos_y - shift))
                        self.game.display.blit(new_surf, (rect.x + self.pos_x, rect.y + self.pos_y + shift))
                if self.explode_direction[0] == "diagonal" or getattr(self.sprite, "e_type", None) == "hero":
                    # For diagonal convergence, apply diagonal movement to horizontal slices
                    if s["dir"] == "v":
                        new_width = max(1, int(rect.width * t))
                        new_height = max(1, int(rect.height * t))
                        new_surf = pygame.transform.scale(surf, (new_width, new_height))
                        shift = int(self.displacement * displace_scale * rev_t)
                        # Convergence diagonally: slices move toward their proper positions.
                        self.game.display.blit(new_surf, (rect.x + self.pos_x - shift, rect.y + self.pos_y - shift))
                        self.game.display.blit(new_surf, (rect.x + self.pos_x + shift, rect.y + self.pos_y + shift))
                        # If mirroring is True, also converge from the opposite diagonal.
                        if self.explode_direction[1]:
                            self.game.display.blit(new_surf, (rect.x + self.pos_x + shift, rect.y + self.pos_y - shift))
                            self.game.display.blit(new_surf, (rect.x + self.pos_x - shift, rect.y + self.pos_y + shift))