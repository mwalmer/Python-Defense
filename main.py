from enemy import Enemy
from tower import Tower
from player import Player
import pygame
import os

WIDTH, HEIGHT = 800, 640
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Defense")

FPS = 60

# Directions
UP, LEFT, DOWN, RIGHT = 0, 90, 180, 270

# Sizes
TILE_WIDTH, TILE_HEIGHT = 32, 32
TOWER_WIDTH, TOWER_HEIGHT = 28, 28
ENEMY_WIDTH, ENEMY_HEIGHT = 16, 16

# Load image
GRASS_TILE = pygame.image.load(os.path.join('assets', 'tiles', 'grass_tile.png'))
DIRT_TILE = pygame.image.load(os.path.join('assets', 'tiles', 'dirt_tile.png'))
MENU_TILE = pygame.image.load(os.path.join('assets', 'tiles', 'menu_tile.png'))
TOWER_SPRITE = pygame.image.load(os.path.join('assets', 'towers', 'tower.png'))
ENEMY_SPRITE = pygame.image.load(os.path.join('assets', 'enemies', 'enemy.png'))

# 0 = grass
# 1 = dirt
# 2 = menu area
MAP = [[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2]]


def update(enemies, towers):
    pixel_per_frame = 1
    for enemy in enemies:
        enemy_pathfinding(enemy)
        enemy.y += pixel_per_frame * enemy.speed * enemy.y_weight
        enemy.x += pixel_per_frame * enemy.speed * enemy.x_weight


def draw_window(enemies, towers):
    # draws map
    for x, row in enumerate(MAP):
        tile = GRASS_TILE
        for y, cord in enumerate(row):
            # draws grass and path
            # needs to be drawn before enemies or towers
            if cord == 0:
                tile = GRASS_TILE
            elif cord == 1:
                tile = DIRT_TILE
            elif cord == 2:
                tile = MENU_TILE
            elif cord == 3:
                tile = TOWER_SPRITE
            WIN.blit(tile, (y * 32, x * 32))

    for enemy in enemies:
        WIN.blit(enemy.sprite, enemy.cords())
    for tower in towers:
        WIN.blit(tower.sprite, tower.cords())

    pygame.display.update()


def to_start():
    temp_count = 0
    for i in MAP[0]:
        if i != 1:
            temp_count += 1
        else:
            return temp_count * 32 + 8


def enemy_pathfinding(enemy):
    # TODO -- fix this up more, right now just turns the enemy right
    if enemy.x == 104 and enemy.y < 136:
        enemy.x_weight, enemy.y_weight = 0, 1
    elif enemy.x < 424 and enemy.y == 136:
        enemy.face(RIGHT)
        enemy.x_weight, enemy.y_weight = 1, 0
    elif enemy.x == 424 and enemy.y < 360:
        enemy.face(DOWN)
        enemy.x_weight, enemy.y_weight = 0, 1
    elif enemy.x >= 234 and enemy.y == 360:
        enemy.face(LEFT)
        enemy.x_weight, enemy.y_weight = -1, 0
    else:
        enemy.face(DOWN)
        enemy.x_weight, enemy.y_weight = 0, 1
    # if ((enemy.y + 32) // 32) < 20 and MAP[int((enemy.y + 32) // 32)][int(enemy.x // 32)] == 0 and enemy.x > 0 and enemy.y > 0:
    #     enemy.face(RIGHT)


def spawn(enemies, Count, Speed):
    for count in range(0, Count):
        enemy_rect = pygame.Rect(8, 8, ENEMY_WIDTH, ENEMY_HEIGHT)
        enemy = Enemy(f'enemy_{count}', 100, Speed, enemy_rect, ENEMY_SPRITE)
        enemy.face(DOWN)
        enemy.y = count * -32
        enemy.x = to_start()
        enemies.append(enemy)


def main():
    # TODO: enemy path finding
    player_health = 100
    player = Player(player_health)

    enemies = []
    spawn(enemies, 20,2)

    towers = []
    #
    # for x in range(0, 2):
    #     tower_rect = pygame.Rect(2, 2, TOWER_WIDTH, TOWER_HEIGHT)
    #     tower = Tower(f'tower_{x}', 10, 3, tower_rect, TOWER_SPRITE)
    #     towers.append(tower)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if MAP[mouse_y//32][mouse_x//32] == 0:
                    MAP[mouse_y // 32][mouse_x // 32] = 3

        # update logic
        update(enemies, towers)

        # refresh/redraw display
        draw_window(enemies, towers)

    pygame.quit()


if __name__ == '__main__':
    main()
