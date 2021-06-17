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
GRASS_TILE = pygame.image.load(os.path.join('assets', 'tiles', 'grass_tile.png')).convert()
DIRT_TILE = pygame.image.load(os.path.join('assets', 'tiles', 'dirt_tile.png')).convert()
MENU_TILE = pygame.image.load(os.path.join('assets', 'tiles', 'menu_tile.png')).convert()
TOWER1_SPRITE = pygame.image.load(os.path.join('assets', 'towers', 'tower1.png')).convert_alpha()
TOWER2_SPRITE = pygame.image.load(os.path.join('assets', 'towers', 'tower2.png')).convert_alpha()
TOWER3_SPRITE = pygame.image.load(os.path.join('assets', 'towers', 'tower3.png')).convert_alpha()
TOWER4_SPRITE = pygame.image.load(os.path.join('assets', 'towers', 'tower4.png')).convert_alpha()
TOWER5_SPRITE = pygame.image.load(os.path.join('assets', 'towers', 'tower5.png')).convert_alpha()
ENEMY1_SPRITE = pygame.image.load(os.path.join('assets', 'enemies', 'enemy1.png')).convert_alpha()
ENEMY2_SPRITE = pygame.image.load(os.path.join('assets', 'enemies', 'enemy2.png')).convert_alpha()
ENEMY3_SPRITE = pygame.image.load(os.path.join('assets', 'enemies', 'enemy3.png')).convert_alpha()
FIRE_PROJECTILE_SPRITE = pygame.image.load(os.path.join('assets', 'projectiles', 'fireball.png')).convert()

UPGRADE_SPRITE = pygame.image.load(os.path.join('assets', 'buttons', 'bt-upgrade-red.jpg')).convert_alpha()

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

UPGRADE_SPRITE = pygame.transform.scale(UPGRADE_SPRITE, (TILE_SIZE*2, TILE_SIZE))

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


def update(enemies, towers, rounds, projectiles, ticks):
    pixel_per_frame = scale(1)
    delete_enemies = []
    delete_projectiles = []

    for tower in towers:
        #  checks the towers attack speed before firing
        tower.ticks += ticks
        if tower.ticks >= tower.attack_speed:
            projectiles.append(tower.fire_projectile())
            tower.ticks -= tower.attack_speed

    #  TODO: account for turret range, also what if enemy dies before shot hits
    for projectile in projectiles:
        if len(enemies) != 0:
            x, y = enemies[0].cords()
            projectile.motion(x, y)
            # TODO: add to remove_projectile when done

    for projectile in delete_projectiles:
        projectiles.remove(projectile)

    for enemy in enemies:
        enemy.check_health()
        enemy_pathfinding(enemy)
        enemy.y += pixel_per_frame * enemy.speed * enemy.y_weight
        enemy.x += pixel_per_frame * enemy.speed * enemy.x_weight

        if enemy.check_health():
            delete_enemies.append(enemy)
        elif enemy.y > HEIGHT:
            delete_enemies.append(enemy)

    for enemy in delete_enemies:
        enemies.remove(enemy)
        Enemy.enemy_count -= 1


def draw_window(enemies, towers, projectiles):
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

    for enemy in enemies:
        WIN.blit(enemy.sprite, enemy.cords())
    for tower in towers:
        WIN.blit(tower.sprite, tower.cords())
    for projectile in projectiles:
        WIN.blit(projectile.sprite, projectile.cords())

    WIN.blit(UPGRADE_SPRITE, (20.5*TILE_SIZE, 17*TILE_SIZE))
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


def main():
    # TODO: enemy path finding
    player_health = 100
    player = Player(player_health)

    count = 1
    rounds = Rounds(to_start(), ENEMY_SIZE, ENEMY1_SPRITE)
    enemies = rounds.level()

    towers = []
    projectiles = []

    upgrade_me = None  # temporary placeholder for a clicked tower (USED FOR UPGRADES)

    clock = pygame.time.Clock()
    run = True
    tower_count = 0
    while run:
        ticks = clock.tick(FPS)
        # TODO: limit possible event types
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                #  TODO: reformat
                if MAP[mouse_y // scale(32)][mouse_x // scale(32)] == 0:
                    MAP[mouse_y // scale(32)][mouse_x // scale(32)] = 3
                    temp_x, temp_y = (mouse_x // scale(32)) * scale(32), (mouse_y // scale(32)) * scale(32)
                    tower_rect = pygame.Rect(temp_x, temp_y, TOWER_SIZE, TOWER_SIZE)
                    fireball_rect = pygame.Rect(temp_x, temp_y, FIRE_PROJECTILE_SIZE, FIRE_PROJECTILE_SIZE)
                    towers.append(Tower(f'tower_{tower_count}', 10, 3, tower_rect, TOWER1_SPRITE, "Fireball",
                                        fireball_rect, FIRE_PROJECTILE_SPRITE, ticks))
                    tower_count += 1

                # Checks if click was over a tower and then proceeds with upgrading tower
                if MAP[mouse_y // scale(32)][mouse_x // scale(32)] == 3:
                    temp_x, temp_y = (mouse_x // scale(32)) * scale(32), (mouse_y // scale(32)) * scale(32)

                    # Finds which tower was clicked
                    for tower in towers:
                        if tower.cords() == (temp_x, temp_y):
                            # TODO Display an upgrade button with details of the cost of the upgrade
                            upgrade_me = tower
                            # tower.basic_upgrade(5, 5)

                if mouse_y >= TILE_SIZE*17 and mouse_y <= TILE_SIZE*17 + TILE_SIZE:
                    if mouse_x >= TILE_SIZE*20.5 and mouse_x <=TILE_SIZE*20.5 + TILE_SIZE*2:
                        if upgrade_me is not None:
                            upgrade_me.basic_upgrade(5, 5)
                            print("UPGRADE SUCCEEDED")
                            # upgrade_me = None

        # TODO: might want to move to update
        # handles level ending and spawning new wave
        if Enemy.enemy_count == 0:
            rounds.next_round()
            enemies = rounds.level()

        # update logic
        update(enemies, towers, rounds, projectiles, ticks)

        # refresh/redraw display
        draw_window(enemies, towers, projectiles)

    pygame.quit()


if __name__ == '__main__':
    main()
