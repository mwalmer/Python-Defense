from helper_functions import scale


class Projectile:
    def __init__(self, name, damage, attack_speed, rect, sprite):
        self.name = name
        self.damage = damage
        self.attack_speed = attack_speed
        self.rect = rect
        self.x = rect.x
        self.y = rect.y
        self._sprite = sprite
        self.sprite = sprite

    def cords(self):
        return self.x, self.y

    # TODO: make a constant speed, right now as the projectile gets closer it slows down, might never reach enemy either
    def motion(self, change_x, change_y):
        self.x = self.x + (change_x - self.x)//scale(32)
        self.y = self.y + (change_y - self.y)//scale(32)

    def absolute_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
