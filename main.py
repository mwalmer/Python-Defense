from enemy import Enemy
from tower import Tower
from player import Player
from round import Rounds
import pygame
import os

pygame.display.init()
infoObject = pygame.display.Info()
WIDTH = infoObject.current_w
HEIGHT = infoObject.current_h
# Sets w/h to max of whatever screen we're using
# WIDTH, HEIGHT = 800, 640

# Scaling pixels to screen ratio
if WIDTH > HEIGHT:
    scale = HEIGHT - (HEIGHT % 25) - 50  # -50 is for top window bar
else:
    scale = WIDTH - (WIDTH % 25) - 50

WIN = pygame.display.set_mode((scale, scale))
pygame.display.set_caption("Python Defense")
FPS = 60

# changing scale to be for scaling tiles/towers/etc.
scale = scale / 25

# Directions
UP, LEFT, DOWN, RIGHT = 0, 90, 180, 270

# Sizes
TILE_WIDTH, TILE_HEIGHT = scale, scale
TOWER_WIDTH, TOWER_HEIGHT = 28 / 32 * scale, 28 / 32 * scale
ENEMY_WIDTH, ENEMY_HEIGHT = 16 / 32 * scale, 16 / 32 * scale
FIRE_PROJECTILE_WIDTH, FIRE_PROJECTILE_HEIGHT = 16 / 32 * scale, 16 / 32 * scale

# Load image
GRASS_TILE = pygame.image.load(os.path.join('assets', 'tiles', 'grass_tile.png'))
DIRT_TILE = pygame.image.load(os.path.join('assets', 'tiles', 'dirt_tile.png'))
MENU_TILE = pygame.image.load(os.path.join('assets', 'tiles', 'menu_tile.png'))
TOWER_SPRITE = pygame.image.load(os.path.join('assets', 'towers', 'tower.png'))
ENEMY_SPRITE = pygame.image.load(os.path.join('assets', 'enemies', 'enemy.png'))
FIRE_PROJECTILE_SPRITE = pygame.image.load(os.path.join('assets', 'projectiles', 'fireball.png'))

# Scale images
GRASS_TILE = pygame.transform.scale(GRASS_TILE, (int(TILE_WIDTH), int(TILE_HEIGHT)))
DIRT_TILE = pygame.transform.scale(DIRT_TILE, (int(TILE_WIDTH), int(TILE_HEIGHT)))
MENU_TILE = pygame.transform.scale(MENU_TILE, (int(TILE_WIDTH), int(TILE_HEIGHT)))
TOWER_SPRITE = pygame.transform.scale(TOWER_SPRITE, (int(TOWER_WIDTH), int(TOWER_HEIGHT)))
ENEMY_SPRITE = pygame.transform.scale(ENEMY_SPRITE, (int(ENEMY_WIDTH), int(ENEMY_HEIGHT)))
FIRE_PROJECTILE_SPRITE = pygame.transform.scale(FIRE_PROJECTILE_SPRITE, (int(ENEMY_WIDTH), int(ENEMY_HEIGHT)))

# 0 = grass
# 1 = dirt
# 2 = menu area
# 3 = grass_with_tower: just renders the grass again but reassigns the value to 3 so we know a towerHasAlreadyBeenPlaced
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
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2]]


# MAP IS 25 ACROSS AND 25 DOWN, 5 last columns are for menu



def update(enemies, towers):
    pixel_per_frame = 1
    for enemy in enemies:
        enemy_pathfinding(enemy)
        enemy.y += pixel_per_frame * enemy.speed * enemy.y_weight
        enemy.x += pixel_per_frame * enemy.speed * enemy.x_weight
    for tower in towers:
        pass


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
                tile = GRASS_TILE
            WIN.blit(tile, (y * TILE_HEIGHT, x * TILE_WIDTH))
    # Scale sprites
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

def level(enemies, Lv):
    if Lv == 1:
        spawn(enemies, 5, 1)

    if Lv == 2:
        spawn(enemies, 5, 1)
        spawn(enemies, 3, 2)


def main():
    # TODO: enemy path finding
    player_health = 100
    player = Player(player_health)

    enemies = []
    count = 1
    R = Rounds(ENEMY_SPRITE, ENEMY_HEIGHT,ENEMY_WIDTH, MAP)
    R.level(enemies, count)

    towers = []
    #
    # for x in range(0, 2):
    #     tower_rect = pygame.Rect(2, 2, TOWER_WIDTH, TOWER_HEIGHT)
    #     tower = Tower(f'tower_{x}', 10, 3, tower_rect, TOWER_SPRITE)
    #     towers.append(tower)

    clock = pygame.time.Clock()
    run = True
    tower_count = 0
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if MAP[mouse_y // 32][mouse_x // 32] == 0:
                    MAP[mouse_y // 32][mouse_x // 32] = 3
                    tower_rect = pygame.Rect((mouse_x // 32) * 32, (mouse_y // 32) * 32, TOWER_WIDTH, TOWER_HEIGHT)
                    fireball_rect = pygame.Rect((mouse_x // 32) * 32, (mouse_y // 32) * 32, FIRE_PROJECTILE_WIDTH,
                                                FIRE_PROJECTILE_HEIGHT)
                    towers.append(Tower(f'tower_{tower_count}', 10, 3, tower_rect, TOWER_SPRITE, "Fireball",
                                        fireball_rect, FIRE_PROJECTILE_SPRITE))
                    tower_count += 1

        # update logic
        update(enemies, towers)

        # refresh/redraw display
        draw_window(enemies, towers)

    pygame.quit()


if __name__ == '__main__':
    main()
