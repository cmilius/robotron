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

        self.sounds = {
            "enforcer_fire": pygame.mixer.Sound(AUDIO_FILEPATH + "enforcer_fire.wav"),
            "grunt_walk": pygame.mixer.Sound(AUDIO_FILEPATH + "grunt_walk.wav"),
            "hero_death": pygame.mixer.Sound(AUDIO_FILEPATH + "hero_death.wav"),
            "hero_lazer": pygame.mixer.Sound(AUDIO_FILEPATH + "hero_lazer.wav"),
            "human_die": pygame.mixer.Sound(AUDIO_FILEPATH + "human_die.wav"),
            "human_save": pygame.mixer.Sound(AUDIO_FILEPATH + "human_save.wav"),
            "level_transition": pygame.mixer.Sound(AUDIO_FILEPATH + "level_transition.wav"),
            "prog_transformation": pygame.mixer.Sound(AUDIO_FILEPATH + "prog_transformation.wav"),
            "quark_spawn": pygame.mixer.Sound(AUDIO_FILEPATH + "quark_spawn.wav"),
            "tank_explode": pygame.mixer.Sound(AUDIO_FILEPATH + "tank_explode.wav"),
            "tank_fire": pygame.mixer.Sound(AUDIO_FILEPATH + "tank_fire.wav"),
            "tank_projectile_bounce": pygame.mixer.Sound(AUDIO_FILEPATH + "tank_projectile_bounce.wav")
            
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