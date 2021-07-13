from PythonDefense.helper_functions import scale
import math


class Projectile:
    def __init__(self, name, damage, projectile_speed, rect, sprite, movement_function):
        self.name = name
        self.damage = damage
        self.projectile_speed = projectile_speed
        self.rect = rect
        self.x = rect.x
        self.y = rect.y
        self._sprite = sprite
        self.sprite = sprite
        self.remove = False
        self.closest = None
        self.movement_function = movement_function
        self.sin_val = math.pi/64
        self.flip = False

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

    def snake_shot(self, change_x, change_y):
        x_component = change_x - self.x
        y_component = change_y - self.y
        if x_component == 0:
            x_component = .0000000000001
        x_direction = math.cos(math.atan2(y_component, x_component))
        y_direction = math.sin(math.atan2(y_component, x_component))
        self.x = (self.x + x_direction * scale(2) * self.projectile_speed * abs(math.sin(self.sin_val)))
        self.y = (self.y + y_direction * scale(1) * self.projectile_speed * abs(math.cos(self.sin_val)))
        self.sin_val += math.pi/64
        self.rect.x = self.x
        self.rect.y = self.y

    def absolute_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.rect.x = self.x
        self.rect.y = self.y

    def flag_removal(self):
        self.remove = True
