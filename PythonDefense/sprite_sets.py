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

        self.GRASS_TILE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'tiles', 'grass_tile.png')).convert()
        self.DIRT_TILE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'tiles', 'dirt_tile.png')).convert()
        self.MENU_TILE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'tiles', 'menu_tile.png')).convert()
        self.HILITE_TILE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'buttons', 'hilite.png')).convert_alpha()
        self.TOWER1_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'tower1.png')).convert_alpha()
        self.TOWER2_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'tower2.png')).convert_alpha()
        self.TOWER3_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'tower3.png')).convert_alpha()
        self.TOWER4_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'tower4.png')).convert_alpha()
        self.TOWER5_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'towers', 'tower5.png')).convert_alpha()
        self.ENEMY1_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'enemies', 'enemy1.png')).convert_alpha()
        self.ENEMY2_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'enemies', 'enemy2.png')).convert_alpha()
        self.ENEMY3_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'enemies', 'enemy3.png')).convert_alpha()
        self.FIRE_PROJECTILE_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'projectiles', 'fireball.png')).convert()
        self.ICE_PROJECTILE_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'projectiles', 'iceball.png')).convert()
        self.UPGRADE_SPRITE = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'assets', 'buttons', 'bt-upgrade-red.jpg')).convert()
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

        # Scale images
        self.GRASS_TILE = pygame.transform.scale(self.GRASS_TILE, self.TILE_XY)
        self.DIRT_TILE = pygame.transform.scale(self.DIRT_TILE, self.TILE_XY)
        self.MENU_TILE = pygame.transform.scale(self.MENU_TILE, self.TILE_XY)
        self.HILITE_TILE = pygame.transform.scale(self.HILITE_TILE, self.TILE_XY)

        self.TOWER1_SPRITE = pygame.transform.scale(self.TOWER1_SPRITE, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.TOWER2_SPRITE = pygame.transform.scale(self.TOWER2_SPRITE, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.TOWER3_SPRITE = pygame.transform.scale(self.TOWER3_SPRITE, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.TOWER4_SPRITE = pygame.transform.scale(self.TOWER4_SPRITE, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.TOWER5_SPRITE = pygame.transform.scale(self.TOWER5_SPRITE, (self.TOWER_SIZE, self.TOWER_SIZE))
        self.ENEMY1_SPRITE = pygame.transform.scale(self.ENEMY1_SPRITE, (self.ENEMY_SIZE, self.ENEMY_SIZE))
        self.ENEMY2_SPRITE = pygame.transform.scale(self.ENEMY2_SPRITE, (self.ENEMY_SIZE, self.ENEMY_SIZE))
        self.ENEMY3_SPRITE = pygame.transform.scale(self.ENEMY3_SPRITE, (self.ENEMY_SIZE, self.ENEMY_SIZE))
        self.FIRE_PROJECTILE_SPRITE = pygame.transform.scale(self.FIRE_PROJECTILE_SPRITE,
                                                             (self.FIRE_PROJECTILE_SIZE, self.FIRE_PROJECTILE_SIZE))
        self.ICE_PROJECTILE_SPRITE = pygame.transform.scale(self.ICE_PROJECTILE_SPRITE,
                                                            (self.ICE_PROJECTILE_SIZE, self.ICE_PROJECTILE_SIZE))
        self.UPGRADE_SPRITE = pygame.transform.scale(self.UPGRADE_SPRITE, (self.TILE_SIZE * 2, self.TILE_SIZE))
        self.UPGRADE_DAMAGE_SPRITE = pygame.transform.scale(self.UPGRADE_DAMAGE_SPRITE, (self.TILE_SIZE, self.TILE_SIZE))
        self.UPGRADE_RANGE_SPRITE = pygame.transform.scale(self.UPGRADE_RANGE_SPRITE, (self.TILE_SIZE, self.TILE_SIZE))
        self.UPGRADE_SPEED_SPRITE = pygame.transform.scale(self.UPGRADE_SPEED_SPRITE, (self.TILE_SIZE, self.TILE_SIZE))
        self.START_SPRITE = pygame.transform.scale(self.START_SPRITE, (self.TILE_SIZE * 2, self.TILE_SIZE))

        self.LEVEL1_TILE = pygame.transform.scale(self.LEVEL1_TILE, self.TILE_XY)
        self.LEVEL2_TILE = pygame.transform.scale(self.LEVEL2_TILE, self.TILE_XY)
        self.LEVEL3_TILE = pygame.transform.scale(self.LEVEL3_TILE, self.TILE_XY)
        self.LEVEL4_TILE = pygame.transform.scale(self.LEVEL4_TILE, self.TILE_XY)
        self.LEVEL5_TILE = pygame.transform.scale(self.LEVEL5_TILE, self.TILE_XY)