from PythonDefense.projectile import Projectile
import copy
import math
import sprite_sets
from helper_functions import scale
import pygame
from ctypes import *


def load_c_lib():
    lib = cdll.LoadLibrary("./c_src.dll")
    lib.modulo_zero.restype = c_bool
    lib.modulo_zero.argtypes = [c_int, c_int]
    return lib


def get_tower_presets():
    sprite_set = sprite_sets.SpriteSets()
    font = pygame.font.SysFont('Arial', scale(14))

    '''
    python - basic tower
    java - might add water tiles to map, this could be a water tower
    cpp - high damage, high attack-speed but has to be compiled/built at start of each round. The more upgrades
        the longer it takes to build
    javascript - slow attack speed, slows enemies
    lisp - projectile doesn't break and follows set path
    '''
    python_cost = 15
    java_cost = 25
    cpp_cost = 50
    javascript_cost = 10
    lisp_cost = 100

    tower_presets = {
        "python": ["python_tower", .1, 1, scale(250), [sprite_set.PYTHON_TOWER_SPRITE],  # tower
                   "python_projectile", [sprite_set.ICE_PROJECTILE_SPRITE], 10, Projectile.snake_shot,  # projectile
                   python_cost,
                   font.render("python tower", False, (0, 0, 0)).convert(),  # text name
                   font.render(f"cost ${python_cost}", False, (0, 0, 0)).convert(),  # text cost
                   font.render("a description for the tower", False, (0, 0, 0)).convert()],  # text description

        "java": ["java_tower", 1, 1, scale(250), [sprite_set.JAVA_TOWER_SPRITE],
                 "java_projectile", [sprite_set.FIRE_PROJECTILE_SPRITE, sprite_set.ICE_PROJECTILE_SPRITE], 10,
                 Projectile.motion,
                 java_cost,
                 font.render("java tower", False, (0, 0, 0)).convert(),
                 font.render(f"cost ${java_cost}", False, (0, 0, 0)).convert(),
                 font.render("a description for the tower", False, (0, 0, 0)).convert()],

        "cpp": ["cpp_tower", 1, 1, scale(250),
                [sprite_set.CPP_TOWER_SPRITE, sprite_set.CPP_LOADING_1_SPRITE, sprite_set.CPP_LOADING_2_SPRITE,
                 sprite_set.CPP_LOADING_3_SPRITE, sprite_set.CPP_LOADING_4_SPRITE, sprite_set.CPP_LOADING_5_SPRITE,
                 sprite_set.CPP_LOADING_6_SPRITE, sprite_set.CPP_LOADING_7_SPRITE, sprite_set.CPP_LOADING_8_SPRITE,
                 sprite_set.CPP_LOADING_9_SPRITE, sprite_set.CPP_LOADING_10_SPRITE, sprite_set.CPP_LOADING_11_SPRITE,
                 sprite_set.CPP_LOADING_12_SPRITE, sprite_set.CPP_LOADING_13_SPRITE],
                "cpp_projectile", [sprite_set.FIRE_PROJECTILE_SPRITE_BIG], 10,
                Projectile.motion,
                cpp_cost,
                font.render("c++ tower", False, (0, 0, 0)).convert(),
                font.render(f"cost ${cpp_cost}", False, (0, 0, 0)).convert(),
                font.render("a description for the tower", False, (0, 0, 0)).convert()],

        "javascript": ["javascript_tower", 1, 1, scale(250), [sprite_set.JAVASCRIPT_TOWER_SPRITE],
                       "javascript_projectile",
                       [sprite_set.GLITCH_PROJECTILE_SPRITE], 10, Projectile.motion,
                       javascript_cost,
                       font.render("javascript tower", False, (0, 0, 0)).convert(),
                       font.render(f"cost ${javascript_cost}", False, (0, 0, 0)).convert(),
                       font.render("a description for the tower", False, (0, 0, 0)).convert()],

        "lisp": ["lisp_tower", 1, 1, scale(250), [sprite_set.LISP_TOWER_SPRITE],
                 "lisp_projectile", [sprite_set.FIRE_PROJECTILE_SPRITE, sprite_set.FIRE_PROJECTILE_SPRITE_2, sprite_set.FIRE_PROJECTILE_SPRITE_3], 10,
                 Projectile.arc_motion,
                 lisp_cost,
                 font.render("lisp tower", False, (0, 0, 0)).convert(),
                 font.render(f"cost ${lisp_cost}", False, (0, 0, 0)).convert(),
                 font.render("a description for the tower", False, (0, 0, 0)).convert()]
    }

    return tower_presets


def get_tower_from_preset(tower_name, ticks, tower_rect, projectile_rect):
    tower_presets = get_tower_presets()
    tp = tower_presets[tower_name]
    name = tp[0]
    damage = tp[1]
    attack_speed = tp[2]
    range = tp[3]
    rect = tower_rect
    sprites = tp[4]
    projectile_name = tp[5]
    projectile_rect = projectile_rect
    projectile_sprite = tp[6]
    ticks = ticks
    projectile_speed = tp[7]
    projectile_motion = tp[8]
    cost = tp[9]

    return Tower(name, damage, attack_speed, range, rect, sprites, projectile_name, projectile_rect,
                 projectile_sprite, ticks, projectile_speed, projectile_motion, cost)


class Tower:
    def __init__(self, name, damage, attack_speed, range, rect, sprites, projectile_name, projectile_rect,
                 projectile_sprite, ticks, projectile_speed, projectile_motion_function, cost):
        self.cost = cost
        self.can_shoot = True
        self.name = name
        self.damage = damage
        self.attack_speed = 1000 / attack_speed
        self.range = range
        self.rect = rect
        self.x = rect.x
        self.y = rect.y
        self._sprites = sprites
        self.sprites = sprites
        self.sprite = sprites[0]
        self.sprite_count = len(sprites)
        self.cur_sprite_num = 0
        self.anim_num = 0
        self.projectile = Projectile(projectile_name, damage, projectile_speed, projectile_rect, projectile_sprite,
                                     projectile_motion_function)
        self.projectile_motion_function = projectile_motion_function
        self.ticks = ticks
        self.level = 1
        self.projectile_speed = projectile_speed
        self.target_mode = 0  # 0 - furthest, 1 - last enemy
        self.range_surf = None
        self.attr_levels_dict = {'damage': 1, 'attack_speed': 1, 'projectile_speed': 1, 'range': 1}

    def multiple_animations(self, update_num, enemies):
        if self.name == "cpp_tower":
            if self.cur_sprite_num == self.sprite_count - 1:
                if self.get_first_enemy(enemies) is None:
                    return
        self.animation_update(update_num)

    def animation_update(self, update_num):
        try:
            lib = load_c_lib()
            if lib.modulo_zero(self.anim_num, update_num):
                if self.cur_sprite_num >= self.sprite_count - 1:
                    self.cur_sprite_num = 0
                else:
                    self.cur_sprite_num += 1
                self.sprite = self.sprites[self.cur_sprite_num]
        except Exception:
            if self.anim_num % update_num == 0:
                if self.cur_sprite_num >= self.sprite_count - 1:
                    self.cur_sprite_num = 0
                else:
                    self.cur_sprite_num += 1
                self.sprite = self.sprites[self.cur_sprite_num]
        self.anim_num += 1

    # returns a new copy of its projectile, if it didn't the tower could only shoot once
    def fire_projectile(self, closest):
        self.projectile.closest = closest
        return copy.copy(self.projectile)

    def cords(self):
        return self.x, self.y

    def get_enemy(self, enemies):
        if self.target_mode == 0:
            return self.get_first_enemy(enemies)
        else:
            return self.get_last_enemy(enemies)

    # gets the enemy which has traveled the furthest and is within turret range
    def get_first_enemy(self, enemies):
        enemies_in_range = []
        for enemy in enemies:
            if self.within_range(enemy.x, enemy.y):
                enemies_in_range.append(enemy)

        furthest_enemy = None
        for enemy in enemies_in_range:
            temp_enemy = enemy
            if furthest_enemy is None or temp_enemy.total_dist_traveled > furthest_enemy.total_dist_traveled:
                furthest_enemy = temp_enemy
        return furthest_enemy

    # gets the enemy last in line
    def get_last_enemy(self, enemies):
        enemies_in_range = []
        for enemy in enemies:
            if self.within_range(enemy.x, enemy.y):
                enemies_in_range.append(enemy)

        last_enemy = None
        for enemy in enemies_in_range:
            temp_enemy = enemy
            if last_enemy is None or temp_enemy.total_dist_traveled < last_enemy.total_dist_traveled:
                last_enemy = temp_enemy
        return last_enemy

    def within_range(self, enemy_x, enemy_y):
        if math.sqrt((enemy_x - self.x) ** 2 + (enemy_y - self.y) ** 2) <= self.range:
            return True
        return False

    # basic upgrade function for towers
    def basic_upgrade(self, damage, attack_speed, projectile_speed, range):
        self.damage += damage
        self.attack_speed -= 1000 / (attack_speed * 2)
        self.projectile_speed += projectile_speed
        self.projectile = Projectile(self.projectile.name, self.damage, self.projectile_speed, copy.copy(self.rect),
                                     self.projectile.sprites, self.projectile_motion_function)
        self.range += range
        if self.level < 5:
            self.level = self.level + 1
        self.range_surf = None

    # Checks if you can level up tower (MAX LEVEL 5)
    def level_up(self):
        if self.level < 5:
            return True
        return False

    def upgrade_damage(self, damage):
        damage_level = self.attr_levels_dict['damage']
        if damage_level < 5:
            self.damage += damage
            self.attr_levels_dict['damage'] = damage_level + 1
            print('damage upgraded! New level: ', self.attr_levels_dict['damage'])

    def upgrade_attack_speed(self, attack_speed):
        attack_speed_level = self.attr_levels_dict['attack_speed']
        if attack_speed_level < 5:
            self.attack_speed -= 1000 / (attack_speed * 2)
            self.attr_levels_dict['attack_speed'] = attack_speed_level + 1
            print('attack speed upgraded! New level: ', self.attr_levels_dict['attack_speed'])

    def upgrade_projectile_speed(self, projectile_speed):
        projectile_speed_level = self.attr_levels_dict['projectile_speed']
        if projectile_speed_level < 5:
            self.projectile_speed += projectile_speed
            self.projectile = Projectile(self.projectile.name, self.damage, self.projectile_speed, copy.copy(self.rect),
                                         self.projectile.sprites, self.projectile_motion_function)
            self.attr_levels_dict['projectile_speed'] = projectile_speed_level + 1
            print('projectile speed upgraded! New level: ', self.attr_levels_dict['projectile_speed'])

    def upgrade_range(self, range):
        range_level = self.attr_levels_dict['range']
        if range_level < 5:
            self.range += range
            self.attr_levels_dict['range'] = range_level + 1
            print('range upgraded! New level: ', self.attr_levels_dict['range'])

    def check_attr_dict(self, attr_string):
        level = self.attr_levels_dict[attr_string]
        if level < 5:
            return True
        else:
            return False
