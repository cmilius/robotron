from scripts.entities.entities import PhysicsEntity

# CONSTANTS
FAMILY_MOVEMENT_SCALER = 0.2  # controls the movement speed of the family


class Family(PhysicsEntity):
    def __init__(self, game, e_type, pos, size):
        super().__init__(game, e_type, pos, size)  # inheret the PhysicsEntity class
        self.image = self.game.human_family_animations.animations[self.e_type][self.action][0]

        self.target_posit = self.random_movement()

    def update(self, movement=(0, 0)):
        # if dad has reached its target, calculate a new target
        self.target_posit = self.reached_target(target_pos=self.target_posit)
        super().move_to_target(target_pos=self.target_posit,
                               movement=movement,
                               scaler=FAMILY_MOVEMENT_SCALER,
                               move_dir=None)

class Dad(Family):
    def __init__(self, game, pos, size):
        super().__init__(game, "dad", pos, size)

class Mom(Family):
    def __init__(self, game, pos, size):
        super().__init__(game, "mom", pos, size)

class Mike(Family):
    def __init__(self, game, pos, size):
        super().__init__(game, "mike", pos, size)