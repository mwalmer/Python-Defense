from enemy import Enemy
from tower import Tower
from player import Player
from round import Rounds
from helper_functions import scale, set_ratio
import pygame
import os


pygame.display.init()
display_info = pygame.display.Info()
width = display_info.current_w
height = display_info.current_h

# Scaling pixels to fixed ratio
# adjust this to change window size
if height > width:
    ratio = 1.5 if height <= 1920 else 2
    set_ratio(ratio)
else:
    ratio = 1.5 if width <= 1920 else 2
    set_ratio(ratio)

# Default tile size
TILE_SIZE = scale(32)
TILE_XY = (TILE_SIZE, TILE_SIZE)

NUM_TILES_X, NUM_TILES_Y = 25, 20

WIDTH = TILE_SIZE * NUM_TILES_X
HEIGHT = TILE_SIZE * NUM_TILES_Y


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Defense")

FPS = 60

# Directions
UP, LEFT, DOWN, RIGHT = 0, 90, 180, 270

# Sizes
TOWER_SIZE = TILE_SIZE
ENEMY_SIZE = TILE_SIZE
FIRE_PROJECTILE_SIZE = scale(16)

# Load image
GRASS_TILE = pygame.image.load(os.path.join('assets', 'tiles', 'grass_tile.png'))
DIRT_TILE = pygame.image.load(os.path.join('assets', 'tiles', 'dirt_tile.png'))
MENU_TILE = pygame.image.load(os.path.join('assets', 'tiles', 'menu_tile.png'))
TOWER1_SPRITE = pygame.image.load(os.path.join('assets', 'towers', 'tower1.png'))
TOWER2_SPRITE = pygame.image.load(os.path.join('assets', 'towers', 'tower2.png'))
TOWER3_SPRITE = pygame.image.load(os.path.join('assets', 'towers', 'tower3.png'))
TOWER4_SPRITE = pygame.image.load(os.path.join('assets', 'towers', 'tower4.png'))
TOWER5_SPRITE = pygame.image.load(os.path.join('assets', 'towers', 'tower5.png'))
ENEMY1_SPRITE = pygame.image.load(os.path.join('assets', 'enemies', 'enemy1.png'))
ENEMY2_SPRITE = pygame.image.load(os.path.join('assets', 'enemies', 'enemy2.png'))
ENEMY3_SPRITE = pygame.image.load(os.path.join('assets', 'enemies', 'enemy3.png'))
FIRE_PROJECTILE_SPRITE = pygame.image.load(os.path.join('assets', 'projectiles', 'fireball.png'))

# Scale images
GRASS_TILE = pygame.transform.scale(GRASS_TILE, TILE_XY)
DIRT_TILE = pygame.transform.scale(DIRT_TILE, TILE_XY)
MENU_TILE = pygame.transform.scale(MENU_TILE, TILE_XY)
TOWER1_SPRITE = pygame.transform.scale(TOWER1_SPRITE, (TOWER_SIZE, TOWER_SIZE))
TOWER2_SPRITE = pygame.transform.scale(TOWER2_SPRITE, (TOWER_SIZE, TOWER_SIZE))
TOWER3_SPRITE = pygame.transform.scale(TOWER3_SPRITE, (TOWER_SIZE, TOWER_SIZE))
TOWER4_SPRITE = pygame.transform.scale(TOWER4_SPRITE, (TOWER_SIZE, TOWER_SIZE))
TOWER5_SPRITE = pygame.transform.scale(TOWER5_SPRITE, (TOWER_SIZE, TOWER_SIZE))
ENEMY1_SPRITE = pygame.transform.scale(ENEMY1_SPRITE, (ENEMY_SIZE, ENEMY_SIZE))
ENEMY2_SPRITE = pygame.transform.scale(ENEMY2_SPRITE, (ENEMY_SIZE, ENEMY_SIZE))
ENEMY3_SPRITE = pygame.transform.scale(ENEMY3_SPRITE, (ENEMY_SIZE, ENEMY_SIZE))
FIRE_PROJECTILE_SPRITE = pygame.transform.scale(FIRE_PROJECTILE_SPRITE, (FIRE_PROJECTILE_SIZE, FIRE_PROJECTILE_SIZE))


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
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2]]
# MAP IS 25 ACROSS AND 20 DOWN, 5 last columns are for menu


# Only finds starting x cord, fine for now
# y is set to 0
def to_start():
    temp_count = 0
    y = 0
    for i in MAP[0]:
        if i != 1:
            temp_count += 1
        else:
            return scale(temp_count * 32), y


def update(enemies, towers, R):
    pixel_per_frame = scale(1)
    to_remove = []
    for tower in towers:
        pass

    for enemy in enemies:
        enemy.check_health()
        enemy_pathfinding(enemy)
        enemy.y += pixel_per_frame * enemy.speed * enemy.y_weight
        enemy.x += pixel_per_frame * enemy.speed * enemy.x_weight

        if enemy.check_health():
            to_remove.append(enemy)
        elif enemy.y > HEIGHT:
            to_remove.append(enemy)

    for enemy in to_remove:
        enemies.remove(enemy)
        Enemy.enemy_count -= 1


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

            WIN.blit(tile, (y * TILE_SIZE, x * TILE_SIZE))
    # Scale sprites
    for enemy in enemies:
        WIN.blit(enemy.sprite, enemy.cords())
    for tower in towers:
        WIN.blit(tower.sprite, tower.cords())
    pygame.display.update()


def enemy_pathfinding(enemy):
    # TODO: make dynamic pathfinding
    if enemy.x == scale(96) and enemy.y < scale(128):
        enemy.x_weight, enemy.y_weight = 0, 1
    elif enemy.x < scale(416) and scale(128) <= enemy.y < scale(350):
        enemy.face(RIGHT)
        enemy.x_weight, enemy.y_weight = 1, 0
        enemy.y = scale(128) if enemy.y > scale(128) else enemy.y
    elif enemy.x >= scale(416) and enemy.y < scale(352):
        enemy.face(DOWN)
        enemy.x_weight, enemy.y_weight = 0, 1
        enemy.x = scale(416) if enemy.x > scale(416) else enemy.x
    elif enemy.x > scale(224) and enemy.y >= scale(352):
        enemy.face(LEFT)
        enemy.x_weight, enemy.y_weight = -1, 0
        enemy.y = scale(352) if enemy.y >= scale(352) else enemy.y
    else:
        enemy.face(DOWN)
        enemy.x_weight, enemy.y_weight = 0, 1
        enemy.x = scale(224) if enemy.x < scale(224) else enemy.x


def spawn(enemies, Count, Speed):
    for count in range(0, Count):
        enemy_rect = pygame.Rect(0, 0, ENEMY_SIZE, ENEMY_SIZE)
        enemy = Enemy(f'enemy_{count}', 100, Speed, enemy_rect, ENEMY3_SPRITE)
        enemy.face(DOWN)
        enemy.y = count * scale(-32)
        enemy.x = to_start()
        enemies.append(enemy)


def level(enemies, Lv):
    if Lv == 1:
        spawn(enemies, 10, 5)

    if Lv == 2:
        spawn(enemies, 5, 1)
        spawn(enemies, 3, 2)


def main():
    # TODO: enemy path finding
    player_health = 100
    player = Player(player_health)

    count = 1
    print(to_start())
    R = Rounds(to_start(), ENEMY_SIZE, ENEMY1_SPRITE)
    enemies = R.level()

    towers = []
    #
    # for x in range(0, 2):
    #     tower_rect = pygame.Rect(2, 2, TOWER_WIDTH, TOWER_HEIGHT)
    #     tower = Tower(f'tower_{x}', 10, 3, tower_rect, TOWER1_SPRITE)
    #     towers.append(tower)

    clock = pygame.time.Clock()
    run = True
    tower_count = 0
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                #  TODO: reformat
                if MAP[mouse_y // scale(32)][mouse_x // scale(32)] == 0:
                    MAP[mouse_y // scale(32)][mouse_x // scale(32)] = 3
                    tower_rect = pygame.Rect((mouse_x // scale(32)) * scale(32), (mouse_y // scale(32)) * scale(32),
                                             TOWER_SIZE, TOWER_SIZE)
                    fireball_rect = pygame.Rect((mouse_x // scale(32)) * scale(32), (mouse_y // scale(32)) * scale(32),
                                                FIRE_PROJECTILE_SIZE, FIRE_PROJECTILE_SIZE)
                    towers.append(Tower(f'tower_{tower_count}', 10, 3, tower_rect, TOWER1_SPRITE, "Fireball",
                                        fireball_rect, FIRE_PROJECTILE_SPRITE))
                    tower_count += 1

        # TODO: might want to move to update
        # handles level ending and spawning new wave
        if Enemy.enemy_count == 0:
            R.next_wave()
            enemies = R.level()

        # update logic
        update(enemies, towers, R)

        # refresh/redraw display
        draw_window(enemies, towers)

    pygame.quit()


if __name__ == '__main__':
    main()
