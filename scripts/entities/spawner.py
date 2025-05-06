import random
import logging
import json
import sys
from scripts.entities.electrode import Electrode
from scripts.entities.grunt import Grunt
from scripts.entities.hulk import Hulk
from scripts.entities.spheroid import Spheroid
from scripts.entities.quark import Quark
from scripts.entities.brain import Brain
from scripts.entities.family import Dad, Mom, Mike

logger = logging.getLogger(__name__)

with open("data/spawn_counts.json", "r") as f:
    WAVE_INTENSITY = json.load(f)


class Spawner:
    def __init__(self, game):
        """
        Constructor to pull in Game class.
        """
        self.game = game
        self.display = self.game.display

    @staticmethod
    def get_valid_position(size, exclude_range):
        """ Return valid positions within the display."""
        valid_positions = [i for i in range(size) if not (exclude_range[0] <= i < exclude_range[1])]
        return random.choice(valid_positions)

    def spawn_positions(self, e_type):
        """
        Given enemy type, give a list of enemy locations.

        :return: List of randomized positions per enemy_type
        """
        # account for the size of the robots to avoid clipping off the edge of the map
        mod_surf_size_x = self.display.get_width() - self.game.grunt_size[0]
        mod_surf_size_y = self.display.get_height() - self.game.grunt_size[1]

        # get the center of the map, use int() to get integer rather than float.
        map_center_x = int(self.display.get_width() / 2)
        map_center_y = int(self.display.get_height() / 2)

        # get the intensity. Search by entity type, then by level number (which has to be a string).
        try:
            num_robots = WAVE_INTENSITY.get(e_type).get(str(self.level))
        except AttributeError as e:
            logger.critical(e)
            logger.critical(f"Error getting the entity or level from the JSON. Double check the variable names.")
            sys.exit()
        posits = []

        # need to define an exclusion zone around the hero spawn area
        x_exclude = range(map_center_x - 30, map_center_x + 30)
        y_exclude = range(map_center_y - 30, map_center_y + 30)

        for i in range(0, num_robots):
            posits.append(((random.choice([x for x in range(mod_surf_size_x) if x not in x_exclude])),
                           random.choice([y for y in range(mod_surf_size_y) if y not in y_exclude])))
        return posits

    def spawn_enemies(self):
        """
        Used to spawn enemies for a new wave.

        :return: None
        """
        self.level = self.game.wave_count  # update the wave

        # spawn electrodes
        electrode_positions = self.spawn_positions("electrodes")
        for pos in electrode_positions:
            electrode = Electrode(self.game, pos, self.game.grunt_size)
            self.game.enemy_group.add(electrode)
            self.game.allsprites.add(electrode)

        # spawn grunts
        grunt_positions = self.spawn_positions("grunts")
        for pos in grunt_positions:
            grunt = Grunt(self.game, pos, self.game.grunt_size)
            self.game.enemy_group.add(grunt)
            self.game.grunts_group.add(grunt)
            self.game.allsprites.add(grunt)

        # spawn hulks
        hulk_positions = self.spawn_positions("hulks")
        for pos in hulk_positions:
            hulk = Hulk(self.game, pos, self.game.hulk_size)
            self.game.enemy_group.add(hulk)
            self.game.hulks_group.add(hulk)
            self.game.allsprites.add(hulk)

        # spawn spheroids
        spheroid_positions = self.spawn_positions("spheroids")
        for pos in spheroid_positions:
            spheroid = Spheroid(self.game, pos, self.game.spheroid_size)
            self.game.enemy_group.add(spheroid)
            self.game.allsprites.add(spheroid)

        # spawn quarks
        quark_positions =self.spawn_positions("quarks")
        for pos in quark_positions:
            quark = Quark(self.game, pos, self.game.quark_size)
            self.game.enemy_group.add(quark)
            self.game.allsprites.add(quark)

        # spawn brains
        brain_positions = self.spawn_positions("brains")
        for pos in brain_positions:
            brain = Brain(self.game, pos, self.game.brain_size)
            self.game.enemy_group.add(brain)
            self.game.brains_group.add(brain)
            self.game.allsprites.add(brain)

    def spawn_family(self):
        """
        Used to spawn family members for a new wave.

        :return: None
        """
        self.level = self.game.wave_count  # update the wave

        # spawn dads
        dad_positions = self.spawn_positions("dad")
        for pos in dad_positions:
            dad = Dad(self.game, pos, self.game.dad_size)
            self.game.family_group.add(dad)
            self.game.allsprites.add(dad)

        # spawn moms
        mom_positions = self.spawn_positions("mom")
        for pos in mom_positions:
            mom = Mom(self.game, pos, self.game.mom_size)
            self.game.family_group.add(mom)
            self.game.allsprites.add(mom)

        # spawn mikes
        mike_positions = self.spawn_positions("mike")
        for pos in mike_positions:
            mike = Mike(self.game, pos, self.game.mike_size)
            self.game.family_group.add(mike)
            self.game.allsprites.add(mike)
