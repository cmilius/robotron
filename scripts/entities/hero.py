from scripts.entities.entities import PhysicsEntity
from scripts.projectiles.projectiles import Projectiles


class Hero(PhysicsEntity):
    def __init__(self, game, pos, size):
        self.game = game
        self.pos = list(pos)
        self.size = size
        super().__init__(self.game, "hero", self.pos, self.size)
        self.image = self.game.hero_animations.animations[self.e_type][self.action][0]
        self.buffer_length = 10  # override the super() buffer_length to be shorter
        self.projectile_reload = 20  # frames
        self.projectile_timer = 10  # count up to projectile reload
        self.respawn_invuln = 0  # frames

        self.action = "idle"  # initial stance

        # used to track the last pressed keys for shooting
        self.h_stack_shooting = []
        self.v_stack_shooting = []
        # used to track the last pressed keys for hero movement
        self.h_stack_movement = []
        self.v_stack_movement = []

    def update(self, movement=(False, False, False, False), shooting=(False, False, False, False)):
        if self.respawn_invuln:
            # Frame counter to make the hero invulnerable after respawn. Will be set to an integer in the game loop.
            self.respawn_invuln -= 1

        self.movement = self._directions_logic(movement, self.h_stack_movement, self.v_stack_shooting)
        super().update(movement=self.movement)

        if True in self.movement:
            # only update the image if the player is pressing a movemnt key.
            # Otherwise the image will face the last direction the hero moved.
            super().iterate_animation_frames()
            self.image = self.game.hero_animations.animations[self.e_type][self.action][self.anim_flipbook[self.flipbook_index]]

        self.shooting = self._directions_logic(shooting, self.h_stack_shooting, self.v_stack_shooting)
        # only fire if the gun is reloaded
        if self.projectile_timer != self.projectile_reload:
            self.projectile_timer += 1
        if True in self.shooting and (self.projectile_timer == self.projectile_reload):
            projectile = Projectiles(self.game, "projectile", self.pos, self.shooting)
            self.game.hero_projectiles.add(projectile)
            self.game.allsprites.add(projectile)
            self.projectile_timer = 0  # cooldown to the projectile_reload framecount

    def _directions_logic(self, player_inputs, h_stack, v_stack):
        """
        Given a list of keyboard inputs, return a list of active outputs.
        This utilizes a stack of horizontal and vertical movement to handle
        conflicting inputs.
        :return: list of directions
        """
        player_inputs = list(player_inputs)

        # Find out which key was last pressed by the hero
        if player_inputs[2] and "up" not in v_stack:
            v_stack.append("up")
        elif not player_inputs[2] and "up" in v_stack:
            v_stack.remove("up")
        if player_inputs[3] and "down" not in v_stack:
            v_stack.append("down")
        elif not player_inputs[3] and "down" in v_stack:
            v_stack.remove("down")
        if v_stack:
            if v_stack[-1] == "up":
                player_inputs[2] = True
                player_inputs[3] = False
                self.action = "walk_up"
            else:
                player_inputs[2] = False
                player_inputs[3] = True
                self.action = "walk_down"
        if player_inputs[0] and "left" not in h_stack:
            h_stack.append("left")
        elif not player_inputs[0] and "left" in h_stack:
            h_stack.remove("left")
        if player_inputs[1] and "right" not in h_stack:
            h_stack.append("right")
        elif not player_inputs[1] and "right" in h_stack:
            h_stack.remove("right")
        if h_stack:
            if h_stack[-1] == "left":
                player_inputs[0] = True
                player_inputs[1] = False
                self.action = "walk_left"
            else:
                player_inputs[0] = False
                player_inputs[1] = True
                self.action = "walk_right"
        return player_inputs
