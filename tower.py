from projectile import Projectile


class Tower:
    def __init__(self, name, damage, attack_speed, rect, sprite, projectile_name, projectile_rect, projectile_sprite):
        self.name = name
        self.damage = damage
        self.attack_speed = attack_speed
        self.rect = rect
        self.x = rect.x
        self.y = rect.y
        self._sprite = sprite
        self.sprite = sprite
        self.projectile = Projectile(projectile_name, damage, attack_speed, projectile_rect, projectile_sprite)

    def cords(self):
        return self.x, self.y

    #basic upgrade function for towers
    def basic_upgrade(self, damage, attack_speed):
        self.damage = damage
        self.attack_speed = attack_speed
        self.projectile = Projectile(self.projectile.name, damage, attack_speed, self.projectile.rect, self.projectile.sprite)
