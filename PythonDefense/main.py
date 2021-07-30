import math
from math import floor

import pygame

from PythonDefense.enemy import Enemy
from PythonDefense.player import Player
from PythonDefense.round import Rounds
from PythonDefense.sound import Sound
from PythonDefense.helper_functions import scale, set_ratio, round_ratio
from PythonDefense.sprite_sets import SpriteSets
from PythonDefense.map import Map
from PythonDefense.soundbar import SoundBar

#  nt is the os.name for windows

pygame.display.init()
display_info = pygame.display.Info()
width = display_info.current_w
height = display_info.current_h
print(height)

# Scaling pixels to fixed ratio
# adjust this to change window size
lives_string = "Lives: 100"
money_string = "Money: 150"
round_string = "Round: "
round_number = 1
score = 0
volume = 10
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

sounds = Sound()

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
play_animation = [False, 0, False]

# text, is up here so it doesn't have to be render/converted every frame
font = pygame.font.SysFont('Arial', scale(12), bold=False)
bold_font = pygame.font.SysFont('Arial', scale(12), bold=True)
round_font = pygame.font.SysFont('Arial', scale(75), bold=True)
small_font = pygame.font.SysFont('Arial', scale(8), bold=False)

tower_sect_text = bold_font.render("Towers", True, (0, 0, 0), None).convert_alpha()
tut = [font.render('- Hover a tower for more info', True, (0, 0, 0), None).convert_alpha(),
       font.render('- Right click to deselect', True, (0, 0, 0), None).convert_alpha()]

cached_tower_stats_text = []
score_text = bold_font.render("score: " + str(score), True, (0, 0, 0), None).convert_alpha()

lives_text = bold_font.render(lives_string, True, (0, 0, 0), None).convert_alpha()
money_text = bold_font.render(money_string, True, (0, 0, 0), None).convert_alpha()
round_over_text = round_font.render("Round Over", True, (0, 0, 0), None).convert_alpha()
round_text = bold_font.render(f"{round_string} {round_number}", True, (0, 0, 0), None).convert_alpha()
sound_text = small_font.render("Volume", True, (0, 0, 0), None).convert_alpha()

num_to_tower_name = {
        4: "python",
        5: "java",
        6: "cpp",
        7: "javascript",
        8: "lisp",
    }


def re_render_round_number():
    global round_string, round_number, round_text
    round_text = bold_font.render(f"{round_string} {round_number}", True, (0, 0, 0), None).convert_alpha()


def re_render_money_and_lives():
    global lives_text, money_text
    global lives_string, money_string
    lives_text = bold_font.render(lives_string, True, (0, 0, 0), None).convert_alpha()
    money_text = bold_font.render(money_string, True, (0, 0, 0), None).convert_alpha()


def re_render_score():
    global score_text
    score_text = bold_font.render("score: " + str(score), True, (0, 0, 0), None).convert_alpha()


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

    # makes a list of on screen enemies which reduces the
    # number of times tower check for enemies.
    # TODO change how enemies are spawned
    enemies_on_screen = []
    for enemy in enemies:
        if enemy.x > 0 and enemy.y > 0:
            enemies_on_screen.append(enemy)
    for tower in towers:
        # checks the towers attack speed before firing
        tower.ticks += ticks
        if tower.ticks >= tower.attack_speed:
            tower.ticks = 0
            tower.can_shoot = True

        # only runs when tower can shoot, reduces number of calls to get_enemy and within_range
        # which is good for performance, can be optimized more if needed
        if enemies_on_screen is not None and tower.can_shoot:
            # If you change name closest_enemy_index then you need to update it later
            # in fire_projectile stat declaration
            closest_enemy = tower.get_enemy(enemies_on_screen)
            if closest_enemy is not None:  # TODO - refactor
                if tower.name == "cpp_tower":
                    if tower.cur_sprite_num == tower.sprite_count - 2:
                        tower.cur_sprite_num = tower.sprite_count - 1
                        tower.sprite = tower.sprites[tower.cur_sprite_num]
                        projectiles.append(tower.fire_projectile(closest_enemy))
                        tower.ticks = 0
                        tower.can_shoot = False
                        tower.cur_sprite_num = tower.sprite_count - 2
                        tower.sprite = tower.sprites[tower.cur_sprite_num]
                        tower.flip_frames = 4
                    else:
                        pass
                else:
                    projectiles.append(tower.fire_projectile(closest_enemy))
                    tower.cur_sprite_num = tower.sprite_count - 1
                    tower.sprite = tower.sprites[tower.cur_sprite_num]
                    tower.ticks = 0
                    tower.can_shoot = False
                    tower.flip_frames = 4
        else:
            if not tower.name == "cpp_tower":
                if tower.flip_frames > 0:
                    tower.flip_frames -= 1
                else:
                    tower.cur_sprite_num = 0
                    tower.sprite = tower.sprites[tower.cur_sprite_num]

        #   might want to optimize later on

    # Might be optimized? Hard to tell because of weird errors/unfamiliarity with concurrency. I think this is better?
    # But may want to use timeit function to test it, I'll do that soon - Benny
    for projectile in projectiles:
        if projectile.closest is not None:
            x, y = projectile.closest.cords()
            projectile.movement_function(projectile(), x, y)
            # for enemy in enemies_on_screen:
            if projectile.name == "lisp_projectile":
                for enemy in enemies_on_screen:
                    if projectile.rect.colliderect(enemy.rect):
                        enemy.health -= projectile.damage
                        projectile.flag_removal()
                        sounds.play_sound("collision_sound")
            else:
                if projectile.rect.colliderect(projectile.closest.rect):
                    if projectile.name == "javascript_projectile":
                        projectile.closest.speed *= .9
                    projectile.closest.health -= projectile.damage
                    projectile.flag_removal()
                    sounds.play_sound("collision_sound")
        else:
            projectile.flag_removal()

    for tower in towers:
        if tower.sprite_count != 0:
            if tower.name != "cpp_tower":
                tower.multiple_animations(tower.attack_speed / 100, enemies_on_screen)
            else:
                tower.multiple_animations(10, enemies_on_screen)

    # sets list equal to remaining projectiles
    projectiles[:] = [projectile for projectile in projectiles if not projectile.remove]

    for enemy in enemies:
        enemy_pathfinding(enemy, sprite_sheet, game_map)
        y_dist = pixel_per_frame * enemy.speed * enemy.y_weight
        x_dist = pixel_per_frame * enemy.speed * enemy.x_weight
        enemy.y += y_dist
        enemy.x += x_dist
        if enemy.y > 0 and enemy.x > 0:
            enemy.total_dist_traveled += abs(x_dist) + abs(y_dist)

        enemy.rect.x = enemy.x
        enemy.rect.y = enemy.y

        if enemy.check_health():
            player.add_money(enemy.value)
            # print('Money ' + str(player.get_money()))
            global money_string, score
            money_string = "Money: " + str(player.get_money())
            score += enemy.base_health
            re_render_score()
            re_render_money_and_lives()
            enemy.flag_removal()

        elif enemy.y > HEIGHT:
            if player.get_health() % 2 == 0:
                sounds.play_sound("lose_life_even_sound")
            else:
                sounds.play_sound("lose_life_odd_sound")
            player.take_damage(enemy.health)
            global lives_string
            lives_string = "Lives: " + str(int(math.floor(player.get_health())))
            re_render_money_and_lives()
            # print('health ' + str(player.get_health()))
            enemy.flag_removal()

    # sets list equal to remaining enemies
    enemies[:] = [enemy for enemy in enemies if not enemy.remove]


# async def projectile_movement(projectile):
#     if projectile.closest is not None:
#         x, y = projectile.closest.cords()
#         projectile.movement_function(projectile(), x, y)
#         if projectile.rect.colliderect(projectile.closest.rect):
#             projectile.closest.health -= projectile.damage
#             projectile.flag_removal()
#             sounds.play_sound("collision_sound")
#     else:
#         projectile.flag_removal()
# this can be modified for aoe projectiles
# for enemy in enemies:
#     if projectile.rect.colliderect(enemy.rect) and has_not_hit:
#         enemy.health -= projectile.damage
#         projectile.flag_removal()
#         collision_sound.play_sound()
#         has_not_hit = False
#
#
# async def all_projectile_movement(projectiles, enemies):
#     tasks = []
#     for projectile in projectiles:
#         tasks.append(projectile_movement(projectile, enemies))
#         try:
#             await asyncio.gather(*tasks)
#         except RuntimeError:  # This seems like a bad solution, look for other ways of concurrency here
#             pass


def draw_window(enemies, towers, projectiles, selected_tower, mouse_cords, current_tower_info, sprite_sheet,
                game_map, hovered_tower_info, sound_bar, start_round, fps, hovered_button=None, money=None):
    # checks tile mouse cords are on and if its a shop tower, set it to be highlighted
    hovered_tile = get_tile(mouse_cords, game_map)
    tiles_to_hover = [4, 5, 6, 7, 8]
    show_hover_effect = False
    if hovered_tile in tiles_to_hover:
        show_hover_effect = True

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
                # do nothing, this is blit in the tower loop. Easy way to get java tower working
                pass
            elif cord == 4:
                # menu has to be drawn under towers, since they do not take up full tile
                WIN.blit(sprite_sheet.MENU_TILE, (y * sprite_sheet.TILE_SIZE, x * sprite_sheet.TILE_SIZE))
                tile = sprite_sheet.PYTHON_TOWER_SPRITE
            elif cord == 5:
                WIN.blit(sprite_sheet.MENU_TILE, (y * sprite_sheet.TILE_SIZE, x * sprite_sheet.TILE_SIZE))
                tile = sprite_sheet.JAVA_TOWER_SPRITE
            elif cord == 6:
                WIN.blit(sprite_sheet.MENU_TILE, (y * sprite_sheet.TILE_SIZE, x * sprite_sheet.TILE_SIZE))
                tile = sprite_sheet.CPP_TOWER_SPRITE
            elif cord == 7:
                WIN.blit(sprite_sheet.MENU_TILE, (y * sprite_sheet.TILE_SIZE, x * sprite_sheet.TILE_SIZE))
                tile = sprite_sheet.JAVASCRIPT_TOWER_SPRITE
            elif cord == 8:
                WIN.blit(sprite_sheet.MENU_TILE, (y * sprite_sheet.TILE_SIZE, x * sprite_sheet.TILE_SIZE))
                tile = sprite_sheet.LISP_TOWER_SPRITE
            elif cord == 9:
                tile = sprite_sheet.DIRT_TILE
            elif cord == 10:
                tile = sprite_sheet.DIRT_TILE
            elif cord == 11:
                tile = sprite_sheet.DIRT_TILE
            elif cord == 13:
                tile = sprite_sheet.WATER_TILE

            if cord in tiles_to_hover:
                WIN.blit(sprite_sheet.BACKGROUND_TOWER_TILE, (y * sprite_sheet.TILE_SIZE, x * sprite_sheet.TILE_SIZE))
                WIN.blit(sprite_sheet.BORDER_TILE, (y * sprite_sheet.TILE_SIZE + scale(1), x * sprite_sheet.TILE_SIZE + scale(1)))

            WIN.blit(tile, (y * sprite_sheet.TILE_SIZE, x * sprite_sheet.TILE_SIZE))

            # hover highlight on shop towers
            if cord == hovered_tile and show_hover_effect:
                WIN.blit(sprite_sheet.HILITE_TILE, (y * sprite_sheet.TILE_SIZE, x * sprite_sheet.TILE_SIZE))

            if cord in tiles_to_hover and money is not None:
                if money < tower_presets[num_to_tower_name[cord]][9]:
                    WIN.blit(sprite_sheet.RED_TILE, (y * sprite_sheet.TILE_SIZE, x * sprite_sheet.TILE_SIZE))

    for enemy in enemies:
        WIN.blit(enemy.sprite, enemy.cords())

    for tower in towers:
        if tower.on_water:
            WIN.blit(sprite_sheet.WATER_TILE, tower.cords())
        else:
            WIN.blit(sprite_sheet.GRASS_TILE, tower.cords())
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

    # highlight and show range for selected tower
    if selected_tower is not None:
        WIN.blit(sprite_sheet.HILITE_TILE, selected_tower.cords())
        draw_range_indicator(selected_tower.range, selected_tower.cords(), selected_tower)

    for projectile in projectiles:
        WIN.blit(projectile.sprite, projectile.cords())

    # draw highlight for menu buttons
    if hovered_button is not None:
        if hovered_button == 1:
            WIN.blit(sprite_sheet.SMALL_HIGHLIGHT, (20.5 * sprite_sheet.TILE_SIZE - scale(3), 11.5 * sprite_sheet.TILE_SIZE - scale(3)))
        elif hovered_button == 2:
            WIN.blit(sprite_sheet.SMALL_HIGHLIGHT, (20.5 * sprite_sheet.TILE_SIZE - scale(3), 13 * sprite_sheet.TILE_SIZE - scale(3)))
        elif hovered_button == 3:
            WIN.blit(sprite_sheet.SMALL_HIGHLIGHT, (20.5 * sprite_sheet.TILE_SIZE - scale(3), 14.5 * sprite_sheet.TILE_SIZE - scale(3)))
        elif hovered_button == 4:
            WIN.blit(sprite_sheet.LARGE_HIGHLIGHT, (20.5 * sprite_sheet.TILE_SIZE - scale(3), 16 * sprite_sheet.TILE_SIZE - scale(3)))
        elif hovered_button == 5:
            WIN.blit(sprite_sheet.LARGE_HIGHLIGHT, (20.5 * sprite_sheet.TILE_SIZE - scale(3), 17.5 * sprite_sheet.TILE_SIZE - scale(3)))
        elif hovered_button == 6:
            WIN.blit(sprite_sheet.SOUND_BAR_HIGHLIGHT, (20.5 * sprite_sheet.TILE_SIZE - scale(3), 19 * sprite_sheet.TILE_SIZE - scale(3)))

    # Draw Menu Buttons
    WIN.blit(sprite_sheet.UPGRADE_DAMAGE_SPRITE, (20.5 * sprite_sheet.TILE_SIZE, 11.5 * sprite_sheet.TILE_SIZE))
    WIN.blit(sprite_sheet.UPGRADE_SPEED_SPRITE, (20.5 * sprite_sheet.TILE_SIZE, 13 * sprite_sheet.TILE_SIZE))
    WIN.blit(sprite_sheet.UPGRADE_RANGE_SPRITE, (20.5 * sprite_sheet.TILE_SIZE, 14.5 * sprite_sheet.TILE_SIZE))
    WIN.blit(sprite_sheet.UPGRADE_SPRITE, (20.5 * sprite_sheet.TILE_SIZE, 16 * sprite_sheet.TILE_SIZE))
    WIN.blit(sprite_sheet.START_SPRITE, (20.5 * sprite_sheet.TILE_SIZE, 17.5 * sprite_sheet.TILE_SIZE))
    WIN.blit(sound_bar.my_sprite(), (20.5 * sprite_sheet.TILE_SIZE, 19 * sprite_sheet.TILE_SIZE))

    # red tile on upgrade buttons
    if selected_tower is not None and money is not None:
        if money < selected_tower.cost * 1.5:
            WIN.blit(sprite_sheet.LARGE_RED_TILE, (20.5 * sprite_sheet.TILE_SIZE, 16 * sprite_sheet.TILE_SIZE))
        if money < selected_tower.cost * .5:
            WIN.blit(sprite_sheet.RED_TILE, (20.5 * sprite_sheet.TILE_SIZE, 11.5 * sprite_sheet.TILE_SIZE))
            WIN.blit(sprite_sheet.RED_TILE, (20.5 * sprite_sheet.TILE_SIZE, 13 * sprite_sheet.TILE_SIZE))
            WIN.blit(sprite_sheet.RED_TILE, (20.5 * sprite_sheet.TILE_SIZE, 14.5 * sprite_sheet.TILE_SIZE))

    if selected_tower is not None:
        if selected_tower.attr_levels_dict["damage"] == 5:
            WIN.blit(sprite_sheet.GRAY_TILE, (20.5 * sprite_sheet.TILE_SIZE, 11.5 * sprite_sheet.TILE_SIZE))
        if selected_tower.attr_levels_dict["attack_speed"] == 5:
            WIN.blit(sprite_sheet.GRAY_TILE, (20.5 * sprite_sheet.TILE_SIZE, 13 * sprite_sheet.TILE_SIZE))
        if selected_tower.attr_levels_dict["range"] == 5:
            WIN.blit(sprite_sheet.GRAY_TILE, (20.5 * sprite_sheet.TILE_SIZE, 14.5 * sprite_sheet.TILE_SIZE))
        if selected_tower.level == 5:
            WIN.blit(sprite_sheet.LARGE_GRAY_TILE, (20.5 * sprite_sheet.TILE_SIZE, 16 * sprite_sheet.TILE_SIZE))

    # start sprite gray out
    if start_round is True:
        WIN.blit(sprite_sheet.LARGE_GRAY_TILE, (20.5 * sprite_sheet.TILE_SIZE, 17.5 * sprite_sheet.TILE_SIZE))

    # draw text
    WIN.blit(round_text, (21 * sprite_sheet.TILE_SIZE, 1 * sprite_sheet.TILE_SIZE - scale(13)))
    WIN.blit(lives_text, (21 * sprite_sheet.TILE_SIZE, 1 * sprite_sheet.TILE_SIZE))
    WIN.blit(money_text, (21 * sprite_sheet.TILE_SIZE, 1 * sprite_sheet.TILE_SIZE + scale(13)))
    WIN.blit(score_text, (21 * sprite_sheet.TILE_SIZE, 1 * sprite_sheet.TILE_SIZE + scale(26)))
    WIN.blit(tower_sect_text, (22 * sprite_sheet.TILE_SIZE, 2 * sprite_sheet.TILE_SIZE + scale(13)))
    WIN.blit(sound_text, (21 * sprite_sheet.TILE_SIZE + scale(35), 19 * sprite_sheet.TILE_SIZE + scale(3.5)))

    # upgrade hover
    if selected_tower is not None:
        draw_upgrade_bar(sprite_sheet, 11.5, selected_tower.attr_levels_dict['damage'], selected_tower.level)
        draw_upgrade_bar(sprite_sheet, 13, selected_tower.attr_levels_dict['attack_speed'], selected_tower.level)
        draw_upgrade_bar(sprite_sheet, 14.5, selected_tower.attr_levels_dict['range'], selected_tower.level)
    else:
        draw_upgrade_bar(sprite_sheet, 11.5, 0, 0)
        draw_upgrade_bar(sprite_sheet, 13, 0, 0)
        draw_upgrade_bar(sprite_sheet, 14.5, 0, 0)

    # shop text box
    if selected_tower is not None:
        display_stats(selected_tower)
    else:
        if hovered_tower_info is None:
            display_tutorial()
            cached_tower_stats_text[:] = []
        else:
            display_shop_tower_info(hovered_tower_info)

    # draws current tower/selected shop tower on mouse with range indicator
    if current_tower_info is not None:
        x, y = mouse_cords
        x, y = x - scale(16), y - scale(16)
        WIN.blit(current_tower_info[0], (x, y))
        tower_range = current_tower_info[1]
        draw_range_indicator(tower_range, (x, y), None, current_tower_info[2])

    # handle playing the round over animation
    global play_animation
    if Enemy.enemy_count == 0 and start_round is False and play_animation[2] is True:
        play_animation[0] = True
    if play_animation[0] is True:
        round_over_text.set_alpha(play_animation[1])
        WIN.blit(round_over_text, (scale(100), scale(250)))
        if play_animation[1] > 255:
            play_animation = [False, 0, False]
        else:
            play_animation[1] += 3

    # FPS Counter, doesn't need convert since it changes every frame anyways
    fps_text = bold_font.render("FPS: " + str(fps)[:4], True, (0, 0, 0), None)
    WIN.blit(fps_text, (scale(10), scale(10)))

    pygame.display.update()


def draw_upgrade_bar(sprite_sheet, y_offset, small_level, big_level):
    for x in range(5):
        WIN.blit(sprite_sheet.SMALL_UPGRADE_LEVEL, (20.5 * sprite_sheet.TILE_SIZE + scale(40) + scale(18) * x, y_offset * sprite_sheet.TILE_SIZE + sprite_sheet.TILE_SIZE // 3.5))
    for x in range(5):
        if x < small_level and x < big_level:
            WIN.blit(sprite_sheet.SMALL_UPGRADE_LEVEL_FILLED, (20.5 * sprite_sheet.TILE_SIZE + scale(42.5) + scale(18) * x, y_offset * sprite_sheet.TILE_SIZE + scale(2.5) + sprite_sheet.TILE_SIZE // 3.5))
            WIN.blit(sprite_sheet.SMALL_UPGRADE_LEVEL_TILTED, (20.5 * sprite_sheet.TILE_SIZE + scale(42.5) + scale(18) * x, y_offset * sprite_sheet.TILE_SIZE + scale(2.5) + sprite_sheet.TILE_SIZE // 3.5))
        elif x < small_level:
            WIN.blit(sprite_sheet.SMALL_UPGRADE_LEVEL_FILLED, (20.5 * sprite_sheet.TILE_SIZE + scale(42.5) + scale(18) * x, y_offset * sprite_sheet.TILE_SIZE + scale(2.5) + sprite_sheet.TILE_SIZE // 3.5))
        elif x < big_level:
            WIN.blit(sprite_sheet.SMALL_UPGRADE_LEVEL_FILLED_ALT, (20.5 * sprite_sheet.TILE_SIZE + scale(42.5) + scale(18) * x, y_offset * sprite_sheet.TILE_SIZE + scale(2.5) + sprite_sheet.TILE_SIZE // 3.5))
        else:
            WIN.blit(sprite_sheet.SMALL_UPGRADE_LEVEL_EMPTY, (20.5 * sprite_sheet.TILE_SIZE + scale(42.5) + scale(18) * x, y_offset * sprite_sheet.TILE_SIZE + scale(2.5) + sprite_sheet.TILE_SIZE // 3.5))

def draw_transparent_rect():
    # if surf is none it caches the surface. Avoids calling convert alpha every frame
    surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA).convert_alpha()
    radius_indicator_color = pygame.Color(0, 0, 0, 60)
    pygame.draw.rect(surf, radius_indicator_color, (0, 0, WIDTH, HEIGHT))
    WIN.blit(surf, (0, 0))


def draw_window_transparent(enemies, towers, projectiles, selected_tower, mouse_cords, current_tower_info, sprite_sheet,
                            game_map, hovered_tower_info, sound_bar, start_round, fps):
    draw_window(enemies, towers, projectiles, selected_tower, mouse_cords, current_tower_info, sprite_sheet,
                game_map, hovered_tower_info, sound_bar, start_round, fps)

    draw_transparent_rect()

    pygame.display.update()


def reset_cpp(towers):
    for tower in towers:
        if tower.name == "cpp_tower":
            tower.cur_sprite_num = 0
            tower.sprite = tower.sprites[tower.cur_sprite_num]


def draw_range_indicator(tower_range, cords, tower=None, temp_surf=None):
    if tower is not None:
        # if surf is none it caches the surface. Avoids calling convert alpha every frame
        if tower.range_surf is None:
            surf = pygame.Surface((tower_range * 2, tower_range * 2), pygame.SRCALPHA).convert_alpha()
            radius_indicator_color = pygame.Color(0, 0, 0, 70)
            pygame.draw.circle(surf, radius_indicator_color, (tower_range, tower_range),
                               tower_range)
            tower.range_surf = surf
        else:
            surf = tower.range_surf
    else:
        surf = temp_surf
    # centers circle on tower
    x, y = cords
    shifted_x = x - tower_range + scale(16)
    shifted_y = y - tower_range + scale(16)
    WIN.blit(surf, (shifted_x, shifted_y))


# pygame doesn't have word wrap and can't use newline characters, so each line in put in manually :)
def display_shop_tower_info(current_tower_info):
    for i, text in enumerate(current_tower_info):
        WIN.blit(text, (21 * TILE_SIZE - scale(12), 9 * TILE_SIZE + i * scale(13)))


# pygame doesn't have word wrap and can't use newline characters, so each line must be put in manually :^)
def display_tutorial():
    for i, text in enumerate(tut):
        WIN.blit(text, (21 * TILE_SIZE - scale(20), 9 * TILE_SIZE + i * scale(13)))


# pygame doesn't have word wrap and can't use newline characters, so each line must be put in manually :^C
# TODO: add upgrade level
def display_stats(selected_tower):
    if not cached_tower_stats_text:
        att_damage = font.render('Attack damage: ' + str(selected_tower.damage)[:4], False, (0, 0, 0)).convert()
        att_speed = font.render('Attack speed: ' + str(1000 / selected_tower.attack_speed)[:4], False,
                                (0, 0, 0)).convert()
        att_range = font.render('Attack range: ' + str(selected_tower.range)[:5], False, (0, 0, 0)).convert()
        minor_upgrade = font.render('Minor upgrade: ' + str(selected_tower.cost * .5)[:4], False, (0, 0, 0)).convert()
        major_upgrade = font.render('Major upgrade: ' + str(selected_tower.cost * 1.5)[:4], False, (0, 0, 0)).convert()
        cached_tower_stats_text.append(att_damage)
        cached_tower_stats_text.append(att_speed)
        cached_tower_stats_text.append(att_range)
        cached_tower_stats_text.append(minor_upgrade)
        cached_tower_stats_text.append(major_upgrade)

    for i, text in enumerate(cached_tower_stats_text):
        WIN.blit(text, (21 * TILE_SIZE - scale(12), 9 * TILE_SIZE + i * scale(13)))


def get_tile(mouse_cords, game_map):
    return game_map.Map[mouse_cords[1] // scale(32)][mouse_cords[0] // scale(32)]


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
        re_render_money_and_lives()
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
    global volume
    sound_bar = SoundBar(sprite_sheet, volume)
    selected_preset = None
    player_health = 20
    player_money = 60
    # So these get properly updated instead of just on hit/change
    global lives_string, money_string, score
    score = 0
    re_render_score()
    lives_string = "Lives: " + str(int(math.floor(player_health)))
    # TODO - figure out why we can't put money string in like this cause otherwise it's bugged
    money_string = "Money: " + str(player_money)
    re_render_money_and_lives()

    main_player = Player(player_health, player_money)

    count = 1
    rounds = Rounds(to_start(game_map), sprite_sheet.ENEMY_SIZE, sprite_sheet.ENEMY1_SPRITE, sprite_sheet.ENEMY2_SPRITE,
                    sprite_sheet.ENEMY3_SPRITE, sprite_sheet.ENEMY4_SPRITE, sprite_sheet.ENEMY5_SPRITE,
                    sprite_sheet.ENEMY6_SPRITE)
    enemies = rounds.level()

    towers = []
    projectiles = []
    shop_towers = {4: "python", 5: "java", 6: "cpp", 7: "javascript", 8: "lisp"}

    # current_tower_info used to know which tower to drop down (BASED ON MENU TOWER NUMBERS)
    current_tower_info = None  # Maybe add a highlight to the menu for this?
    has_placed = True
    selected_tower = None  # temporary placeholder for a clicked tower (USED FOR UPGRADES)
    any_highlight = False
    skip_round = False
    clock = pygame.time.Clock()
    run = True
    tower_count = 0
    global play_animation
    play_animation = [False, 0, False]
    start_round = False  # Changed to True when start button clicked
    while run and main_player.get_health() > 0:
        ticks = clock.tick(FPS)
        mouse_cords = pygame.mouse.get_pos()
        hovered_tower = None
        hovered_button = None
        # TODO: limit possible event types
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print(get_tile(mouse_cords, game_map))
                #  TODO: reformat
                player_money = main_player.get_money()
                selected_tile = get_tile(mouse_cords, game_map)
                tile_cord = game_map.Map[mouse_y // scale(32)][mouse_x // scale(32)]
                if (selected_tile == 0 or (selected_tile == 13 and selected_preset == "java")) and \
                        selected_preset is not None:
                    # moved selected preset to ^^ condition from vv condition to allow for deselection on grass
                    if player_money >= tower_presets[selected_preset][9]:
                        game_map.Map[mouse_y // scale(32)][mouse_x // scale(32)] = 3
                        temp_x, temp_y = (mouse_x // scale(32)) * scale(32), (mouse_y // scale(32)) * scale(32)
                        tower_rect = pygame.Rect(temp_x, temp_y, sprite_sheet.TOWER_SIZE, sprite_sheet.TOWER_SIZE)
                        projectile_rect = pygame.Rect(temp_x, temp_y, sprite_sheet.FIRE_PROJECTILE_SIZE,
                                                      sprite_sheet.FIRE_PROJECTILE_SIZE)
                        # places tower from preset
                        if not any_highlight:
                            sounds.play_sound("tower_placement_sound")
                            # print(game_map.Map)
                            on_water = False
                            if selected_tile == 13:
                                on_water = True
                            new_tower = get_tower_from_preset(selected_preset, ticks, tower_rect, projectile_rect,
                                                              on_water)
                            towers.append(new_tower)
                            tower_count += 1
                            main_player.money = player_money - new_tower.cost
                            money_string = "Money: " + str(main_player.money)
                            re_render_money_and_lives()
                            has_placed = True
                            selected_preset = None
                            selected_tower = new_tower
                            current_tower_info = None
                            any_highlight = True

                    selected_preset = None
                    current_tower_info = None

                    # added so that the tower would be removed upon not having enough money to place
                # Checks if click was over a tower and then proceeds with upgrading tower
                elif game_map.Map[mouse_y // scale(32)][mouse_x // scale(32)] == 3:
                    temp_x, temp_y = (mouse_x // scale(32)) * scale(32), (mouse_y // scale(32)) * scale(32)
                    current_tower_info = None
                    # Finds which tower was clicked
                    for tower in towers:
                        if tower.cords() == (temp_x, temp_y):
                            # TODO Display an upgrade button with details of the cost of the upgrade
                            selected_tower = tower
                            has_placed = True
                            any_highlight = True
                            cached_tower_stats_text[:] = []
                            # tower.basic_upgrade(5, 5, 1)
                # clears selected tower when clicking on grass/path
                elif 0 <= game_map.Map[mouse_y // scale(32)][mouse_x // scale(32)] < 2 or 9 <= \
                        game_map.Map[mouse_y // scale(32)][mouse_x // scale(32)] <= \
                        11:
                    # should occur on 0,1,9,10,11, TODO: Fix not deselecting on grass 0
                    current_tower_info = None
                    selected_tower = None
                    any_highlight = False

                elif sprite_sheet.TILE_SIZE * 19 <= mouse_y <= sprite_sheet.TILE_SIZE * 19 + sprite_sheet.TILE_SIZE//2:
                    if sprite_sheet.TILE_SIZE * 20.5 <= mouse_x <= sprite_sheet.TILE_SIZE * 20.5 + sprite_sheet.\
                            TILE_SIZE * 4:
                        sound_bar.user_click(mouse_x, mouse_y, sprite_sheet, sounds)
                        numerator = mouse_x - sprite_sheet.TILE_SIZE * 20.5
                        index = ((numerator / (sprite_sheet.TILE_SIZE * 4)) * 20)
                        if index <= .4:
                            index = math.floor(index)
                        else:
                            index = math.ceil(index)
                        volume = int(index)

                # MAJOR TODO: CHANGE ALL THESE IF's TO ELIFS for PREFORMANce
                # Checks if upgrade button was clicked
                elif sprite_sheet.TILE_SIZE * 16 <= mouse_y <= sprite_sheet.TILE_SIZE * 16 + sprite_sheet.TILE_SIZE:
                    if sprite_sheet.TILE_SIZE * 20.5 <= mouse_x <= sprite_sheet.TILE_SIZE * 20.5 + sprite_sheet.TILE_SIZE * 4:
                        if selected_tower is not None and has_placed is not False:
                            if selected_tower.level_up():
                                if player_money >= selected_tower.cost * 1.5:
                                    selected_tower.basic_upgrade()
                                    main_player.money = player_money - selected_tower.cost * 1.5
                                    sounds.play_sound("upgrade_button_sound")
                                    money_string = "Money: " + str(main_player.money)

                                    # this updates the money text and selected tower stats text, helps with optimization
                                    re_render_money_and_lives()
                                    cached_tower_stats_text[:] = []

                                    # don't have to reset selected_tower after upgrade
                                    selected_tower = selected_tower
                                    current_tower_info = None
                                    any_highlight = True

                # Checks if small upgrade buttons were clicked
                elif sprite_sheet.TILE_SIZE * 20.5 <= mouse_x <= sprite_sheet.TILE_SIZE * 20.5 + sprite_sheet.TILE_SIZE and sprite_sheet.TILE_SIZE * 11.5 <= mouse_y <= sprite_sheet.TILE_SIZE * 14.5 + sprite_sheet.TILE_SIZE:
                    upgrade_complete = False
                    if selected_tower is not None and has_placed is not False:
                        if player_money >= selected_tower.cost * .5:
                            if sprite_sheet.TILE_SIZE * 11.5 <= mouse_y <= sprite_sheet.TILE_SIZE * 11.5 + sprite_sheet.TILE_SIZE:
                                if selected_tower.check_attr_dict('damage'):
                                    selected_tower.upgrade_damage()
                                    sounds.play_sound("upgrade_button_sound")
                                    upgrade_complete = True

                            elif sprite_sheet.TILE_SIZE * 13 <= mouse_y <= sprite_sheet.TILE_SIZE * 13 + sprite_sheet.TILE_SIZE:
                                if selected_tower.check_attr_dict('attack_speed'):
                                    selected_tower.upgrade_attack_speed()
                                    sounds.play_sound("upgrade_button_sound")
                                    upgrade_complete = True

                            elif sprite_sheet.TILE_SIZE * 14.5 <= mouse_y <= sprite_sheet.TILE_SIZE * 14.5 + sprite_sheet.TILE_SIZE:
                                if selected_tower.check_attr_dict('range'):
                                    selected_tower.upgrade_range()
                                    sounds.play_sound("upgrade_button_sound")
                                    upgrade_complete = True

                            if upgrade_complete:
                                main_player.money = player_money - selected_tower.cost * .5
                                sounds.play_sound("collision_sound")
                                money_string = "Money: " + str(main_player.money)

                                # this updates the money text and selected tower stats text, helps with optimization
                                re_render_money_and_lives()
                                cached_tower_stats_text[:] = []

                                # don't have to reset selected_tower after upgrade

                                selected_tower = selected_tower
                                current_tower_info = None
                                any_highlight = True

                # Checks if start button was clicked
                elif sprite_sheet.TILE_SIZE * 17.5 <= mouse_y <= sprite_sheet.TILE_SIZE * 17.5 + sprite_sheet.TILE_SIZE:
                    if sprite_sheet.TILE_SIZE * 20.5 <= mouse_x <= sprite_sheet.TILE_SIZE * 20.5 + sprite_sheet.TILE_SIZE * 4:
                        print("START BT CLICKED")
                        sounds.play_sound("start_button_sound")
                        start_round = True
                        # used to not show round over on start
                        play_animation[2] = True

                # Checks if a menu tower selection was clicked, TODO -- where to go for highlighting
                elif 4 <= tile_cord <= 8 and player_money >= tower_presets[num_to_tower_name[tile_cord]][9]:
                    num = tile_cord
                    if num == 4:
                        selected_preset = "python"
                        current_tower_info = [sprite_sheet.PYTHON_TOWER_SPRITE, tower_presets[selected_preset][3]]
                    elif num == 5:
                        selected_preset = "java"
                        current_tower_info = [sprite_sheet.JAVA_TOWER_SPRITE, tower_presets[selected_preset][3]]
                    elif num == 6:
                        selected_preset = "cpp"
                        current_tower_info = [sprite_sheet.CPP_TOWER_SPRITE, tower_presets[selected_preset][3]]
                    elif num == 7:
                        selected_preset = "javascript"
                        current_tower_info = [sprite_sheet.JAVASCRIPT_TOWER_SPRITE, tower_presets[selected_preset][3]]
                    elif num == 8:
                        selected_preset = "lisp"
                        current_tower_info = [sprite_sheet.LISP_TOWER_SPRITE, tower_presets[selected_preset][3]]

                    if selected_preset is not None:
                        sounds.play_sound("tower_grab_sound")
                        has_placed = False
                        tower_range = tower_presets[selected_preset][3]
                        # TODO: cache the surf
                        surf = pygame.Surface((tower_range * 2, tower_range * 2), pygame.SRCALPHA).convert_alpha()
                        radius_indicator_color = pygame.Color(0, 0, 0, 70)
                        pygame.draw.circle(surf, radius_indicator_color, (tower_range, tower_range), tower_range)
                        current_tower_info.append(surf)

                        # adds every line of text to current tower info
                        text_box = []
                        for i, _ in enumerate(tower_presets[selected_preset]):
                            if i > 9:
                                text_box.append(tower_presets[selected_preset][i])
                        current_tower_info.append(text_box)

                    any_highlight = False
                    selected_tower = None
            # right click deselects towers and tower placement indicator
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                selected_tower = None
                selected_preset = None
                current_tower_info = None

        if get_tile(mouse_cords, game_map) in shop_towers.keys():
            temp = shop_towers[get_tile(mouse_cords, game_map)]
            text_box = []
            for i, _ in enumerate(tower_presets[temp]):
                if i > 9:
                    text_box.append(tower_presets[temp][i])
            hovered_tower = text_box

        # hover effect for menu buttons, not towers though
        mouse_x, mouse_y = mouse_cords
        if sprite_sheet.TILE_SIZE * 20.5 <= mouse_x <= sprite_sheet.TILE_SIZE * 20.5 + sprite_sheet.TILE_SIZE and sprite_sheet.TILE_SIZE * 11.5 <= mouse_y <= sprite_sheet.TILE_SIZE * 14.5 + sprite_sheet.TILE_SIZE:
            if sprite_sheet.TILE_SIZE * 11.5 <= mouse_y <= sprite_sheet.TILE_SIZE * 11.5 + sprite_sheet.TILE_SIZE:
                hovered_button = 1
            elif sprite_sheet.TILE_SIZE * 13 <= mouse_y <= sprite_sheet.TILE_SIZE * 13 + sprite_sheet.TILE_SIZE:
                hovered_button = 2
            elif sprite_sheet.TILE_SIZE * 14.5 <= mouse_y <= sprite_sheet.TILE_SIZE * 14.5 + sprite_sheet.TILE_SIZE:
                hovered_button = 3
        elif sprite_sheet.TILE_SIZE * 16 <= mouse_y <= sprite_sheet.TILE_SIZE * 16 + sprite_sheet.TILE_SIZE:
            if sprite_sheet.TILE_SIZE * 20.5 <= mouse_x <= sprite_sheet.TILE_SIZE * 20.5 + sprite_sheet.TILE_SIZE * 4:
                hovered_button = 4
        elif sprite_sheet.TILE_SIZE * 17.5 <= mouse_y <= sprite_sheet.TILE_SIZE * 17.5 + sprite_sheet.TILE_SIZE:
            if sprite_sheet.TILE_SIZE * 20.5 <= mouse_x <= sprite_sheet.TILE_SIZE * 20.5 + sprite_sheet.TILE_SIZE * 4:
                hovered_button = 5
        elif sprite_sheet.TILE_SIZE * 19 <= mouse_y <= sprite_sheet.TILE_SIZE * 19 + sprite_sheet.TILE_SIZE // 2:
            if sprite_sheet.TILE_SIZE * 20.5 <= mouse_x <= sprite_sheet.TILE_SIZE * 20.5 + sprite_sheet.TILE_SIZE * 4:
                hovered_button = 6
        # TODO: might want to move to update
        # handles level ending and spawning new wave

        if Enemy.enemy_count == 0 and not start_round:
            clear(enemies, projectiles)
        if Enemy.enemy_count != 0:
            # update logic
            update(enemies, towers, rounds, projectiles, ticks, main_player, sprite_sheet, game_map)
        if Enemy.enemy_count == 0 and rounds.last_round():
            start_round = False
            play_animation = [False, 0, False]
            _continue = win_screen([enemies, towers, projectiles, selected_tower, mouse_cords, current_tower_info, sprite_sheet,
                        game_map, hovered_tower, sound_bar, start_round, clock.get_fps()])
            if _continue == 2: #TODO - WARNING - don't change these
                return 2
            if _continue == 3: #TODO - WARNING - don't change these
                return 3
            if _continue == 1:
                rounds.next_round()
                skip_round = True
            if not _continue:
                return False
        if Enemy.enemy_count == 0 and start_round:
            rounds.next_round()
            if skip_round:
                rounds.round -= 1
                skip_round = False
            reset_cpp(towers)

            # updates the round number
            global round_number
            round_number = rounds.round
            re_render_round_number()

            enemies = rounds.level()
            start_round = False
            projectiles[:] = []
        # refresh/redraw display
        draw_window(enemies, towers, projectiles, selected_tower, mouse_cords, current_tower_info, sprite_sheet,
                    game_map, hovered_tower, sound_bar, start_round, clock.get_fps(), hovered_button, main_player.get_money())

    if main_player.get_health() <= 0:
        play_animation = [False, 0, False]
        Enemy.enemy_count = 0  # Resets static var in enemy.py
        return [1, [enemies, towers, projectiles, selected_tower, mouse_cords, current_tower_info, sprite_sheet,
                    game_map, hovered_tower, sound_bar, start_round, clock.get_fps()]]

    else:
        play_animation = [False, 0, False]
        pygame.quit()
        return 3


def start_menu(sprite_sheet, game_map):
    player_health = 10000
    player_money = 100000
    won = False
    # So these get properly updated instead of just on hit/change
    global lives_string, money_string
    lives_string = "Lives: " + str(int(math.floor(player_health)))
    # TODO - figure out why we can't put money string in like this cause otherwise it's bugged
    money_string = "Money: " + str(player_money)
    re_render_money_and_lives()

    if game_map.name == "default":
        game_map.set_default_map()
    if game_map.name == "level_2":
        game_map.set_level_2_map()
    sound_bar = SoundBar(sprite_sheet, volume)
    draw_window_transparent([], [], [], None, pygame.mouse.get_pos(), None, sprite_sheet, game_map, None, sound_bar,
                            False, FPS)


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
                    sounds.play_sound("menu_sound")
                    sounds.play_sound("tower_placement_sound")
                    return True
        pygame.display.update()
    pygame.quit()
    return False


def end_menu(value):
    draw_window_transparent(value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8],
                            value[9], value[10], value[11])
    color = (0, 0, 0)
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
                    sounds.play_sound("menu_sound")
                    return True
        pygame.display.update()
    pygame.quit()
    return False


def win_screen(value):
    draw_window_transparent(value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8],
                            value[9], value[10], value[11])
    color = (255, 255, 255)
    font = pygame.font.SysFont('Arial', scale(32))
    win_text = font.render('You win! Well played', True, color)
    reset_text = font.render('Click this text to start a new game', True, color)
    continue_text = font.render('Click this text to continue the game', True, color)
    button_rect = reset_text.get_rect()
    button_rect[0] = width / 6
    button_rect[1] = height / 2.5 + (height / 2.5 - height / 3.5)
    continue_button_rect = continue_text.get_rect()
    continue_button_rect[0] = width / 6
    continue_button_rect[1] = height / 2.5
    run = True
    while run:
        WIN.blit(win_text, (width / 6, height / 3.5))
        WIN.blit(continue_text, (width / 6, height / 2.5))
        WIN.blit(reset_text, (width / 6, height / 2.5 + (height / 2.5 - height / 3.5)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse):
                    sounds.play_sound("menu_sound")
                    return 2
                if continue_button_rect.collidepoint(mouse):
                    sounds.play_sound("menu_sound")
                    return 1
                    print("hi")
        pygame.display.update()
    pygame.quit()
    return False


def level_screen(sprite_sheet, game_map):
    sound_bar = SoundBar(sprite_sheet, volume)
    draw_window_transparent([], [], [], None, pygame.mouse.get_pos(), None, sprite_sheet, game_map, None, sound_bar,
                            False, FPS)
    color = (255, 255, 255)
    font = pygame.font.SysFont('Arial', scale(32))
    level_1_text = font.render('Click for level 1 Map', True, color)
    button_1_rect = level_1_text.get_rect()
    button_1_rect[0] = width / 6
    button_1_rect[1] = height / 3.5
    level_2_text = font.render('Click for level 2 Map', True, color)
    button_2_rect = level_2_text.get_rect()
    button_2_rect[0] = width / 6
    button_2_rect[1] = height / 2.5
    level_3_text = font.render('Click for level 3 Map', True, color)
    button_3_rect = level_3_text.get_rect()
    button_3_rect[0] = width / 6
    button_3_rect[1] = height / 2.5 + (height / 2.5 - height / 3.5)
    run = True
    while run:
        WIN.blit(level_1_text, (width / 6, height / 3.5))
        WIN.blit(level_2_text, (width / 6, height / 2.5))
        WIN.blit(level_3_text, (width / 6, height / 2.5 + (height / 2.5 - height / 3.5)))
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if button_1_rect.collidepoint(mouse):
                if game_map.name != "default":
                    game_map.set_default_map()
                    draw_window_transparent([], [], [], None, pygame.mouse.get_pos(), None, sprite_sheet, game_map,
                                            None,
                                            sound_bar, False, FPS)
                    level_1_text = font.render('Click for level 1 Map', True, color)
                    level_2_text = font.render('Click for level 2 Map', True, color)
                    level_3_text = font.render('Click for level 3 Map', True, color)
            if button_2_rect.collidepoint(mouse):
                if game_map.name != "level_2":
                    game_map.set_level_2_map()
                    draw_window_transparent([], [], [], None, pygame.mouse.get_pos(), None, sprite_sheet, game_map,
                                            None,
                                            sound_bar, False, FPS)
                    level_1_text = font.render('Click for level 1 Map', True, color)
                    level_2_text = font.render('Click for level 2 Map', True, color)
                    level_3_text = font.render('Click for level 3 Map', True, color)
            if button_3_rect.collidepoint(mouse):
                if game_map.name != "level_3":
                    game_map.set_level_3_map()
                    draw_window_transparent([], [], [], None, pygame.mouse.get_pos(), None, sprite_sheet, game_map,
                                            None,
                                            sound_bar, False, FPS)
                    level_1_text = font.render('Click for level 1 Map', True, color)
                    level_2_text = font.render('Click for level 2 Map', True, color)
                    level_3_text = font.render('Click for level 3 Map', True, color)
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if button_1_rect.collidepoint(mouse):
                    game_map.set_default_map()
                    sounds.play_sound("menu_sound")
                    return True
                if button_2_rect.collidepoint(mouse):
                    game_map.set_level_2_map()
                    sounds.play_sound("menu_sound")
                    return True
                if button_3_rect.collidepoint(mouse):
                    game_map.set_level_3_map()
                    sounds.play_sound("menu_sound")
                    return True
        pygame.display.update()
    pygame.quit()
    return False


def information_screen(sprite_sheet, game_map):
    sound_bar = SoundBar(sprite_sheet, volume)

    # Upgrades - update these values after changing them in main_game_loop
    player_health = 10000
    player_money = 100000
    won = False
    # So these get properly updated instead of just on hit/change
    global lives_string, money_string
    lives_string = "Lives: " + str(int(math.floor(player_health)))
    # TODO - figure out why we can't put money string in like this cause otherwise it's bugged
    money_string = "Money: " + str(player_money)
    re_render_money_and_lives()

    run = True
    draw_window_transparent([], [], [], None, pygame.mouse.get_pos(), None, sprite_sheet, game_map, None, sound_bar,
                            False, FPS)
    while run:
        # enemies, towers, projectiles, selected_tower, mouse_cords, current_tower_info, sprite_sheet,
        # game_map, hovered_tower_info, sound_bar, start_round, fps

        WIN.blit(sprite_sheet.POP_UP, (2 * sprite_sheet.TILE_SIZE, 2 * sprite_sheet.TILE_SIZE))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                rect = sprite_sheet.POP_UP.get_rect()
                rect.x += scale(32) * 2
                rect.y += scale(32) * 2
                if rect.collidepoint(mouse):
                    sounds.play_sound("menu_sound")
                    return True
        pygame.display.update()
    pygame.quit()
    return False


def main():
    sprites = SpriteSets()
    game_map = Map()
    loop = True
    while loop:
        if start_menu(sprites, game_map):
            if level_screen(sprites, game_map):
                if information_screen(sprites, game_map):
                    value = game_loop(sprites, game_map)
                    global score, round_number
                    score = 0
                    round_number = 0
                    if value == False:
                        loop = False
                    else:
                        if value != 3 and value != 2:
                            if value[0] == 1:
                                if end_menu(value[1]):
                                    pass
                                else:
                                    loop = False
                        if value == 2:
                            loop = True
                        if value == 3:
                            loop = False
                else:
                    loop = False
            else:
                loop = False
        else:
            loop = False


if __name__ == '__main__':
    # might be a better way to do this, but this works
    # tower presets needs pygame to be init before it is imported
    from PythonDefense.tower import Tower, get_tower_from_preset, tower_presets

    main()
