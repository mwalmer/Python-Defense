class Tower:
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
