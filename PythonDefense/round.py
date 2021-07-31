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
            enemies1 = self.weakEn(8, -36)
            enemies = enemies1
        elif self.round == 2:
            enemies1 = self.weakEn(10, -24)
            enemies = enemies1
        elif self.round == 3:
            enemies1 = self.weakEn(20, -38)
            enemies = enemies1
        elif self.round == 4:
            enemies1 = self.weakEn(6, -32)
            enemies2 = self.SoldierEn(2, -32)
            enemies = enemies1 + enemies2
        elif self.round == 5:
            enemies1 = self.weakEn(8, -32)
            enemies2 = self.SoldierEn(4, -38)
            enemies = enemies1 + enemies2
        elif self.round == 6:
            enemies1 = self.tankEn(2, -32)
            enemies = enemies1
        elif self.round == 7:
            enemies1 = self.tankEn(2, -32)
            enemies2 = self.SoldierEn(6, -36)
            enemies = enemies1 + enemies2
        elif self.round == 8:
            enemies1 = self.SoldierEn(6, -32)
            enemies2 = self.weakEn(20, -28)
            enemies = enemies1 + enemies2
        elif self.round == 9:
            enemies1 = self.scoutEn(5, -38)
            enemies = enemies1
        elif self.round == 10:
            enemies1 = self.weakEn(30, -24)
            enemies = enemies1
        elif self.round == 11:
            enemies1 = self.SoldierEn(6, -32)
            enemies2 = self.scoutEn(4, -32)
            enemies = enemies1 + enemies2
        elif self.round == 12:
            enemies1 = self.tankEn(6, -32)
            enemies2 = self.scoutEn(6, -32)
            enemies = enemies1 + enemies2
        elif self.round == 13:
            enemies1 = self.weakEn(25, -18)
            enemies2 = self.SoldierEn(6, -32)
            enemies = enemies1 + enemies2
        elif self.round == 14:
            enemies1 = self.weakEn(5, -32)
            enemies2 = self.tankEn(4, -32)
            enemies3 = self.SoldierEn(4, -32)
            enemies4 = self.scoutEn(4, -32)
            enemies = enemies1 + enemies2 + enemies3 + enemies4
        elif self.round == 15:
            enemies1 = self.scoutEn(8, -32)
            enemies2 = self.tankEn(6, -32)
            enemies3 = self.SoldierEn(5, -32)
            enemies4 = self.weakEn(12, -20)
            enemies = enemies1 + enemies2 + enemies3 + enemies4
        elif self.round == 16:
            enemies1 = self.tankEn(4, -52)
            enemies2 = self.SoldierEn(8, -32)
            enemies3 = self.tankEn(4, -32)
            enemies4 = self.SoldierEn(8, -32)
            enemies = enemies1 + enemies2 + enemies3 + enemies4
        elif self.round == 17:
            enemies1 = self.tankEn(5, -52)
            enemies2 = self.scoutEn(4, -32)
            enemies3 = self.tankEn(5, -32)
            enemies4 = self.scoutEn(4, -32)
            enemies = enemies1 + enemies2 + enemies3 + enemies4
        elif self.round == 18:
            enemies1 = self.tankEn(10, -26)
            enemies2 = self.scoutEn(4, -32)
            enemies3 = self.weakEn(20, -48)
            enemies4 = self.scoutEn(6, -32)
            enemies = enemies1 + enemies2 + enemies3 + enemies4
        elif self.round == 19:
            enemies1 = self.tankEn(10, -24)
            enemies2 = self.scoutEn(4, -32)
            enemies3 = self.weakEn(18, -24)
            enemies4 = self.SoldierEn(10, -32)
            enemies = enemies1 + enemies2 + enemies3 + enemies4
        elif self.round == 20:
            enemies1 = self.SoldierEn(20, -32)
            enemies2 = self.scoutEn(4, -32)
            enemies3 = self.weakEn(15, -24)
            enemies4 = self.SoldierEn(10, -32)
            enemies = enemies1 + enemies2 + enemies3 + enemies4
        elif self.round == 21:
            enemies1 = self.SoldierEn(20, -36)
            enemies2 = self.tankEn(10, -38)
            enemies3 = self.scoutEn(8, -36)
            enemies4 = self.SoldierEn(15, -36)
            enemies = enemies1 + enemies2 + enemies3 + enemies4
        elif self.round == 22:
            enemies1 = self.SoldierEn(11, -50)
            enemies2 = self.SoldierEn(11, -40)
            enemies3 = self.SoldierEn(11, -30)
            enemies4 = self.SoldierEn(11, -22)
            enemies = enemies1 + enemies2 + enemies3 + enemies4
        elif self.round == 23:
            enemies1 = self.tankEn(10, -42)
            enemies2 = self.SoldierEn(12, -38)
            enemies3 = self.scoutEn(18, -28)
            enemies = enemies1 + enemies2 + enemies3
        elif self.round == 24:
            enemies1 = self.weakEn(8, -36)
            enemies = enemies1
        elif self.round == 25:
            enemies1 = self.tankEn(16, -42)
            enemies2 = self.SoldierEn(25, -20)
            enemies3 = self.scoutEn(18, -28)
            enemies4 = self.SoldierEn(45, -26)
            enemies = enemies1 + enemies2 + enemies3 + enemies4
        elif self.round > 25:
            enemies3 = self.tankEn(int(self.round / 2 * random()), -1 * int(18 * random()) - 20)
            enemies4 = self.SoldierEn(int(self.round * random()), -20)
            enemies2 = self.scoutEn(int(self.round / 2 * random()), -1 * int(18 * random()) - 20)
            enemies1 = self.weakEn(int(self.round * random()), -1 * int(18 * random()) - 20)
            enemies = enemies1 + enemies2 + enemies3 + enemies4
        return enemies

    def next_round(self):
        self.round += 1

    def last_round(self):
        return self.round == 25

    # slow and tanky
    def tankEn(self, num, sep):
        return self.spawn(num, sep, 16, 1, self.enemy_size, self.enemy_sprite4, 5)

    # fast and weak
    def scoutEn(self, num, sep):
        return self.spawn(num, sep, 2, 5, self.enemy_size, self.enemy_sprite3, 3)

    # generalist
    def SoldierEn(self, num, sep):
        return self.spawn(num, sep, 3, 3.1, self.enemy_size, self.enemy_sprite, 3) #3.1 fixes a bug, don't change to 3

    # these guys suck
    def weakEn(self, num, sep):
        return self.spawn(num, sep, 1, 2, self.enemy_size, self.enemy_sprite2, 1)
