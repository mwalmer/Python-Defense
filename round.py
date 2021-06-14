import pygame
from helper_functions import scale
from enemy import Enemy
UP, LEFT, DOWN, RIGHT = 0, 90, 180, 270


class Rounds:
    # TODO: remove enemy_size and enemy_sprite, class round shouldn't need to know about the enemies
    def __init__(self, start_cords, enemy_size, enemy_sprite, wave=1):
        self.enemy_size = enemy_size
        self.enemy_sprite = enemy_sprite
        self.x, self.y = start_cords
        self.wave = wave

    def spawn(self, num_enemies, speed, enemy_size, enemy_sprite):
        enemies = []
        for count in range(0, num_enemies):
            enemy_rect = pygame.Rect(0, 0, enemy_size, enemy_size)
            enemy = Enemy(f'enemy_{count}', 100, speed, enemy_rect, enemy_sprite)
            enemy.face(DOWN)
            enemy.y = Enemy.enemy_count * scale(-32)  # separates enemies when they spawn
            enemy.x = self.x
            enemies.append(enemy)
        return enemies

    def level(self):
        enemies = []
        if self.wave == 1:
            e1 = self.spawn(5, 5, self.enemy_size, self.enemy_sprite)
            enemies = e1
        elif self.wave == 2:
            e1 = self.spawn(5, 5, self.enemy_size, self.enemy_sprite)
            e2 = self.spawn(30, 5, self.enemy_size, self.enemy_sprite)
            enemies = e1 + e2
        elif self.wave == 3:
            e1 = self.spawn(5, 5, self.enemy_size, self.enemy_sprite)
            e2 = self.spawn(3, 5, self.enemy_size, self.enemy_sprite)
            enemies = e1 + e2
        return enemies

    def next_wave(self):
        self.wave += 1
