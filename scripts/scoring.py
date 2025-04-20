import logging
from pygame import font

logger = logging.getLogger(__name__)

GRUNT_SCORE = 100
TANK_SCORE = 200
ENFORCER_SCORE = 200  # This one is not in the list below, just guessing.
BRAIN_SCORE = 500
SPHEROID_SCORE = 1000
ENEMY_PROJECTILE_SCORE = 25
NEW_LIFE_SCORE = 25000


class Scoring:
    """
    RESCUING HUMANS: 1000 multiplied by the number of humans you've saved so far,
    up untill five, at which point the bonus stays at 5000 points. The value
    resets each wave.

    SHOOT GRUNT OR PROG: 100 Points
    SHOOT TANK: 200 Points
    SHOOT BRAIN: 500 Points
    SHOOT SPHEROID OR QUARK: 1000 Points
    SHOOT ENEMY SHOT: 25 Points

    You begin every game with five lives. You lose a life every time you are hit
    by an enemy or one of their shots, or if you touch an electrode. A bonus life
    is awarded for every 25,000 points earned.
    """

    def __init__(self, game):
        self.game = game

        self.curr_wave = 1  # new game wave will start on 1
        self.score_mult = 1  # used to multiply vs. the number of humans saved per wave
        self.life_add_mult = 1  # used to multiply vs. the 25000 additional life counter

        self.font = font.SysFont('Consolas', 10)  # Load the Consolas font
        self.score_disp = {}

        self.enemy_score_dict = {
            "grunt": GRUNT_SCORE,
            "prog": GRUNT_SCORE,
            "enforcer": ENFORCER_SCORE,
            "tank": TANK_SCORE,
            "brain": BRAIN_SCORE,
            "spheroid": SPHEROID_SCORE,
            "quark": SPHEROID_SCORE,
            "projectile": ENEMY_PROJECTILE_SCORE
        }

    def reset_score_mult(self):
        """
        Reset the score multiplier on each new wave.

        :return: None
        """
        self.score_mult = 1

    def update_score(self, e_type, pos=None):
        """
        Given entity, update the score.

        :param e_type: entity type
        :param pos: the position of the entity, only needed if the entity is family
        :return: None
        """
        if e_type in self.enemy_score_dict.keys():
            self.game.score_count += self.enemy_score_dict[e_type]
        elif e_type == "family":
            # calculate and add score
            self.score_to_add = 1000 * self.score_mult
            self.game.score_count += self.score_to_add

            # Add score to the score_disp dictionary. [surf, position, time to display]
            surf = self.font.render(str(self.score_to_add), True, (255, 255, 255))
            self.score_disp[surf] = [surf, list(pos), 120]

            if not self.score_mult == 5:  # limit the score multiplier to 5
                self.score_mult += 1
        elif e_type == "hulk":
            # this is just here for now to avoid getting the logger.critical() message below for shooting hulks.
            pass
        else:
            # To catch any score errors that might go unnoticed in the chaos.
            logger.critical(f"e_type not recognized: {e_type}")

        if self.game.score_count >= (NEW_LIFE_SCORE * self.life_add_mult):
            # TODO: I think we should add some animation here to make it clear there was a life added
            self.game.life_count += 1
            self.life_add_mult += 1
            logger.info("Life count +1!")

    def draw_family_saved_score(self):
        """
        Display the 'family saved' score the floats near the saved family member for two seconds.

        :return: None
        """
        if self.score_disp:
            self.score_disp = self.game.floating_animations.float_anim(self.score_disp)


