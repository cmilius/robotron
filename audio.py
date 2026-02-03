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
            "hero_lazer": pygame.mixer.Sound(AUDIO_FILEPATH + "hero_lazer.wav"),
            "hero_death": pygame.mixer.Sound(AUDIO_FILEPATH + "hero_death.wav"),
            "human_save": pygame.mixer.Sound(AUDIO_FILEPATH + "human_save.wav"),
            "level_transition": pygame.mixer.Sound(AUDIO_FILEPATH + "level_transition.wav")
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