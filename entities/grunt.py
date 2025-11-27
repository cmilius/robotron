from entities.entities import PhysicsEntity

# CONSTANTS
MOVE_AT_TIME = 20  # Frames, dictates the frame interval when all the grunts move at once
GRUNT_MOVEMENT_SCALER = 3

class Grunt(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, "grunt", pos, size)  # inheret the PhysicsEntity class
        self.image = self.game.robotrons_animations.animations[self.e_type][self.action][0]
        self.move_at_time = MOVE_AT_TIME

    def update(self, movement=(0, 0)):
        """
        The grunt should slowly move torwards the hero entity.

        :param movement: Movement in (x, y). Default (0, 0)
        :return: None
        """
        self.move_at_time -= 1
        if self.move_at_time <= 0:
            super().move_to_target(target_pos=(self.game.hero.rect.x, self.game.hero.rect.y),
                                   movement=movement,
                                   scaler=GRUNT_MOVEMENT_SCALER)
            self.move_at_time = MOVE_AT_TIME

    def iterate_animation_frames(self):
        # the grunt already moves on a "delay", so no buffer is required.
        self.flipbook_index += 1
        if self.flipbook_index == self.anim_length:
            self.flipbook_index = 0

    def animate(self, frame_movement):
        """
        Given a list frame_movement, update the entity animations.

        :param list frame_movement: The direction vector the entity is moving in.
        :return: None
        """
        if frame_movement[0] or frame_movement[1]:
            self.action = "walk"
            self.iterate_animation_frames()
        self.image = self.game.robotrons_animations.animations[self.e_type][self.action][self.anim_flipbook[self.flipbook_index]]

    def hit_by_projectile(self, **kwargs):
        self.kill()


