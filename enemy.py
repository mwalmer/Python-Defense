import pygame.transform


class Enemy:
    def __init__(self, name, health, speed, rect, sprite):
        self.name = name
        self.health = health
        self.speed = speed
        self.rect = rect
        self.x = rect.x
        self.y = rect.y
        self.x_weight = 1
        self.y_weight = 1
        self._sprite = sprite
        self.sprite = sprite

    def face(self, deg):
        self.sprite = pygame.transform.rotate(self._sprite, deg)

    def cords(self):
        return self.x, self.y
