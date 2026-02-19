import sys
import pygame

# CONSTANTS
DEFAULT_VOLUME = 0.5
AUDIO_FILEPATH = "data/audio/"

class Audio:
    """
    Handles the audio & sound effects for the game.
    """

    def __init__(self):
        pygame.mixer.init()

        if sys.platform == "emscripten":
            extension = ".ogg"
        else:
            extension = ".wav"

        self.sounds = {
            "enforcer_fire": pygame.mixer.Sound(AUDIO_FILEPATH + "enforcer_fire" + extension),
            "grunt_walk": pygame.mixer.Sound(AUDIO_FILEPATH + "grunt_walk" + extension),
            "hero_death": pygame.mixer.Sound(AUDIO_FILEPATH + "hero_death" + extension),
            "hero_lazer": pygame.mixer.Sound(AUDIO_FILEPATH + "hero_lazer" + extension),
            "human_die": pygame.mixer.Sound(AUDIO_FILEPATH + "human_die" + extension),
            "human_save": pygame.mixer.Sound(AUDIO_FILEPATH + "human_save" + extension),
            "level_transition": pygame.mixer.Sound(AUDIO_FILEPATH + "level_transition" + extension),
            "prog_transformation": pygame.mixer.Sound(AUDIO_FILEPATH + "prog_transformation" + extension),
            "quark_spawn": pygame.mixer.Sound(AUDIO_FILEPATH + "quark_spawn" + extension),
            "tank_explode": pygame.mixer.Sound(AUDIO_FILEPATH + "tank_explode" + extension),
            "tank_fire": pygame.mixer.Sound(AUDIO_FILEPATH + "tank_fire" + extension),
            "tank_projectile_bounce": pygame.mixer.Sound(AUDIO_FILEPATH + "tank_projectile_bounce" + extension)
            
        }

        # Set a default volume for all sounds
        for sound in self.sounds.values():
            sound.set_volume(DEFAULT_VOLUME)  

    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].stop() # Stop the sound if it's already playing
            self.sounds[sound_name].play()

    def stop(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()