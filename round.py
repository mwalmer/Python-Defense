import pygame
from helper_functions import scale
from enemy import Enemy
UP, LEFT, DOWN, RIGHT = 0, 90, 180, 270


class Rounds:
    # TODO: remove enemy_size and enemy_sprite, class round shouldn't need to know about the enemies
    def __init__(self, start_cords, enemy_size, enemy_sprite):
        self.enemy_size = enemy_size
        self.enemy_sprite = enemy_sprite
        self.x, self.y = start_cords

    def spawn(self, enemies, num_enemies, speed, enemy_size, enemy_sprite):
        for count in range(0, num_enemies):
            enemy_rect = pygame.Rect(0, 0, enemy_size, enemy_size)
            enemy = Enemy(f'enemy_{count}', 100, speed, enemy_rect, enemy_sprite)
            enemy.face(DOWN)
            enemy.y = count * scale(-32)  # separates enemies when they spawn
            enemy.x = self.x
            enemies.append(enemy)

    def level(self, enemies, lv):
        if lv == 1:
            self.spawn(enemies, 5, 1, self.enemy_size, self.enemy_sprite)
        elif lv == 2:
            self.spawn(enemies, 5, 1, self.enemy_size, self.enemy_sprite)
            self.spawn(enemies, 3, 2, self.enemy_size, self.enemy_sprite)
