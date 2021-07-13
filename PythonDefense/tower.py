from PythonDefense.projectile import Projectile
import copy
import math
import sprite_sets


def get_tower_presets():
    sprite_set = sprite_sets.SpriteSets()

    tower_presets = {
        "python": ["python_tower", 1, 1, 500, sprite_set.PYTHON_TOWER_SPRITE,
                   "python_projectile", sprite_set.ICE_PROJECTILE_SPRITE, 10, Projectile.snake_shot],
        "java": ["java_tower", 1, 1, 500, sprite_set.JAVA_TOWER_SPRITE,
                    "java_projectile", sprite_set.FIRE_PROJECTILE_SPRITE, 10, Projectile.motion],
        "cpp": ["cpp_tower", 1, 1, 500, sprite_set.CPP_TOWER_SPRITE,
                   "cpp_projectile", sprite_set.FIRE_PROJECTILE_SPRITE, 10, Projectile.motion],
        "javascript": ["javascript_tower", 1, 1, 500, sprite_set.JAVASCRIPT_TOWER_SPRITE,
                   "javascript_projectile", sprite_set.FIRE_PROJECTILE_SPRITE, 10, Projectile.motion],
        "lisp": ["lisp_tower", 1, 1, 500, sprite_set.LISP_TOWER_SPRITE,
                   "lisp_projectile", sprite_set.FIRE_PROJECTILE_SPRITE, 10, Projectile.arc_motion],
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
    sprite = tp[4]
    projectile_name = tp[5]
    projectile_rect = projectile_rect
    projectile_sprite = tp[6]
    ticks = ticks
    projectile_speed = tp[7]
    projectile_motion = Projectile.motion

    return Tower(name, damage, attack_speed, range, rect, sprite, projectile_name, projectile_rect,
                 projectile_sprite, ticks, projectile_speed, projectile_motion)


class Tower:
    def __init__(self, name, damage, attack_speed, range, rect, sprite, projectile_name, projectile_rect,
                 projectile_sprite, ticks, projectile_speed, projectile_motion_function):
        self.can_shoot = True
        self.name = name
        self.damage = damage
        self.attack_speed = 1000 / attack_speed
        self.range = range
        self.rect = rect
        self.x = rect.x
        self.y = rect.y
        self._sprite = sprite
        self.sprite = sprite
        self.projectile = Projectile(projectile_name, damage, projectile_speed, projectile_rect, projectile_sprite, projectile_motion_function)
        self.projectile_motion_function = projectile_motion_function
        self.ticks = ticks
        self.level = 1
        self.projectile_speed = projectile_speed

    # returns a new copy of its projectile, if it didn't the tower could only shoot once
    def fire_projectile(self, closest):
        self.projectile.closest = closest
        return copy.copy(self.projectile)

    def cords(self):
        return self.x, self.y

    def any_within_range(self, enemies):
        for i in range(len(enemies)):
            if self.within_range(enemies[i].x, enemies[i].y):
                return i
        return -1

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
                                     self.projectile.sprite, self.projectile_motion_function)
        self.range += range
        if self.level < 5:
            self.level = self.level + 1

    # Checks if you can level up tower (MAX LEVEL 5)
    def level_up(self):
        if self.level < 5:
            return True
        return False
