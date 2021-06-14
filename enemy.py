import pygame.transform


class Enemy:
    enemy_count = 0  # static variable, used to track number of enemies

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
        Enemy.enemy_count += 1

    def face(self, deg):
        self.sprite = pygame.transform.rotate(self._sprite, deg)

    def cords(self):
        return self.x, self.y

    def check_health(self):
        if self.health <= 0:
            return True
