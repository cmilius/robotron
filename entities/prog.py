import pygame
from entities.entities import PhysicsEntity
import logging

logger = logging.getLogger(__name__)

class Prog(PhysicsEntity):
    """
    Former humans who have been reprogrammed by Brains. They chase the player with deadly intent and move like fast grunts.
    """

    def __init__(self, game, pos, size):
        super().__init__(game, self.__class__.__name__.lower(), pos, size)
        self.animations = self.game.human_family_animations.animations[self.e_type] # they were originally humans
        self.image = self.animations[self.action][0] 

        self.target_posit = self.random_movement()

        self.block_actions = True  # block movement until the prog has fully spawned
        self.spawn_frames = 6  # the number of animations frames in the prog spawn
        self.frame_counter = 0
        self.anim_frame_delay = 0
        self.trail_images = []  # list to store the trail images


    def animate(self, frame_movement):
        """
        Given a list frame_movement, update the entity animations.

        :param list frame_movement: The direction vector the entity is moving in.
        :return: None
        """

        # Append the current image and position to the trail
        self.trail_images.append((self.image, self.rect.topleft))

        # Limit the trail to the last 15 frames
        if len(self.trail_images) > 15:
            self.trail_images.pop(0)

        # Draw trail images at their respective positions
        for i, (trail_image, trail_pos) in enumerate(self.trail_images):
            if i % 5 == 0:  # Only draw every 5th image
                self.game.display.blit(trail_image, trail_pos, special_flags=pygame.BLEND_SUB)

        # Iterate the animation frames
        super().iterate_animation_frames()
        
        if frame_movement[0] > 0:
            self.action = "walk_right"
        elif frame_movement[0] < 0:
            self.action = "walk_left"
        if frame_movement[1] > 0 and not frame_movement[0]:
            self.action = "walk_down"
        elif frame_movement[1] < 0 and not frame_movement[0]:
            self.action = "walk_up"
                
        self.image = self.game.human_family_animations.animations[self.e_type][self.action][self.anim_flipbook[self.flipbook_index]]

    def update(self, movement=(0, 0)):
        # if reached its target, calculate a new target
        self.target_posit = self.reached_target(target_pos=self.target_posit)

        super().move_to_target(target_pos=self.target_posit,
                            movement=movement,
                            scaler=.7,
                            move_dir=None)