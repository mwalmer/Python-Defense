import pygame
from numpy.random import random

from PythonDefense.helper_functions import scale
from PythonDefense.enemy import Enemy

# Directions
UP, LEFT, DOWN, RIGHT = 0, 90, 180, 270


class Rounds:
    # TODO: remove enemy_size and enemy_sprite, class round shouldn't need to know about the enemies
    # changed round initialization to 0 so 1st level doesn't start until button is pressed
    def __init__(self, start_cords, enemy_size, enemy_sprite, enemy_sprite2, enemy_sprite3, enemy_sprite4,
                 enemy_sprite5, enemy_sprite6, round=0):
        self.enemy_size = enemy_size
        self.enemy_sprite = enemy_sprite
        self.enemy_sprite2 = enemy_sprite2
        self.enemy_sprite3 = enemy_sprite3
        self.enemy_sprite4 = enemy_sprite4
        self.enemy_sprite5 = enemy_sprite5
        self.enemy_sprite6 = enemy_sprite6
        self.x, self.y = start_cords
        self.round = round

    def spawn(self, num_enemies, enemy_Sep, health, speed, enemy_size, enemy_sprite, value):
        enemies = []
        for count in range(0, num_enemies):
            enemy_rect = pygame.Rect(0, 0, enemy_size, enemy_size)
            enemy = Enemy(f'enemy_{count}', health, speed, enemy_rect, enemy_sprite, value)
            enemy.face(DOWN)
            enemy.y = Enemy.enemy_count * scale(enemy_Sep)  # separates enemies when they spawn
            # default is -32
            enemy.x = self.x
            enemies.append(enemy)
        return enemies

    def level(self):
        enemies = []
        if self.round == 1:
            enemies1 = self.SoldierEn(500, -.5)
            enemies = enemies1
        elif self.round == 2:
            enemies1 = self.weakEn(10, -24)
            enemies = enemies1
        elif self.round == 3:
            enemies1 = self.weakEn(6, -32)
            enemies2 = self.SoldierEn(2, -32)
            enemies = enemies1 + enemies2
        elif self.round == 4:
            enemies1 = self.weakEn(10, -32)
            enemies2 = self.SoldierEn(4, -32)
            enemies = enemies1 + enemies2
        elif self.round == 5:
            enemies1 = self.tankEn(4, -32)
            enemies = enemies1
        elif self.round == 6:
            enemies1 = self.tankEn(2, -32)
            enemies2 = self.SoldierEn(6, -22)
            enemies = enemies1 + enemies2
        elif self.round == 7:
            enemies1 = self.scoutEn(5, -32)
            enemies = enemies1
        elif self.round == 8:
            enemies1 = self.weakEn(20, -32)
            enemies = enemies1
        elif self.round == 9:
            enemies1 = self.SoldierEn(10, -32)
            enemies2 = self.scoutEn(4, -32)
            enemies = enemies1 + enemies2
        elif self.round == 10:
            enemies1 = self.tankEn(6, -32)
            enemies2 = self.scoutEn(6, -32)
            enemies = enemies1 + enemies2
        elif self.round > 10:
            enemies3 = self.tankEn(int(self.round / 2 * random()), -1 * int(18 * random()) - 20)
            enemies4 = self.SoldierEn(int(self.round / 2 * random()), -1 * int(18 * random()) - 20)
            enemies2 = self.scoutEn(int(self.round / 2 * random()), -1 * int(18 * random()) - 20)
            enemies1 = self.weakEn(int(self.round / 2 * random()), -1 * int(18 * random()) - 20)
            enemies = enemies1 + enemies2 + enemies3 + enemies4
        return enemies

    def next_round(self):
        self.round += 1

    def last_round(self):
        return self.round == 15

    # slow and tanky
    def tankEn(self, num, sep):
        return self.spawn(num, sep, 15, 1, self.enemy_size, self.enemy_sprite4, 4)

    # fast and weak
    def scoutEn(self, num, sep):
        return self.spawn(num, sep, 5, 12, self.enemy_size, self.enemy_sprite3, 3)

    # generalist
    def SoldierEn(self, num, sep):
        return self.spawn(num, sep, 4, 3, self.enemy_size, self.enemy_sprite, 2)

    # these guys suck
    def weakEn(self, num, sep):
        return self.spawn(num, sep, 2, 2, self.enemy_size, self.enemy_sprite6, 1)
