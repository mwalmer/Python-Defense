from PythonDefense.helper_functions import scale, lib
import math
import numpy
from ctypes import *


class Projectile:
    def __init__(self, name, damage, projectile_speed, rect, sprites, movement_function):
        self.name = name
        self.damage = damage
        self.projectile_speed = projectile_speed
        self.rect = rect
        self.x = rect.x
        self.y = rect.y
        self.sprites = sprites
        self.sprite_count = len(self.sprites)
        if name == "javascript_projectile":
            print(numpy.random.randint(0, self.sprite_count))
            init_sprite_num = numpy.random.randint(0, self.sprite_count)
            self.cur_sprite_num = init_sprite_num
            self._sprite = sprites[init_sprite_num]
            self.sprite = sprites[init_sprite_num]
        else:
            self.cur_sprite_num = 0
            self._sprite = sprites[0]
            self.sprite = sprites[0]
        self.anim_num = 0
        self.remove = False
        self.closest = None
        self.movement_function = movement_function
        self.sin_val = math.pi / 64
        self.flip = 0
        self.radians = 2 * math.pi - math.pi / 8

    def cords(self):
        return self.x, self.y

    def __call__(self):
        return self

    def motion(self, change_x, change_y):
        self.x = c_double(self.x)
        self.y = c_double(self.y)

        lib.motion(c_double(change_x), c_double(change_y), byref(self.x), byref(self.y), c_double(scale(1)),
                   c_double(self.projectile_speed))

        self.x = self.x.value
        self.y = self.y.value
        self.rect.x = self.x
        self.rect.y = self.y
        Projectile.animation_update(self, 10)

    def js_motion(self, change_x, change_y):
        self.x = c_double(self.x)
        self.y = c_double(self.y)

        lib.motion(c_double(change_x), c_double(change_y), byref(self.x), byref(self.y), c_double(scale(1)),
                   c_double(self.projectile_speed))

        self.x = self.x.value
        self.y = self.y.value
        self.rect.x = self.x
        self.rect.y = self.y

        Projectile.animation_update(self, 4)

    def arc_motion(self, change_x, change_y):
        self.x = c_double(self.x)
        self.y = c_double(self.y)

        lib.arc_motion(c_double(change_x), c_double(change_y), byref(self.x), byref(self.y), c_double(scale(1)),
                       c_double(self.projectile_speed))

        self.x = self.x.value
        self.y = self.y.value
        self.rect.x = self.x
        self.rect.y = self.y

        Projectile.animation_update(self, 16)

    def snake_shot(self, change_x, change_y):
        self.x = c_double(self.x)
        self.y = c_double(self.y)

        self.sin_val += math.pi / 64
        lib.snake_shot(c_double(change_x), c_double(change_y), byref(self.x), byref(self.y), c_double(scale(1)),
                       c_double(self.projectile_speed), c_double(self.sin_val))

        self.x = self.x.value
        self.y = self.y.value
        self.rect.x = self.x
        self.rect.y = self.y
        Projectile.animation_update(self, 10)

    def around_shot(self, change_x, change_y):

        self.x = c_double(self.x)
        self.y = c_double(self.y)
        self.radians += math.pi / 8
        lib.around_shot(byref(self.x), byref(self.y), c_double(scale(16)), c_double(-scale(32)), c_int(self.flip),
                        c_double(self.radians))
        self.flip += 1
        # if (rock):
        #    velocity = math.pi / 8
        #    if self.flip < 1:
        #        self.x = self.x + scale(16)
        #        self.y = self.y - scale(32)
        #        self.flip += 1
        #    else:
        #        self.radians += velocity
        #        self.x = self.x + math.cos(self.radians) * 25
        #        self.y = self.y + math.sin(self.radians) * 25

        self.x = self.x.value
        self.y = self.y.value
        self.rect.x = self.x
        self.rect.y = self.y
        Projectile.animation_update(self, 10)

    def animation_update(self, update_num):
        try:
            if lib.modulo_zero(int(self.anim_num), int(update_num)):
                if self.cur_sprite_num >= self.sprite_count - 1:
                    self.cur_sprite_num = 0
                else:
                    self.cur_sprite_num += 1
                self.sprite = self.sprites[self.cur_sprite_num]
        except Exception:
            print('Animation Exception: PROJECTILE')
            if self.anim_num % update_num == 0:
                if self.cur_sprite_num >= self.sprite_count - 1:
                    self.cur_sprite_num = 0
                else:
                    self.cur_sprite_num += 1
                self.sprite = self.sprites[self.cur_sprite_num]
        self.anim_num += 1

    def absolute_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.rect.x = self.x
        self.rect.y = self.y

    def flag_removal(self):
        self.remove = True
