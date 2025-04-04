from scripts.entities.entities import PhysicsEntity
from scripts.projectiles.projectiles import Projectiles


class Hero(PhysicsEntity):
    def __init__(self, game, pos, size):
        self.game = game
        self.pos = list(pos)
        self.size = size
        super().__init__(self.game, "hero", self.pos, self.size)
        self.projectile_reload = 20  # frames
        self.projectile_timer = 10  # count up to projectile reload
        self.respawn_invuln = 0  # frames

        self.action = "idle"  # initial stance

        # used to track the last pressed keys for shooting
        self.h_stack = []
        self.v_stack = []

    def update(self, movement=(0, 0), shooting=(False, False, False, False)):

        self.image = self.game.hero_animations.animations[self.e_type][self.action][0]
        
        if self.respawn_invuln:
            # Frame counter to make the hero invulnerable after respawn. Will be set to an integer in the game loop.
            self.respawn_invuln -= 1

        super().update(movement=movement)

        self.shooting = list(shooting)
        # Find out which key was last pressed by the hero
        if self.shooting[0] and "left" not in self.h_stack:
            self.h_stack.append("left")
        elif not self.shooting[0] and "left" in self.h_stack:
            self.h_stack.remove("left")
        if self.shooting[1] and "right" not in self.h_stack:
            self.h_stack.append("right")
        elif not self.shooting[1] and "right" in self.h_stack:
            self.h_stack.remove("right")
        if self.h_stack:
            if self.h_stack[-1] == "left":
                self.shooting[0] = True
                self.shooting[1] = False
            else:
                self.shooting[0] = False
                self.shooting[1] = True
        if self.shooting[2] and "up" not in self.v_stack:
            self.v_stack.append("up")
        elif not self.shooting[2] and "up" in self.v_stack:
            self.v_stack.remove("up")
        if self.shooting[3] and "down" not in self.v_stack:
            self.v_stack.append("down")
        elif not self.shooting[3] and "down" in self.v_stack:
            self.v_stack.remove("down")
        if self.v_stack:
            if self.v_stack[-1] == "up":
                self.shooting[2] = True
                self.shooting[3] = False
            else:
                self.shooting[2] = False
                self.shooting[3] = True

        # only fire if the gun is reloaded
        if self.projectile_timer != self.projectile_reload:
            self.projectile_timer += 1
        if True in self.shooting and (self.projectile_timer == self.projectile_reload):
            projectile = Projectiles(self.game, "projectile", self.pos, self.shooting)
            self.game.hero_projectiles.add(projectile)
            self.game.allsprites.add(projectile)
            self.projectile_timer = 0  # cooldown to the projectile_reload framecount
