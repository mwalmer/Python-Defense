import pygame
from enemy import Enemy
UP, LEFT, DOWN, RIGHT = 0, 90, 180, 270


class Rounds:
    def __init__(self,ENEMY_SPRITE, ENEMY_HEIGHT,ENEMY_WIDTH, MAP):
        self.ENEMY_SPRITE = ENEMY_SPRITE
        self.ENEMY_HEIGHT = ENEMY_HEIGHT
        self.ENEMY_WIDTH = ENEMY_WIDTH
        self.MAP = MAP

    def to_start(self):
        temp_count = 0
        for i in self.MAP[0]:
            if i != 1:
                temp_count += 1
            else:
                return temp_count * 32 + 8

    def spawn(self, enemies, Count, Speed):
        for count in range(0, Count):
            enemy_rect = pygame.Rect(8, 8, self.ENEMY_WIDTH, self.ENEMY_HEIGHT)
            enemy = Enemy(f'enemy_{count}', 100, Speed, enemy_rect, self.ENEMY_SPRITE)
            enemy.face(DOWN)
            enemy.y = count * -32
            enemy.x = self.to_start()
            enemies.append(enemy)

    def level(self, enemies, Lv):
        if Lv == 1:
            self.spawn(enemies, 5, 1)

        if Lv == 2:
            self.spawn(enemies, 5, 1)
            self.spawn(enemies, 3, 2)
