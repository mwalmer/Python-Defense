from projectile import Projectile
import copy


class Tower:
    def __init__(self, name, damage, attack_speed, rect, sprite, projectile_name, projectile_rect, projectile_sprite, ticks):
        self.name = name
        self.damage = damage
        self.attack_speed = 1000 / attack_speed
        self.rect = rect
        self.x = rect.x
        self.y = rect.y
        self._sprite = sprite
        self.sprite = sprite
        self.projectile = Projectile(projectile_name, damage, attack_speed, projectile_rect, projectile_sprite)
        self.ticks = ticks
        self.level = 1

    # returns a new copy of its projectile, if it didn't the tower could only shoot once
    def fire_projectile(self):
        return copy.copy(self.projectile)

    def cords(self):
        return self.x, self.y

    # basic upgrade function for towers
    def basic_upgrade(self, damage, attack_speed):
        self.damage = self.damage + damage
        self.attack_speed = self.attack_speed + attack_speed
        proj_damage = self.projectile.damage + damage
        proj_attack_speed = self.projectile.attack_speed + attack_speed
        self.projectile = Projectile(self.projectile.name, proj_damage, proj_attack_speed, self.projectile.rect, self.projectile.sprite)
        if self.level < 5:
            self.level = self.level + 1

    # Checks if you can level up tower (MAX LEVEL 5)
    def level_up(self):
        if self.level < 5:
            return True
        return False
