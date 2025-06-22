from scripts.entities.entities import PhysicsEntity
import random
import logging

logger = logging.getLogger(__name__)

DIRECTION_MAP = {
    (True, False, False, True): (-1, 1),  # Northwest
    (True, False, True, False): (-1, -1),  # Southwest
    (False, True, False, True): (1, 1),  # Northeast
    (False, True, True, False): (1, -1),  # Southeast
    (False, False, False, True): (0, 1),  # North
    (False, False, True, False): (0, -1),  # South
    (False, True, False, False): (1, 0),  # East
    (True, False, False, False): (-1, 0),  # West
}

# CONSTANTS
SLOWED_TIMER = 300  # frames. Controls how long the hulk will be slowed by.
DEFAULT_MOVE_SPEED_SCALER = 0.6  # The normal movement speed of the hulk
SLOWED_MOVE_SPEED_SCALER = 0.2  # Movement speed of the hulk when slowed by hero projectile

class Hulk(PhysicsEntity):
    """
        Large, indestructible robots that wander the screen, killing humans and trapping the player.
    """

    def __init__(self, game, pos, size):
        super().__init__(game, "hulk", pos, size)  # inheret the PhysicsEntity class
        self.image = self.game.robotrons_animations.animations[self.e_type][self.action][0]
        self.slowed_timer = SLOWED_TIMER

        self.target_posit = self.random_movement()
        self.move_dir = None

    def update(self, movement=(0, 0)):
        """
        Moves the hulk. The hulk only moves orthogonally and in one direction at a time.

        :param movement: Movement in (x, y). Default (0, 0)
        :return: None
        """
        # If the hulk is hit with a projectile, its movement speed will be slowed for self.slowed_timer.
        if self.slowed_timer <= 0:
            movement_scaler = DEFAULT_MOVE_SPEED_SCALER
        else:
            movement_scaler = SLOWED_MOVE_SPEED_SCALER
            self.slowed_timer -= 1

        # pick movement direction, x or y
        if self.move_dir is None:
            self.move_dir = random.choice(["x", "y"])
        # move x
        if self.move_dir == "x":
            if abs(self.pos[0] - self.target_posit[0]) < 2:  # get it close, won't ever be exact due to speed variation
                self.move_dir = "y"
        # move y
        if self.move_dir == "y":
            if abs(self.pos[1] - self.target_posit[1]) < 2:  # get it close, won't ever be exact due to speed variation
                self.move_dir = "x"
        # if the hulk has reached its target, calculate a new target
        # TODO: this logic got implemented into the super().reached_target function.
        #  However, I did not implement the self.move_dir logic into the return. Need to figure out how to handle this.
        if abs(self.pos[0] - self.target_posit[0]) < 2\
                and abs(self.pos[1] - self.target_posit[1]) < 2:
            # calculate new target posit
            self.target_posit = self.random_movement()
            self.move_dir = None  # reset the movement direction
        super().move_to_target(target_pos=self.target_posit,
                               movement=movement,
                               scaler=movement_scaler,
                               move_dir=self.move_dir)

    def animate(self, frame_movement):
        """
        Given a list frame_movement, update the entity animations.

        :param list frame_movement: The direction vector the entity is moving in.
        :return: None
        """
        self.iterate_animation_frames()
        if frame_movement[0] == 0 and frame_movement[1] != 0:
            self.action = "walk_vertical"
        elif frame_movement[0] > 0:
            self.action = "walk_right"
        elif frame_movement[0] < 0:
            self.action = "walk_left"
        self.image = self.game.robotrons_animations.animations[self.e_type][self.action][self.anim_flipbook[self.flipbook_index]]

    def hit_by_projectile(self, **kwargs):
        """
        Slows down the hulk.

        :return: None
        """
        # This will slow down the movement scaler in update()
        self.slowed_timer = SLOWED_TIMER
        
        # Push back the hulk in the direction it was hit
        for k, val in kwargs.items():
            hit_dir_list = val

        movement = DIRECTION_MAP.get(tuple(hit_dir_list))
        self.move_entity(movement)

