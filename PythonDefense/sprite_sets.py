import pygame
import os

from PythonDefense.helper_functions import scale


class SpriteSets:
    def __init__(self):
        self.TILE_SIZE = scale(32)
        self.TILE_XY = (self.TILE_SIZE, self.TILE_SIZE)

        # Sizes
        self.TOWER_SIZE = self.TILE_SIZE
        self.ENEMY_SIZE = self.TILE_SIZE
        self.FIRE_PROJECTILE_SIZE = scale(16)
        self.ICE_PROJECTILE_SIZE = scale(16)
        self.GLITCH_PROJECTILE_SIZE = scale(16)

        self.GRASS_TILE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'tiles', 'grass_tile.png')).convert()
        self.DIRT_TILE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'tiles', 'dirt_tile.png')).convert()
        self.MENU_TILE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'tiles', 'menu_tile.png')).convert()
        self.WATER_TILE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'tiles', 'water_tile.png')).convert()
        self.HILITE_TILE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'buttons', 'hilite.png')).convert_alpha()
        self.PYTHON_TOWER = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'python_tower.png')).convert_alpha()
        self.JAVA_TOWER_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'java_tower.png')).convert_alpha()
        self.CPP_TOWER_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'cpp_tower.png')).convert_alpha()
        self.JAVASCRIPT_TOWER_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'javascript_tower.png')).convert_alpha()
        self.LISP_TOWER_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'lisp_tower.png')).convert_alpha()

        self.PYTHON_TOWER_FLIP = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'python_tower_flip.png')).convert_alpha()
        self.JAVA_TOWER_SPRITE_FLIP = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'java_tower_flip.png')).convert_alpha()
        self.CPP_TOWER_SPRITE_FLIP = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'cpp_tower_flip.png')).convert_alpha()
        self.JAVASCRIPT_TOWER_SPRITE_FLIP = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'javascript_tower_flip.png')).convert_alpha()
        self.LISP_TOWER_SPRITE_FLIP = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'lisp_tower_flip.png')).convert_alpha()

        self.CPP_LOADING_1_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'cpp_tower_loading_1.png')).convert_alpha()
        self.CPP_LOADING_2_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'cpp_tower_loading_2.png')).convert_alpha()
        self.CPP_LOADING_3_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'cpp_tower_loading_3.png')).convert_alpha()
        self.CPP_LOADING_4_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'cpp_tower_loading_4.png')).convert_alpha()
        self.CPP_LOADING_5_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'cpp_tower_loading_5.png')).convert_alpha()
        self.CPP_LOADING_6_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'cpp_tower_loading_6.png')).convert_alpha()
        self.CPP_LOADING_7_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'cpp_tower_loading_7.png')).convert_alpha()
        self.CPP_LOADING_8_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'cpp_tower_loading_8.png')).convert_alpha()
        self.CPP_LOADING_9_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'cpp_tower_loading_9.png')).convert_alpha()
        self.CPP_LOADING_10_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'cpp_tower_loading_10.png')).convert_alpha()
        self.CPP_LOADING_11_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'cpp_tower_loading_11.png')).convert_alpha()
        self.CPP_LOADING_12_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'cpp_tower_loading_12.png')).convert_alpha()
        self.CPP_LOADING_13_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'cpp_tower_loading_13.png')).convert_alpha()
        self.ENEMY1_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'enemies', 'Smile.png')).convert_alpha()
        self.ENEMY2_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'enemies', 'Face.png')).convert_alpha()
        self.ENEMY3_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'enemies', 'Skull.png')).convert_alpha()
        self.ENEMY4_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'enemies', 'Cool.png')).convert_alpha()
        self.ENEMY5_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'enemies', 'enemy5.png')).convert_alpha()
        self.ENEMY6_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'enemies', 'enemy6.png')).convert_alpha()
        self.FIRE_PROJECTILE_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'projectiles', 'fireball.png')).convert()
        self.FIRE_PROJECTILE_SPRITE_2 = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'projectiles', 'fireball_2.png')).convert()
        self.FIRE_PROJECTILE_SPRITE_3 = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'projectiles', 'fireball_3.png')).convert()
        self.FIRE_PROJECTILE_SPRITE_BIG = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'projectiles', 'fireball_big.png')).convert()
        self.ICE_PROJECTILE_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'projectiles', 'iceball.png')).convert()
        self.YELLOW_BALL_PROJECTILE_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'projectiles', 'yellowball.png')).convert()
        self.GLITCH_PROJECTILE_RED_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'projectiles', 'glitchball_red.png')).convert()
        self.GLITCH_PROJECTILE_ORANGE_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'projectiles', 'glitchball_orange.png')).convert()
        self.GLITCH_PROJECTILE_YELLOW_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'projectiles', 'glitchball_yellow.png')).convert()
        self.GLITCH_PROJECTILE_GREEN_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'projectiles', 'glitchball_green.png')).convert()
        self.GLITCH_PROJECTILE_BLUE_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'projectiles', 'glitchball_blue.png')).convert()
        self.GLITCH_PROJECTILE_INDIGO_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'projectiles', 'glitchball_indigo.png')).convert()
        self.GLITCH_PROJECTILE_VIOLET_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'projectiles', 'glitchball_violet.png')).convert()
        self.UPGRADE_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'buttons', 'bt-upgrade-red.png')).convert_alpha()
        self.UPGRADE_DAMAGE_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'buttons', 'bt_upgrade_damage.png')).convert_alpha()
        self.UPGRADE_RANGE_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'buttons', 'bt_upgrade_range.png')).convert_alpha()
        self.UPGRADE_SPEED_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'buttons', 'bt_upgrade_speed.png')).convert_alpha()
        self.START_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'buttons', 'bt-start.png')).convert_alpha()
        self.LEVEL1_TILE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'levels', 'num1.png')).convert_alpha()
        self.LEVEL2_TILE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'levels', 'num2.png')).convert_alpha()
        self.LEVEL3_TILE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'levels', 'num3.png')).convert_alpha()
        self.LEVEL4_TILE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'levels', 'num4.png')).convert_alpha()
        self.LEVEL5_TILE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'levels', 'num5.png')).convert_alpha()
        self.POP_UP = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'buttons', 'popup.png')).convert_alpha()

        # Scale images
        self.GRASS_TILE = pygame.transform.scale(self.GRASS_TILE, self.TILE_XY)
        self.DIRT_TILE = pygame.transform.scale(self.DIRT_TILE, self.TILE_XY)
        self.MENU_TILE = pygame.transform.scale(self.MENU_TILE, self.TILE_XY)
        self.WATER_TILE = pygame.transform.scale(self.WATER_TILE, self.TILE_XY)
        self.HILITE_TILE = pygame.transform.scale(self.HILITE_TILE, self.TILE_XY)

        self.PYTHON_TOWER_SPRITE_FLIP = pygame.transform.scale(self.PYTHON_TOWER_FLIP, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.JAVA_TOWER_SPRITE_FLIP = pygame.transform.scale(self.JAVA_TOWER_SPRITE_FLIP, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.CPP_TOWER_SPRITE_FLIP = pygame.transform.scale(self.CPP_TOWER_SPRITE_FLIP, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.JAVASCRIPT_TOWER_SPRITE_FLIP = pygame.transform.scale(self.JAVASCRIPT_TOWER_SPRITE_FLIP, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.LISP_TOWER_SPRITE_FLIP = pygame.transform.scale(self.LISP_TOWER_SPRITE_FLIP, (self.TOWER_SIZE, self.TOWER_SIZE))

        self.PYTHON_TOWER_SPRITE = pygame.transform.scale(self.PYTHON_TOWER, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.JAVA_TOWER_SPRITE = pygame.transform.scale(self.JAVA_TOWER_SPRITE, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.CPP_TOWER_SPRITE = pygame.transform.scale(self.CPP_TOWER_SPRITE, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.JAVASCRIPT_TOWER_SPRITE = pygame.transform.scale(self.JAVASCRIPT_TOWER_SPRITE,
                                                              (self.TOWER_SIZE, self.TOWER_SIZE))
        self.LISP_TOWER_SPRITE = pygame.transform.scale(self.LISP_TOWER_SPRITE, (self.TOWER_SIZE, self.TOWER_SIZE))

        self.CPP_LOADING_1_SPRITE = pygame.transform.scale(self.CPP_LOADING_1_SPRITE, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.CPP_LOADING_2_SPRITE = pygame.transform.scale(self.CPP_LOADING_2_SPRITE, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.CPP_LOADING_3_SPRITE = pygame.transform.scale(self.CPP_LOADING_3_SPRITE, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.CPP_LOADING_4_SPRITE = pygame.transform.scale(self.CPP_LOADING_4_SPRITE, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.CPP_LOADING_5_SPRITE = pygame.transform.scale(self.CPP_LOADING_5_SPRITE, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.CPP_LOADING_6_SPRITE = pygame.transform.scale(self.CPP_LOADING_6_SPRITE, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.CPP_LOADING_7_SPRITE = pygame.transform.scale(self.CPP_LOADING_7_SPRITE, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.CPP_LOADING_8_SPRITE = pygame.transform.scale(self.CPP_LOADING_8_SPRITE, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.CPP_LOADING_9_SPRITE = pygame.transform.scale(self.CPP_LOADING_9_SPRITE, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.CPP_LOADING_10_SPRITE = pygame.transform.scale(self.CPP_LOADING_10_SPRITE, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.CPP_LOADING_11_SPRITE = pygame.transform.scale(self.CPP_LOADING_11_SPRITE, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.CPP_LOADING_12_SPRITE = pygame.transform.scale(self.CPP_LOADING_12_SPRITE, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.CPP_LOADING_13_SPRITE = pygame.transform.scale(self.CPP_LOADING_13_SPRITE, (self.TOWER_SIZE, self.TOWER_SIZE))

        self.ENEMY1_SPRITE = pygame.transform.scale(self.ENEMY1_SPRITE, (self.ENEMY_SIZE, self.ENEMY_SIZE))
        self.ENEMY2_SPRITE = pygame.transform.scale(self.ENEMY2_SPRITE, (self.ENEMY_SIZE, self.ENEMY_SIZE))
        self.ENEMY3_SPRITE = pygame.transform.scale(self.ENEMY3_SPRITE, (self.ENEMY_SIZE, self.ENEMY_SIZE))
        self.ENEMY4_SPRITE = pygame.transform.scale(self.ENEMY4_SPRITE, (self.ENEMY_SIZE, self.ENEMY_SIZE))
        self.ENEMY5_SPRITE = pygame.transform.scale(self.ENEMY5_SPRITE, (self.ENEMY_SIZE, self.ENEMY_SIZE))
        self.ENEMY6_SPRITE = pygame.transform.scale(self.ENEMY6_SPRITE, (self.ENEMY_SIZE, self.ENEMY_SIZE))

        self.FIRE_PROJECTILE_SPRITE = pygame.transform.scale(self.FIRE_PROJECTILE_SPRITE,
                                                             (self.FIRE_PROJECTILE_SIZE, self.FIRE_PROJECTILE_SIZE))
        # More Visually distinct
        # self.FIRE_PROJECTILE_SPRITE_2 = pygame.transform.scale(self.FIRE_PROJECTILE_SPRITE_2,
        #                                                     (self.FIRE_PROJECTILE_SIZE, self.FIRE_PROJECTILE_SIZE))
        self.FIRE_PROJECTILE_SPRITE_3 = pygame.transform.scale(self.FIRE_PROJECTILE_SPRITE_3,
                                                             (self.FIRE_PROJECTILE_SIZE, self.FIRE_PROJECTILE_SIZE))
        self.FIRE_PROJECTILE_SPRITE_BIG = pygame.transform.scale(self.FIRE_PROJECTILE_SPRITE_BIG,
                                                             (scale(24), scale(24)))
        self.ICE_PROJECTILE_SPRITE = pygame.transform.scale(self.ICE_PROJECTILE_SPRITE,
                                                            (self.ICE_PROJECTILE_SIZE, self.ICE_PROJECTILE_SIZE))
        self.YELLOW_BALL_PROJECTILE_SPRITE = pygame.transform.scale(self.YELLOW_BALL_PROJECTILE_SPRITE,
                                                            (self.ICE_PROJECTILE_SIZE, self.ICE_PROJECTILE_SIZE))
        self.GLITCH_PROJECTILE_RED_SPRITE = pygame.transform.scale(self.GLITCH_PROJECTILE_RED_SPRITE,
                                                            (self.GLITCH_PROJECTILE_SIZE, self.GLITCH_PROJECTILE_SIZE))
        self.GLITCH_PROJECTILE_ORANGE_SPRITE = pygame.transform.scale(self.GLITCH_PROJECTILE_ORANGE_SPRITE,
                                                                   (self.GLITCH_PROJECTILE_SIZE,
                                                                    self.GLITCH_PROJECTILE_SIZE))
        self.GLITCH_PROJECTILE_YELLOW_SPRITE = pygame.transform.scale(self.GLITCH_PROJECTILE_YELLOW_SPRITE,
                                                                   (self.GLITCH_PROJECTILE_SIZE,
                                                                    self.GLITCH_PROJECTILE_SIZE))
        self.GLITCH_PROJECTILE_GREEN_SPRITE = pygame.transform.scale(self.GLITCH_PROJECTILE_GREEN_SPRITE,
                                                                   (self.GLITCH_PROJECTILE_SIZE,
                                                                    self.GLITCH_PROJECTILE_SIZE))
        self.GLITCH_PROJECTILE_BLUE_SPRITE = pygame.transform.scale(self.GLITCH_PROJECTILE_BLUE_SPRITE,
                                                                   (self.GLITCH_PROJECTILE_SIZE,
                                                                    self.GLITCH_PROJECTILE_SIZE))
        self.GLITCH_PROJECTILE_INDIGO_SPRITE = pygame.transform.scale(self.GLITCH_PROJECTILE_INDIGO_SPRITE,
                                                                   (self.GLITCH_PROJECTILE_SIZE,
                                                                    self.GLITCH_PROJECTILE_SIZE))
        self.GLITCH_PROJECTILE_VIOLET_SPRITE = pygame.transform.scale(self.GLITCH_PROJECTILE_VIOLET_SPRITE,
                                                                   (self.GLITCH_PROJECTILE_SIZE,
                                                                    self.GLITCH_PROJECTILE_SIZE))

        self.UPGRADE_SPRITE = pygame.transform.scale(self.UPGRADE_SPRITE, (self.TILE_SIZE * 4, self.TILE_SIZE))
        self.UPGRADE_DAMAGE_SPRITE = pygame.transform.scale(self.UPGRADE_DAMAGE_SPRITE, (self.TILE_SIZE, self.TILE_SIZE))
        self.UPGRADE_RANGE_SPRITE = pygame.transform.scale(self.UPGRADE_RANGE_SPRITE, (self.TILE_SIZE, self.TILE_SIZE))
        self.UPGRADE_SPEED_SPRITE = pygame.transform.scale(self.UPGRADE_SPEED_SPRITE, (self.TILE_SIZE, self.TILE_SIZE))
        self.START_SPRITE = pygame.transform.scale(self.START_SPRITE, (self.TILE_SIZE * 4, self.TILE_SIZE))

        self.LEVEL1_TILE = pygame.transform.scale(self.LEVEL1_TILE, self.TILE_XY)
        self.LEVEL2_TILE = pygame.transform.scale(self.LEVEL2_TILE, self.TILE_XY)
        self.LEVEL3_TILE = pygame.transform.scale(self.LEVEL3_TILE, self.TILE_XY)
        self.LEVEL4_TILE = pygame.transform.scale(self.LEVEL4_TILE, self.TILE_XY)
        self.LEVEL5_TILE = pygame.transform.scale(self.LEVEL5_TILE, self.TILE_XY)

        self.POP_UP = pygame.transform.scale(self.POP_UP, (scale(32 * 20), scale(32 * 16)))

        self.VOLUME = []
        for i in range(21):
            self.VOLUME.append(pygame.image.load(
                os.path.join(os.path.dirname(__file__), 'assets', 'buttons', f'Volume{i}.png')).convert())
            self.VOLUME[i] = pygame.transform.scale(self.VOLUME[i], (self.TILE_SIZE * 4, self.TILE_SIZE//2))

        self.YELLOW = pygame.Color(255, 255, 0)
        self.BLACK = pygame.Color(0, 0, 0)
        self.EMPTY_COLOR = pygame.Color(111, 207, 242)
        self.FILLED_IN_COLOR = pygame.Color(0, 150, 135)
        self.OTHER_FILLED_IN_COLOR = pygame.Color(63, 81, 181)

        self.SMALL_HIGHLIGHT = pygame.Surface((self.TILE_SIZE + scale(6), self.TILE_SIZE + scale(6))).convert()
        self.SMALL_HIGHLIGHT.fill(self.YELLOW)

        self.LARGE_HIGHLIGHT = pygame.Surface((self.TILE_SIZE * 4 + scale(6), self.TILE_SIZE + scale(6))).convert()
        self.LARGE_HIGHLIGHT.fill(self.YELLOW)

        self.SOUND_BAR_HIGHLIGHT = pygame.Surface((self.TILE_SIZE * 4 + scale(6), self.TILE_SIZE // 2 + scale(6))).convert()
        self.SOUND_BAR_HIGHLIGHT.fill(self.YELLOW)

        self.SMALL_UPGRADE_LEVEL = pygame.Surface((scale(15), scale(15))).convert()
        self.SMALL_UPGRADE_LEVEL.fill(self.BLACK)

        self.SMALL_UPGRADE_LEVEL_EMPTY = pygame.Surface((scale(10), scale(10))).convert()
        self.SMALL_UPGRADE_LEVEL_EMPTY.fill(self.EMPTY_COLOR)

        self.SMALL_UPGRADE_LEVEL_FILLED = pygame.Surface((scale(10), scale(10))).convert()
        self.SMALL_UPGRADE_LEVEL_FILLED.fill(self.FILLED_IN_COLOR)

        self.SMALL_UPGRADE_LEVEL_FILLED_ALT = pygame.Surface((scale(10), scale(10))).convert()
        self.SMALL_UPGRADE_LEVEL_FILLED_ALT.fill(self.OTHER_FILLED_IN_COLOR)

        self.SMALL_UPGRADE_LEVEL_TILTED = pygame.Surface((scale(10), scale(10)), pygame.SRCALPHA).convert_alpha()
        self.triangle = pygame.draw.polygon(self.SMALL_UPGRADE_LEVEL_TILTED, self.OTHER_FILLED_IN_COLOR,
                                            [
                                                (scale(10), 0),
                                                (0, scale(10)),
                                                (0, 0),
                                            ])

        self.RED_TILE = pygame.Surface((self.TILE_SIZE, self.TOWER_SIZE), pygame.SRCALPHA).convert_alpha()
        self.RED_TILE.fill((255, 0, 0, 60))

        self.GRAY_TILE = pygame.Surface((self.TILE_SIZE, self.TOWER_SIZE), pygame.SRCALPHA).convert_alpha()
        self.GRAY_TILE.fill((0, 0, 0, 60))

        self.LARGE_GRAY_TILE = pygame.Surface((self.TILE_SIZE * 4, self.TILE_SIZE), pygame.SRCALPHA).convert_alpha()
        self.LARGE_GRAY_TILE.fill((0, 0, 0, 80))

        self.BACKGROUND_TOWER_TILE = pygame.Surface((self.TILE_SIZE, self.TOWER_SIZE), pygame.SRCALPHA).convert_alpha()
        self.BACKGROUND_TOWER_TILE.fill(pygame.Color(0, 0, 0, 70))
        self.BORDER_TILE = pygame.Surface((self.TILE_SIZE - scale(2), self.TOWER_SIZE - scale(2))).convert()
        self.BORDER_TILE.fill(self.EMPTY_COLOR)

        self.LARGE_RED_TILE = pygame.Surface((self.TILE_SIZE * 4, self.TILE_SIZE), pygame.SRCALPHA).convert_alpha()
        self.LARGE_RED_TILE.fill((255, 0, 0, 60))
