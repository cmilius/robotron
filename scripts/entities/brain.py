from scripts.entities.entities import PhysicsEntity
from scripts.entities.prog import Prog

class Brain(PhysicsEntity):
    """
        These are the most intelligent enemies. They fire Cruise Missiles that home in 
        on the player and can capture humans, turning them into Progs. They only appear every 
        5 levels in a "Brain Wave."
    """

    # define constants
    POINT_VALUE     = 500  # point value for the brain
    MOVEMENT_SPEED  = 0.2  # movement speed of the brain

    def __init__(self, game, pos, size):
        """
        Initialize the Brain entity.
        :param game: The game object.
        :param pos: The position of the brain.
        :param size: The size of the brain.
        """

        # inheret the PhysicsEntity class
        super().__init__(game, self.__class__.__name__.lower(), pos, size)  
        self.image = self.game.robotrons_animations.animations[self.e_type][self.action][0]
        self.action = "idle"        # initial stance
        self.target_pos = [0, 0]    # target position for the brain to move to

    def update(self, movement=(0, 0)):
        """
        Moves the brain. The brain can move in any direction, including diagonally.
        The brain will focus colliding with the nearest human to turn them into a prog.
        If there are no humans left, the brain will chase down the player.

        :param movement: Movement in (x, y). Default (0, 0)
        :return: None
        """

        # chase the player
        target_pos = [self.game.hero.rect[0], self.game.hero.rect[1]]
        
        # unless there are humans left, chase the closest one
        humans = self.game.family_group.sprites()

        if len(humans) > 0:
            
            # initialize the closest human position
            smallest_distance = 0

            # loop through the humans to find the closest one
            for human in humans:
                x = self.pos[0] - human.pos[0]
                y = self.pos[1] - human.pos[1]
                distance = abs(x) + abs(y)

                # Update the smallest distance and target position if a closer human is found
                if smallest_distance == 0 or distance <= smallest_distance:
                    smallest_distance = distance
                    target_pos = human.pos       

        # move to the target position
        super().move_to_target(target_pos,
                               movement=movement,
                               scaler=self.MOVEMENT_SPEED,
                               move_dir=None)

    def fire_projectile(self):
        """
        Fire cruise missile at the hero
        :return: None
        """
        # TODO: Implement the fire_projectile method for the brain.

    def spawn_prog(self):
        """
        Turn a human into a Prog
        :return: None
        """

        # spawn the prog at the brain's position
        prog = Prog(self.game, (self.pos[0], self.pos[1]), self.game.prog_size)
        self.game.enemy_group.add(prog)
        self.game.allsprites.add(prog)

    def hit_by_projectile(self):
        """
        Brain ded

        :return: None
        """
        self.kill()

    def get_point_value(self):
        """
        Returns the point value of the brain

        :return: int
        """
        # TODO: This method should be moved to the PhysicsEntity class and pull from each
        # entity sub-class's POINT_VALUE propery. This is a placeholder for now.
        return self.POINT_VALUE
