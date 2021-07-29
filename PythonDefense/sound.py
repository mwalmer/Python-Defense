import pygame
import os

volume = 0.5


class Sound:
    def __init__(self):
        self.sounds = {
            "collision_sound": pygame.mixer.Sound(
                os.path.join(os.path.dirname(__file__), 'assets', 'sounds', 'Trompo collido.wav')),
            "start_button_sound": pygame.mixer.Sound(
                os.path.join(os.path.dirname(__file__), 'assets', 'sounds', 'start_button.wav')),
            "upgrade_button_sound": pygame.mixer.Sound(
                os.path.join(os.path.dirname(__file__), 'assets', 'sounds', 'upgrade_button.wav')),
            "tower_placement_sound": pygame.mixer.Sound(
                os.path.join(os.path.dirname(__file__), 'assets', 'sounds', 'tower_placement.wav')),
            "tower_grab_sound": pygame.mixer.Sound(
                os.path.join(os.path.dirname(__file__), 'assets', 'sounds', 'tower_grab.wav')),
            "lose_life_even_sound": pygame.mixer.Sound(
                os.path.join(os.path.dirname(__file__), 'assets', 'sounds', 'lose_life_even.wav')),
            "lose_life_odd_sound": pygame.mixer.Sound(
                os.path.join(os.path.dirname(__file__), 'assets', 'sounds', 'lose_life_odd.wav')),
            "menu_sound": pygame.mixer.Sound(
                os.path.join(os.path.dirname(__file__), 'assets', 'sounds', 'menu_sound.wav'))
        }
        for sounds in self.sounds:
            self.sounds[sounds].set_volume(volume)

    def play_sound(self, sound_name):
        (self.sounds[sound_name]).play()

    def set_volume(self, new_volume):
        for sounds in self.sounds:
            self.sounds[sounds].set_volume(new_volume)
