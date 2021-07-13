from math import floor

import pygame
import os

from PythonDefense.enemy import Enemy
from PythonDefense.tower import Tower, get_tower_from_preset
from PythonDefense.player import Player
from PythonDefense.round import Rounds
from PythonDefense.sound import Sound
from PythonDefense.projectile import Projectile
from PythonDefense.helper_functions import scale, set_ratio, round_ratio
from PythonDefense.sprite_sets import SpriteSets
from PythonDefense.map import Map

#  nt is the os.name for windows

pygame.display.init()
display_info = pygame.display.Info()
width = display_info.current_w
height = display_info.current_h
print(height)

# Scaling pixels to fixed ratio
# adjust this to change window size
global lives_string
lives_string = "Lives: 100"
global money_string
money_string = "Money: 150"
NUM_TILES_X, NUM_TILES_Y = 25, 20

# test colors/cords for text
pygame.init()
# screen = pygame.display.set_mode((400, 400))


# We need to fit NUM_TILES_Y on screen, height will be the default limit.
MAX_HEIGHT = display_info.current_h - 70  # room for window header
MAX_PIXELS_PER_TILE = MAX_HEIGHT / NUM_TILES_Y
RATIO_TO_BE_ROUNDED = MAX_PIXELS_PER_TILE / 32  # ratio * 32 = scaled, so scaled / 32 = ratio
ratio = round_ratio(RATIO_TO_BE_ROUNDED)
set_ratio(ratio)

# if os.name != 'nt':
#     ratio = 1
# elif height > width:
#     ratio = 1.5 if height <= 1920 else 2
#     set_ratio(ratio)
# else:
#     ratio = 1.5 if width <= 1920 else 2
#     set_ratio(ratio)

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

collision_sound = Sound(os.path.join(os.path.dirname(__file__), 'assets', 'sounds', 'Trompo collido.wav'))
start_button_sound = Sound(os.path.join(os.path.dirname(__file__), 'assets', 'sounds', 'start_button.wav'))
upgrade_button_sound = Sound(os.path.join(os.path.dirname(__file__), 'assets', 'sounds', 'upgrade_button.wav'))
tower_placement_sound = Sound(os.path.join(os.path.dirname(__file__), 'assets', 'sounds', 'tower_placement.wav'))
tower_grab_sound = Sound(os.path.join(os.path.dirname(__file__), 'assets', 'sounds', 'tower_grab.wav'))
lose_life_even_sound = Sound(os.path.join(os.path.dirname(__file__), 'assets', 'sounds', 'lose_life_even.wav'))
lose_life_odd_sound = Sound(os.path.join(os.path.dirname(__file__), 'assets', 'sounds', 'lose_life_odd.wav'))

# 0 = grass
# 1 = dirt
# 2 = menu area
# 3 = grass_with_tower: just renders the grass again but reassigns the value to 3 so we know a towerHasAlreadyBeenPlaced
# 4-8 = tower icon on menu
# 9 = enemies go left
# 10 = enemies go right
# 11 = down

# MAP IS 25 ACROSS AND 25 DOWN, 5 last columns are for menu

lives = 25


# Only finds starting x cord, fine for now
# y is set to 0
def to_start(game_map):
    temp_count = 0
    y = 0
    for i in game_map.Map[0]:
        if i != 11:
            temp_count += 1
        else:
            return scale(temp_count * 32), y


def clear(enemies, projectiles):
    enemies[:] = []
    projectiles[:] = []


def update(enemies, towers, rounds, projectiles, ticks, player, sprite_sheet, game_map):
    pixel_per_frame = scale(1)

    for tower in towers:
        #  checks the towers attack speed before firing
        if tower.any_within_range(enemies) != -1:
            tower.ticks += ticks

            # If you change name closest_enemy_index then you need to update it later in fire_projectile stat declaration
            closest_enemy_index = tower.any_within_range(enemies)
            if tower.ticks >= tower.attack_speed and closest_enemy_index != -1:
                projectiles.append(tower.fire_projectile(closest_enemy_index))
                tower.ticks -= tower.attack_speed

    #   might want to optimize later on
    for projectile in projectiles:
        has_not_hit = True
        if len(enemies) != 0:
            if len(enemies) > projectile.closest:
                x, y = enemies[projectile.closest].cords()
                projectile.movement_function(projectile(), x, y)
                #  TODO: make sure only one enemy is getting hit
                for enemy in enemies:
                    if projectile.rect.colliderect(enemy.rect) and has_not_hit:
                        enemy.health -= projectile.damage
                        projectile.flag_removal()
                        collision_sound.play_sound()
                        has_not_hit = False
            else:
                projectile.flag_removal()

    # sets list equal to remaining projectiles
    projectiles[:] = [projectile for projectile in projectiles if not projectile.remove]

    for enemy in enemies:
        enemy_pathfinding(enemy, sprite_sheet, game_map)
        enemy.y += pixel_per_frame * enemy.speed * enemy.y_weight
        enemy.x += pixel_per_frame * enemy.speed * enemy.x_weight
        enemy.rect.x = enemy.x
        enemy.rect.y = enemy.y

        if enemy.check_health():
            player.add_money()
            # print('Money ' + str(player.get_money()))
            global money_string
            money_string = "Money: " + str(player.get_money())
            enemy.flag_removal()
        elif enemy.y > HEIGHT:
            if player.get_health() % 2 == 0:
                lose_life_even_sound.play_sound()
            else:
                lose_life_odd_sound.play_sound()
            player.take_damage()
            global lives_string
            lives_string = "Lives: " + str(player.get_health())
            # print('health ' + str(player.get_health()))
            enemy.flag_removal()

    # sets list equal to remaining enemies
    enemies[:] = [enemy for enemy in enemies if not enemy.remove]


def draw_window(enemies, towers, projectiles, hilite, mouse_cords, current_tower, sprite_sheet, game_map):
    # draws map
    for x, row in enumerate(game_map.Map):
        tile = sprite_sheet.GRASS_TILE
        for y, cord in enumerate(row):
            # draws grass and path
            # needs to be drawn before enemies or towers

            # Rename cord to a more fitting var name
            if cord == 0:
                tile = sprite_sheet.GRASS_TILE
            elif cord == 1:
                tile = sprite_sheet.DIRT_TILE
            elif cord == 2:
                tile = sprite_sheet.MENU_TILE
            elif cord == 3:
                tile = sprite_sheet.GRASS_TILE
            elif cord == 4:
                # menu has to be drawn under towers, since they do not take up full tile
                WIN.blit(sprite_sheet.MENU_TILE, (y * sprite_sheet.TILE_SIZE, x * sprite_sheet.TILE_SIZE))
                tile = sprite_sheet.TOWER1_SPRITE
            elif cord == 5:
                WIN.blit(sprite_sheet.MENU_TILE, (y * sprite_sheet.TILE_SIZE, x * sprite_sheet.TILE_SIZE))
                tile = sprite_sheet.TOWER2_SPRITE
            elif cord == 6:
                WIN.blit(sprite_sheet.MENU_TILE, (y * sprite_sheet.TILE_SIZE, x * sprite_sheet.TILE_SIZE))
                tile = sprite_sheet.TOWER3_SPRITE
            elif cord == 7:
                WIN.blit(sprite_sheet.MENU_TILE, (y * sprite_sheet.TILE_SIZE, x * sprite_sheet.TILE_SIZE))
                tile = sprite_sheet.TOWER4_SPRITE
            elif cord == 8:
                WIN.blit(sprite_sheet.MENU_TILE, (y * sprite_sheet.TILE_SIZE, x * sprite_sheet.TILE_SIZE))
                tile = sprite_sheet.TOWER5_SPRITE
            elif cord == 9:
                tile = sprite_sheet.DIRT_TILE
            elif cord == 10:
                tile = sprite_sheet.DIRT_TILE
            elif cord == 11:
                tile = sprite_sheet.DIRT_TILE

            WIN.blit(tile, (y * sprite_sheet.TILE_SIZE, x * sprite_sheet.TILE_SIZE))

    for enemy in enemies:
        WIN.blit(enemy.sprite, enemy.cords())

    for tower in towers:
        WIN.blit(tower.sprite, tower.cords())
        # Check tower level and assign it a level tile
        if tower.level == 1:
            WIN.blit(sprite_sheet.LEVEL1_TILE, tower.cords())
        elif tower.level == 2:
            WIN.blit(sprite_sheet.LEVEL2_TILE, tower.cords())
        elif tower.level == 3:
            WIN.blit(sprite_sheet.LEVEL3_TILE, tower.cords())
        elif tower.level == 4:
            WIN.blit(sprite_sheet.LEVEL4_TILE, tower.cords())
        elif tower.level == 5:
            WIN.blit(sprite_sheet.LEVEL5_TILE, tower.cords())

    if hilite is not None:
        WIN.blit(sprite_sheet.HILITE_TILE, hilite.cords())

    for projectile in projectiles:
        WIN.blit(projectile.sprite, projectile.cords())

    # draws current tower/selected shop tower by mouse
    if current_tower is not None:
        WIN.blit(current_tower, mouse_cords)

    # Draw Menu Buttons
    WIN.blit(sprite_sheet.UPGRADE_SPRITE, (20.5 * sprite_sheet.TILE_SIZE, 17 * sprite_sheet.TILE_SIZE))
    WIN.blit(sprite_sheet.UPGRADE_DAMAGE_SPRITE, (20.5 * sprite_sheet.TILE_SIZE, 18.5 * sprite_sheet.TILE_SIZE))
    WIN.blit(sprite_sheet.UPGRADE_RANGE_SPRITE, (22 * sprite_sheet.TILE_SIZE, 18.5 * sprite_sheet.TILE_SIZE))
    WIN.blit(sprite_sheet.UPGRADE_SPEED_SPRITE, (23.5 * sprite_sheet.TILE_SIZE, 18.5 * sprite_sheet.TILE_SIZE))
    WIN.blit(sprite_sheet.START_SPRITE, (20.5 * sprite_sheet.TILE_SIZE, 15 * sprite_sheet.TILE_SIZE))
    BLACK = (0, 0, 0)
    font = pygame.font.SysFont('Arial', int(sprite_sheet.TILE_SIZE / 2))
    global lives_string
    global money_string
    text1 = font.render(lives_string, True, BLACK)
    text2 = font.render(money_string, True, BLACK)
    WIN.blit(text1, (21 * sprite_sheet.TILE_SIZE, 1 * sprite_sheet.TILE_SIZE))
    WIN.blit(text2, (21 * sprite_sheet.TILE_SIZE, 2 * sprite_sheet.TILE_SIZE))
    pygame.display.update()


def enemy_pathfinding(enemy, sprite_sheet, game_map):
    if enemy.x_weight == -1:
        enemy_tile_x = int(floor((enemy.x + (sprite_sheet.TILE_SIZE - 2)) / WIDTH * NUM_TILES_X))
    else:
        enemy_tile_x = int(floor(enemy.x / WIDTH * NUM_TILES_X))
    enemy_tile_y = -int(floor((-enemy.y + sprite_sheet.TILE_SIZE - 2) / HEIGHT * NUM_TILES_Y))
    if enemy_tile_y < 0:
        enemy.face(DOWN)
        enemy.x_weight, enemy.y_weight = 0, 1
    elif enemy_tile_y >= 20 or enemy_tile_x >= 25:
        global lives
        lives = lives - 1  # Duplicate code? This may have been rewritten in update
        # if removed, update conditions to keep from out-of-bounds error
    elif game_map.Map[enemy_tile_y][enemy_tile_x] == 9:
        enemy.face(LEFT)
        enemy.x_weight, enemy.y_weight = -1, 0
    elif game_map.Map[enemy_tile_y][enemy_tile_x] == 10:
        enemy.face(RIGHT)
        enemy.x_weight, enemy.y_weight = 1, 0
    elif game_map.Map[enemy_tile_y][enemy_tile_x] == 11:
        enemy.face(DOWN)
        enemy.x_weight, enemy.y_weight = 0, 1


def game_loop(sprite_sheet, game_map):
    # TODO: enemy path finding
    selected_preset = None
    player_health = 10
    player_money = 50
    won = False
    # So these get properly updated instead of just on hit/change
    global lives_string
    lives_string = "Lives: " + str(player_health)
    # TODO - figure out why we can't put money string in like this cause otherwise it's bugged
    global money_string
    money_string = "Money: " + str(player_money)

    main_player = Player(player_health, player_money)

    count = 1
    rounds = Rounds(to_start(game_map), sprite_sheet.ENEMY_SIZE, sprite_sheet.ENEMY1_SPRITE, sprite_sheet.ENEMY2_SPRITE,
                    sprite_sheet.ENEMY3_SPRITE, sprite_sheet.ENEMY4_SPRITE, sprite_sheet.ENEMY5_SPRITE,sprite_sheet.ENEMY6_SPRITE)
    enemies = rounds.level()

    towers = []
    projectiles = []

    # current_tower used to know which tower to drop down (BASED ON MENU TOWER NUMBERS)
    current_tower = None  # Maybe add a highlight to the menu for this?
    has_placed = True
    selected_tower = None  # temporary placeholder for a clicked tower (USED FOR UPGRADES)
    any_highlight = False
    clock = pygame.time.Clock()
    run = True
    tower_count = 0
    start_round = False  # Changed to True when start button clicked
    while run and main_player.get_health() > 0 and not won:
        ticks = clock.tick(FPS)
        # TODO: limit possible event types
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                #  TODO: reformat
                player_money = main_player.get_money()
                if game_map.Map[mouse_y // scale(32)][mouse_x // scale(32)] == 0:
                    if player_money >= 15 and selected_preset is not None:
                        game_map.Map[mouse_y // scale(32)][mouse_x // scale(32)] = 3
                        temp_x, temp_y = (mouse_x // scale(32)) * scale(32), (mouse_y // scale(32)) * scale(32)
                        tower_rect = pygame.Rect(temp_x, temp_y, sprite_sheet.TOWER_SIZE, sprite_sheet.TOWER_SIZE)
                        projectile_rect = pygame.Rect(temp_x, temp_y, sprite_sheet.FIRE_PROJECTILE_SIZE,
                                                    sprite_sheet.FIRE_PROJECTILE_SIZE)

                        # TODO: selected tower is initialized with menu sprite/cords, this is just a temp solution
                        if not any_highlight:
                            tower_placement_sound.play_sound()
                            # print(game_map.Map)
                            new_tower = get_tower_from_preset(selected_preset, ticks, tower_rect, projectile_rect)
                            towers.append(new_tower)
                            tower_count += 1
                            main_player.money = player_money - 15
                            money_string = "Money: " + str(main_player.money)
                            has_placed = True
                            selected_preset = None
                        selected_tower = None
                        current_tower = None
                        any_highlight = False
                # Checks if click was over a tower and then proceeds with upgrading tower
                elif game_map.Map[mouse_y // scale(32)][mouse_x // scale(32)] == 3:
                    temp_x, temp_y = (mouse_x // scale(32)) * scale(32), (mouse_y // scale(32)) * scale(32)
                    current_tower = None
                    # Finds which tower was clicked
                    for tower in towers:
                        if tower.cords() == (temp_x, temp_y):
                            # TODO Display an upgrade button with details of the cost of the upgrade
                            selected_tower = tower
                            has_placed = True
                            any_highlight = True
                            # tower.basic_upgrade(5, 5, 1)
                # clears selected tower when clicking on grass/path
                elif game_map.Map[mouse_y // scale(32)][mouse_x // scale(32)] < 2 or game_map.Map[mouse_y // scale(32)][mouse_x // scale(32)] == 9 or game_map.Map[mouse_y // scale(32)][mouse_x // scale(32)] == 10 \
                        or game_map.Map[mouse_y // scale(32)][mouse_x // scale(32)] == 11:
                    current_tower = None
                    selected_tower = None
                    any_highlight = False

                # Checks if upgrade button was clicked
                if sprite_sheet.TILE_SIZE * 17 <= mouse_y <= sprite_sheet.TILE_SIZE * 17 + sprite_sheet.TILE_SIZE:
                    if sprite_sheet.TILE_SIZE * 20.5 <= mouse_x <= sprite_sheet.TILE_SIZE * 20.5 + sprite_sheet.TILE_SIZE * 2:
                        if selected_tower is not None and has_placed is not False:
                            if selected_tower.level_up():
                                if player_money >= 15:
                                    selected_tower.basic_upgrade(5, 5, 1, 50)
                                    main_player.money = player_money - 15
                                    upgrade_button_sound.play_sound()
                                    money_string = "Money: " + str(main_player.money)

                                    # don't have to reset selected_tower after upgrade
                                    # selected_tower = None
                                selected_tower = None
                                current_tower = None
                                any_highlight = False

                # Checks if start button was clicked
                if sprite_sheet.TILE_SIZE * 15 <= mouse_y <= sprite_sheet.TILE_SIZE * 15 + sprite_sheet.TILE_SIZE:
                    if sprite_sheet.TILE_SIZE * 20.5 <= mouse_x <= sprite_sheet.TILE_SIZE * 20.5 + sprite_sheet.TILE_SIZE * 2:
                        print("START BT CLICKED")
                        start_button_sound.play_sound()
                        start_round = True

                # Checks if a menu tower selection was clicked, TODO -- where to go for highlighting
                if 4 <= game_map.Map[mouse_y // scale(32)][mouse_x // scale(32)] <= 8:
                    num = game_map.Map[mouse_y // scale(32)][mouse_x // scale(32)]
                    temp_x, temp_y = (mouse_x // scale(32)) * scale(32), (mouse_y // scale(32)) * scale(32)
                    tower_rect = pygame.Rect(temp_x, temp_y, sprite_sheet.TOWER_SIZE, sprite_sheet.TOWER_SIZE)
                    fireball_rect = pygame.Rect(temp_x, temp_y, sprite_sheet.FIRE_PROJECTILE_SIZE,
                                                sprite_sheet.FIRE_PROJECTILE_SIZE)
                    if num == 4:
                        selected_preset = "python"
                        current_tower = sprite_sheet.TOWER1_SPRITE
                        tower_grab_sound.play_sound()
                        has_placed = False

                    elif num == 5:
                        selected_preset = "java"
                        current_tower = sprite_sheet.TOWER2_SPRITE
                        tower_grab_sound.play_sound()
                        has_placed = False

                    elif num == 6:
                        selected_preset = "cpp"
                        current_tower = sprite_sheet.TOWER3_SPRITE
                        tower_grab_sound.play_sound()
                        has_placed = False

                    elif num == 7:
                        selected_preset = "javascript"
                        current_tower = sprite_sheet.TOWER4_SPRITE
                        tower_grab_sound.play_sound()
                        has_placed = False

                    elif num == 8:
                        selected_preset = "lisp"
                        current_tower = sprite_sheet.TOWER5_SPRITE
                        tower_grab_sound.play_sound()
                        has_placed = False
                    any_highlight = False

        if current_tower is not None:
            mouse_cords = pygame.mouse.get_pos()
        else:
            mouse_cords = None

        # TODO: might want to move to update
        # handles level ending and spawning new wave
        if Enemy.enemy_count == 0 and not start_round:
            clear(enemies, projectiles)
        if Enemy.enemy_count != 0:
            # update logic
            update(enemies, towers, rounds, projectiles, ticks, main_player, sprite_sheet, game_map)
        if Enemy.enemy_count == 0 and start_round:
            rounds.next_round()
            enemies = rounds.level()
            start_round = False
            projectiles[:] = []
        # refresh/redraw display
        draw_window(enemies, towers, projectiles, selected_tower, mouse_cords, current_tower, sprite_sheet, game_map)
        if Enemy.enemy_count == 0 and rounds.last_round():
            won = True

    if main_player.get_health() <= 0:
        Enemy.enemy_count = 0  # Resets static var in enemy.py
        return 1

    if won:
        return 2

    else:
        pygame.quit()
        return 3


def start_menu():
    WIN.fill((25, 200, 255))
    color = (0, 0, 0)
    font = pygame.font.SysFont('Arial', scale(32))
    title_text = font.render('Python Defense', True, color)
    start_text = font.render('Click Here To Start!', True, color)
    button_rect = start_text.get_rect()
    button_rect[0] = width / 6
    button_rect[1] = height / 2.5
    run = True
    while run:
        WIN.blit(title_text, (width / 6, height / 3))
        WIN.blit(start_text, (width / 6, height / 2.5))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse):
                    return True
        pygame.display.update()
    pygame.quit()
    return False


def end_menu():
    WIN.fill((175, 238, 238))
    color = (255, 69, 0)
    font = pygame.font.SysFont('Arial', scale(32))
    end_text = font.render('Game Over', True, color)
    reset_text = font.render('Click this text to reset the game', True, color)
    button_rect = reset_text.get_rect()
    button_rect[0] = width / 6
    button_rect[1] = height / 2.5
    run = True
    while run:
        WIN.blit(reset_text, (width / 6, height / 2.5))
        WIN.blit(end_text, (width / 6, height / 3.5))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse):
                    return True
        pygame.display.update()
    pygame.quit()
    return False


def win_screen():
    WIN.fill((175, 238, 238))
    WIN.fill((236, 192, 67))
    color = (19, 63, 188)
    font = pygame.font.SysFont('Arial', scale(32))
    win_text = font.render('You win! Well played', True, color)
    reset_text = font.render('Click this text to reset the game', True, color)
    button_rect = reset_text.get_rect()
    button_rect[0] = width / 6
    button_rect[1] = height / 2.5
    run = True
    while run:
        WIN.blit(reset_text, (width / 6, height / 2.5))
        WIN.blit(win_text, (width / 6, height / 3.5))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse):
                    return True
        pygame.display.update()
    pygame.quit()
    return False


def level_screen(game_map):
    WIN.fill((108, 135, 130))
    color = (255, 255, 255)
    font = pygame.font.SysFont('Arial', scale(32))
    level_1_text = font.render('Level 1 Map', True, color)
    button_1_rect = level_1_text.get_rect()
    button_1_rect[0] = width / 6
    button_1_rect[1] = height / 3.5
    level_2_text = font.render('Level 2 Map', True, color)
    button_2_rect = level_2_text.get_rect()
    button_2_rect[0] = width / 6
    button_2_rect[1] = height / 2.5
    run = True
    while run:
        WIN.blit(level_1_text, (width / 6, height / 3.5))
        WIN.blit(level_2_text, (width / 6, height / 2.5))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if button_1_rect.collidepoint(mouse):
                    game_map.set_default_map()
                    return True
                if button_2_rect.collidepoint(mouse):
                    game_map.set_level_2_map()
                    return True
        pygame.display.update()
    pygame.quit()
    return False



def main():
    sprites = SpriteSets()
    game_map = Map()
    loop = True
    while loop:
        if start_menu():
            if level_screen(game_map):
                value = game_loop(sprites, game_map)
                if value == 1:
                    if end_menu():
                        pass
                    else:
                        loop = False
                if value == 2:
                    if win_screen():
                        pass
                    else:
                        loop = False
                if value == 3:
                    loop = False
            else:
                loop = False
        else:
            loop = False


if __name__ == '__main__':
    main()
