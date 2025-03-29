from scripts.entities.entities import PhysicsEntity


class Grunt(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, "grunt", pos, size)  # inheret the PhysicsEntity class
        self.movement_timer = 0
        self.move_at_time = 20

    def update(self, movement=(0, 0)):
        """
        The grunt should slowly move torwards the hero entity.

        :param movement: Movement in (x, y). Default (0, 0)
        :return: None
        """
        self.movement_timer += 1
        if self.movement_timer == self.move_at_time:
            super().move_to_target(target_pos=(self.game.hero.rect.x, self.game.hero.rect.y),
                                   movement=movement,
                                   scaler=3)
            self.movement_timer = 0

    def hit_by_projectile(self):
        self.kill()
        # TODO: add to score


