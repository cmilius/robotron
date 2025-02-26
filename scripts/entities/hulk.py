from robotron.scripts.entities.entities import PhysicsEntity
import random


class Hulk(PhysicsEntity):
    """
        Large, indestructible robots that wander the screen, killing humans and trapping the player.
    """

    def __init__(self, game, pos, size):
        super().__init__(game, "hulk", pos, size)  # inheret the PhysicsEntity class
        self.slowed_timer = 300
        self.timer = 300

        self.target_posit = self.hulk_movement()
        self.move_dir = None

    def hulk_movement(self):
        """
        Pick a new position for the hulk to travel to.

        :return: [x, y]
        """
        posit = [random.choice(range(self.game.display.get_width())),
                 random.choice(range(self.game.display.get_height()))]
        return posit

    def update(self, movement=(0, 0)):
        """
        Moves the hulk. The hulk only moves orthogonally and in one direction at a time.

        :param movement: Movement in (x, y). Default (0, 0)
        :return: None
        """
        # If the hulk is hit with a projectile, its movement speed will be slowed for self.slowed_timer.
        if self.timer == self.slowed_timer:
            movement_scaler = .6
        else:
            movement_scaler = .2
            self.timer += 1

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
        if abs(self.pos[0] - self.target_posit[0]) < 2\
                and abs(self.pos[1] - self.target_posit[1]) < 2:
            # calculate new target posit
            self.target_posit = self.hulk_movement()
            self.move_dir = None  # reset the movement direction
        super().move_to_target(target_pos=self.target_posit,
                               movement=movement,
                               scaler=movement_scaler,
                               move_dir=self.move_dir)

    def hit_by_projectile(self):
        """
        Slows down the hulk.

        :return: None
        """
        self.timer = 0
