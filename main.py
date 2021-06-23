from math import floor
import pygame
import os

from enemy import Enemy
from tower import Tower
from player import Player
from round import Rounds
from helper_functions import scale, set_ratio

#  nt is the os.name for windows

pygame.display.init()
display_info = pygame.display.Info()
width = display_info.current_w
height = display_info.current_h
print(height)

# Scaling pixels to fixed ratio
# adjust this to change window size

NUM_TILES_X, NUM_TILES_Y = 25, 20

# test colors/cords for text
pygame.init()
# screen = pygame.display.set_mode((400, 400))
font = pygame.font.SysFont('arial', 32)
text = font.render("test", True, (0, 0, 0))

if os.name != 'nt':
    ratio = 1
elif height > width:
    ratio = 1.5 if height <= 1920 else 2
    set_ratio(ratio)
else:
    ratio = 1.5 if width <= 1920 else 2
    set_ratio(ratio)

# Default tile size
TILE_SIZE = scale(32)
print(TILE_SIZE)
TILE_XY = (TILE_SIZE, TILE_SIZE)

WIDTH = TILE_SIZE * NUM_TILES_X
HEIGHT = TILE_SIZE * NUM_TILES_Y
print(WIDTH)
print(HEIGHT)

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
HILITE_TILE = pygame.image.load(os.path.join('assets', 'buttons', 'hilite.png')).convert_alpha()

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
START_SPRITE = pygame.image.load(os.path.join('assets', 'buttons', 'bt-start.png')).convert_alpha()

# Level tiles for towers
LEVEL1_TILE = pygame.image.load(os.path.join('assets', 'levels', 'num1.png')).convert_alpha()
LEVEL2_TILE = pygame.image.load(os.path.join('assets', 'levels', 'num2.png')).convert_alpha()
LEVEL3_TILE = pygame.image.load(os.path.join('assets', 'levels', 'num3.png')).convert_alpha()
LEVEL4_TILE = pygame.image.load(os.path.join('assets', 'levels', 'num4.png')).convert_alpha()
LEVEL5_TILE = pygame.image.load(os.path.join('assets', 'levels', 'num5.png')).convert_alpha()

# Scale images
GRASS_TILE = pygame.transform.scale(GRASS_TILE, TILE_XY)
DIRT_TILE = pygame.transform.scale(DIRT_TILE, TILE_XY)
MENU_TILE = pygame.transform.scale(MENU_TILE, TILE_XY)
HILITE_TILE = pygame.transform.scale(HILITE_TILE, TILE_XY)

TOWER1_SPRITE = pygame.transform.scale(TOWER1_SPRITE, (TOWER_SIZE, TOWER_SIZE))
TOWER2_SPRITE = pygame.transform.scale(TOWER2_SPRITE, (TOWER_SIZE, TOWER_SIZE))
TOWER3_SPRITE = pygame.transform.scale(TOWER3_SPRITE, (TOWER_SIZE, TOWER_SIZE))
TOWER4_SPRITE = pygame.transform.scale(TOWER4_SPRITE, (TOWER_SIZE, TOWER_SIZE))
TOWER5_SPRITE = pygame.transform.scale(TOWER5_SPRITE, (TOWER_SIZE, TOWER_SIZE))
ENEMY1_SPRITE = pygame.transform.scale(ENEMY1_SPRITE, (ENEMY_SIZE, ENEMY_SIZE))
ENEMY2_SPRITE = pygame.transform.scale(ENEMY2_SPRITE, (ENEMY_SIZE, ENEMY_SIZE))
ENEMY3_SPRITE = pygame.transform.scale(ENEMY3_SPRITE, (ENEMY_SIZE, ENEMY_SIZE))
FIRE_PROJECTILE_SPRITE = pygame.transform.scale(FIRE_PROJECTILE_SPRITE, (FIRE_PROJECTILE_SIZE, FIRE_PROJECTILE_SIZE))

UPGRADE_SPRITE = pygame.transform.scale(UPGRADE_SPRITE, (TILE_SIZE * 2, TILE_SIZE))
START_SPRITE = pygame.transform.scale(START_SPRITE, (TILE_SIZE * 2, TILE_SIZE))

LEVEL1_TILE = pygame.transform.scale(LEVEL1_TILE, TILE_XY)
LEVEL2_TILE = pygame.transform.scale(LEVEL2_TILE, TILE_XY)
LEVEL3_TILE = pygame.transform.scale(LEVEL3_TILE, TILE_XY)
LEVEL4_TILE = pygame.transform.scale(LEVEL4_TILE, TILE_XY)
LEVEL5_TILE = pygame.transform.scale(LEVEL5_TILE, TILE_XY)

# 0 = grass
# 1 = dirt
# 2 = menu area
# 3 = grass_with_tower: just renders the grass again but reassigns the value to 3 so we know a towerHasAlreadyBeenPlaced
# 4-8 = tower icon on menu
# 9 = enemies go left
# 10 = enemies go right
# 11 = down
MAP = [[0, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 2, 5, 2],
       [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 11, 0, 0, 0, 0, 0, 0, 2, 6, 2, 7, 2],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 8, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 11, 1, 1, 1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2]]

# MAP IS 25 ACROSS AND 25 DOWN, 5 last columns are for menu
lives = 25


# Only finds starting x cord, fine for now
# y is set to 0
def to_start():
    temp_count = 0
    y = 0
    for i in MAP[0]:
        if i != 11:
            temp_count += 1
        else:
            return scale(temp_count * 32), y


def clear(enemies, projectiles):
    enemies[:] = []
    projectiles[:] = []


def update(enemies, towers, rounds, projectiles, ticks, player):
    pixel_per_frame = scale(1)

    for tower in towers:
        #  checks the towers attack speed before firing
        tower.ticks += ticks
        if tower.ticks >= tower.attack_speed and tower.any_within_range(enemies):
            projectiles.append(tower.fire_projectile())
            tower.ticks -= tower.attack_speed

    #  TODO: account for turret range, also what if enemy dies before shot hits
    #   might want to optimize later on
    for projectile in projectiles:
        has_not_hit = True
        if len(enemies) != 0:
            x, y = enemies[0].cords()

            projectile.motion(x, y)
            #  TODO: make sure only one enemy is getting hit
            for enemy in enemies:
                if projectile.rect.colliderect(enemy.rect) and has_not_hit:
                    enemy.health -= projectile.damage
                    projectile.flag_removal()
                    has_not_hit = False

    # sets list equal to remaining projectiles
    projectiles[:] = [projectile for projectile in projectiles if not projectile.remove]

    for enemy in enemies:
        enemy_pathfinding(enemy)
        enemy.y += pixel_per_frame * enemy.speed * enemy.y_weight
        enemy.x += pixel_per_frame * enemy.speed * enemy.x_weight
        enemy.rect.x = enemy.x
        enemy.rect.y = enemy.y

        if enemy.check_health():
            player.add_money()
            print('Money ' + str(player.get_money()))
            enemy.flag_removal()
        elif enemy.y > HEIGHT:
            player.take_damage()
            print('health ' + str(player.get_health()))
            enemy.flag_removal()

    # sets list equal to remaining enemies
    enemies[:] = [enemy for enemy in enemies if not enemy.remove]


def draw_window(enemies, towers, projectiles, hilite):
    # draws map
    # Text not working
    WIN.blit(text, (1200, 960))
    for x, row in enumerate(MAP):
        tile = GRASS_TILE
        for y, cord in enumerate(row):
            # draws grass and path
            # needs to be drawn before enemies or towers

            # Rename cord to a more fitting var name
            if cord == 0:
                tile = GRASS_TILE
            elif cord == 1:
                tile = DIRT_TILE
            elif cord == 2:
                tile = MENU_TILE
            elif cord == 3:
                tile = GRASS_TILE
            elif cord == 4:
                tile = TOWER1_SPRITE
            elif cord == 5:
                tile = TOWER2_SPRITE
            elif cord == 6:
                tile = TOWER3_SPRITE
            elif cord == 7:
                tile = TOWER4_SPRITE
            elif cord == 8:
                tile = TOWER5_SPRITE
            elif cord == 9:
                tile = DIRT_TILE
            elif cord == 10:
                tile = DIRT_TILE
            elif cord == 11:
                tile = DIRT_TILE

            WIN.blit(tile, (y * TILE_SIZE, x * TILE_SIZE))

    for enemy in enemies:
        WIN.blit(enemy.sprite, enemy.cords())

    for tower in towers:
        WIN.blit(tower.sprite, tower.cords())
        # Check tower level and assign it a level tile
        if tower.level == 1:
            WIN.blit(LEVEL1_TILE, tower.cords())
        elif tower.level == 2:
            WIN.blit(LEVEL2_TILE, tower.cords())
        elif tower.level == 3:
            WIN.blit(LEVEL3_TILE, tower.cords())
        elif tower.level == 4:
            WIN.blit(LEVEL4_TILE, tower.cords())
        elif tower.level == 5:
            WIN.blit(LEVEL5_TILE, tower.cords())

    if hilite is not None:
        WIN.blit(HILITE_TILE, hilite.cords())

    for projectile in projectiles:
        WIN.blit(projectile.sprite, projectile.cords())

    # Draw Menu Buttons
    WIN.blit(UPGRADE_SPRITE, (20.5 * TILE_SIZE, 17 * TILE_SIZE))  # What the heck? User proper scale function y'all
    WIN.blit(START_SPRITE, (20.5 * TILE_SIZE, 15 * TILE_SIZE))

    pygame.display.update()


def enemy_pathfinding(enemy):
    # TODO: make dynamic pathfinding
    # Get what tile the enemy is in
    # Compare tile number
    # Rotate appropriately
    # Enemy tile number can be found by checking x vs screen width
    # Add 1/2 tile width for center, do later?
    # Screen is 825 wide, x coord is 100. Thus we should have 100/825 * num tiles then floored to find tile x
    # print("Enemy x coord:", enemy.x)
    if enemy.x_weight == -1:
        enemy_tile_x = int(floor((enemy.x + (TILE_SIZE - 2)) / WIDTH * NUM_TILES_X))
    else:
        enemy_tile_x = int(floor(enemy.x / WIDTH * NUM_TILES_X))
    enemy_tile_y = -int(floor((-enemy.y + TILE_SIZE - 2) / HEIGHT * NUM_TILES_Y))
    # print("Enemy y coord:", enemy.y)
    # print("Y:", enemy_tile_y)
    # print("Map tile:", MAP[enemy_tile_y][enemy_tile_x])
    if enemy_tile_y < 0:
        enemy.face(DOWN)
        # print("down")
        enemy.x_weight, enemy.y_weight = 0, 1
    elif enemy_tile_y >= 20 or enemy_tile_x >= 25:
        # delete_enemies.append(enemy)
        global lives
        lives = lives - 1
        #  insert remove enemy logic and live loss here
    elif MAP[enemy_tile_y][enemy_tile_x] == 9:
        enemy.face(LEFT)
        enemy.x_weight, enemy.y_weight = -1, 0
    elif MAP[enemy_tile_y][enemy_tile_x] == 10:
        enemy.face(RIGHT)
        enemy.x_weight, enemy.y_weight = 1, 0
    elif MAP[enemy_tile_y][enemy_tile_x] == 11:
        enemy.face(DOWN)
        enemy.x_weight, enemy.y_weight = 0, 1


def main():
    # TODO: enemy path finding
    player_health = 100
    player_money = 150
    main_player = Player(player_health, player_money)

    count = 1
    rounds = Rounds(to_start(), ENEMY_SIZE, ENEMY1_SPRITE)
    enemies = rounds.level()

    towers = []
    projectiles = []

    # current_tower used to know which tower to drop down (BASED ON MENU TOWER NUMBERS)
    current_tower = TOWER1_SPRITE

    upgrade_me = None  # temporary placeholder for a clicked tower (USED FOR UPGRADES)

    clock = pygame.time.Clock()
    run = True
    tower_count = 0
    start_round = False  # Changed to True when start button clicked
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

                    towers.append(Tower(f'tower_{tower_count}', 10, 3, 500, tower_rect, current_tower, "Fireball",
                                        fireball_rect, FIRE_PROJECTILE_SPRITE, ticks, 3))
                    tower_count += 1

                # Checks if click was over a tower and then proceeds with upgrading tower
                if MAP[mouse_y // scale(32)][mouse_x // scale(32)] == 3:
                    temp_x, temp_y = (mouse_x // scale(32)) * scale(32), (mouse_y // scale(32)) * scale(32)

                    # Finds which tower was clicked
                    for tower in towers:
                        if tower.cords() == (temp_x, temp_y):
                            # TODO Display an upgrade button with details of the cost of the upgrade
                            upgrade_me = tower
                            # tower.basic_upgrade(5, 5, 1)

                # Checks if upgrade button was clicked
                if TILE_SIZE * 17 <= mouse_y <= TILE_SIZE * 17 + TILE_SIZE:
                    if TILE_SIZE * 20.5 <= mouse_x <= TILE_SIZE * 20.5 + TILE_SIZE * 2:
                        if upgrade_me is not None:
                            if upgrade_me.level_up():
                                upgrade_me.basic_upgrade(5, 5, 1, 50)
                                # don't have to reset upgrade_me after upgrade
                                # upgrade_me = None

                # Checks if start button was clicked
                if TILE_SIZE * 15 <= mouse_y <= TILE_SIZE * 15 + TILE_SIZE:
                    if TILE_SIZE * 20.5 <= mouse_x <= TILE_SIZE * 20.5 + TILE_SIZE * 2:
                        print("START BT CLICKED")
                        start_round = True

                # Checks if a menu tower selection was clicked
                if MAP[mouse_y // scale(32)][mouse_x // scale(32)] > 3:
                    num = MAP[mouse_y // scale(32)][mouse_x // scale(32)]
                    if num == 4:
                        current_tower = TOWER1_SPRITE
                    elif num == 5:
                        current_tower = TOWER2_SPRITE
                    elif num == 6:
                        current_tower = TOWER3_SPRITE
                    elif num == 7:
                        current_tower = TOWER4_SPRITE
                    elif num == 8:
                        current_tower = TOWER5_SPRITE

        # TODO: might want to move to update
        # handles level ending and spawning new wave
        if Enemy.enemy_count == 0 and not start_round:
            clear(enemies, projectiles)
        if Enemy.enemy_count != 0:
            # update logic
            update(enemies, towers, rounds, projectiles, ticks, main_player)
        if Enemy.enemy_count == 0 and start_round:
            rounds.next_round()
            enemies = rounds.level()
            start_round = False
        # refresh/redraw display
        draw_window(enemies, towers, projectiles, upgrade_me)

    pygame.quit()


if __name__ == '__main__':
    main()
