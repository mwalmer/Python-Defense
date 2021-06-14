class Projectile:
    def __init__(self, name, damage, attack_speed, rect, sprite) -> object:
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

    def motion(self, change_x, change_y):
        self.x += change_x
        self.y += change_y

    def absolute_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
