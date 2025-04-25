from scripts.entities.entities import PhysicsEntity


class Dad(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, "dad", pos, size)  # inheret the PhysicsEntity class
        self.image = self.game.human_family_animations.animations[self.e_type][self.action][0]

        self.target_posit = self.random_movement()

    def update(self, movement=(0, 0)):
        # if dad has reached its target, calculate a new target
        self.target_posit = self.reached_target(target_pos=self.target_posit)
        super().move_to_target(target_pos=self.target_posit,
                               movement=movement,
                               scaler=.2,
                               move_dir=None)
