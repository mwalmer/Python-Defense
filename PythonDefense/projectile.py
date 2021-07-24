from PythonDefense.helper_functions import scale, lib
import math


class Projectile:
    def __init__(self, name, damage, projectile_speed, rect, sprites, movement_function):
        self.name = name
        self.damage = damage
        self.projectile_speed = projectile_speed
        self.rect = rect
        self.x = rect.x
        self.y = rect.y
        self._sprite = sprites[0]
        self.sprite = sprites[0]
        self.sprites = sprites
        self.cur_sprite_num = 0
        self.sprite_count = len(self.sprites)
        self.anim_num = 0
        self.remove = False
        self.closest = None
        self.movement_function = movement_function
        self.sin_val = math.pi/64
        self.flip = 0
        self.radians = 2 * math.pi
    def cords(self):
        return self.x, self.y

    def __call__(self):
        return self

    def motion(self, change_x, change_y):
        x_component = change_x - self.x
        y_component = change_y - self.y
        if x_component == 0:
            x_component = .0000000000001
        x_direction = math.cos(math.atan2(y_component, x_component))
        y_direction = math.sin(math.atan2(y_component, x_component))
        self.x = (self.x + x_direction * scale(1) * self.projectile_speed)
        self.y = (self.y + y_direction * scale(1) * self.projectile_speed)
        self.rect.x = self.x
        self.rect.y = self.y
        Projectile.animation_update(self, 10)

    def arc_motion(self, change_x, change_y):
        x_component = change_x - self.x
        y_component = change_y - self.y
        if x_component == 0:
            x_component = .0000000000001
        x_direction = math.cos(math.atan2(y_component, x_component))
        y_direction = math.sin(math.atan2(y_component, x_component))
        self.x = (self.x + x_direction * scale(1) * self.projectile_speed) + y_direction * scale(1)
        self.y = (self.y + y_direction * scale(1) * self.projectile_speed) + x_direction * scale(1)
        self.rect.x = self.x
        self.rect.y = self.y
        Projectile.animation_update(self, 8)

    def snake_shot(self, change_x, change_y):
        x_component = change_x - self.x
        y_component = change_y - self.y
        if x_component == 0:
            x_component = .0000000000001
        x_direction = math.cos(math.atan2(y_component, x_component))
        y_direction = math.sin(math.atan2(y_component, x_component))
        self.x = (self.x + x_direction * scale(1) * self.projectile_speed * abs(math.sin(self.sin_val)))
        self.y = (self.y + y_direction * scale(1) * self.projectile_speed * abs(math.cos(self.sin_val)))
        self.sin_val += math.pi/64
        self.rect.x = self.x
        self.rect.y = self.y
        Projectile.animation_update(self, 8)

    def around_shot(self, change_x, change_y):
        velocity = math.pi/8
        if self.flip < 1:
            self.x = self.x + scale(16)
            self.y = self.y - scale(32)
            self.flip += 1
        else:
            self.radians += velocity
            self.x = self.x + math.cos(self.radians) * 25
            self.y = self.y + math.sin(self.radians) * 25
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
