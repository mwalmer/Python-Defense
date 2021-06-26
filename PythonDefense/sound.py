import pygame


class Sound:
    def __init__(self, sound_name):
        self.sound_name = pygame.mixer.Sound(sound_name)

    def play_sound(self):
        self.sound_name.play()
