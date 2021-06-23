class Player:
    def __init__(self, health, money):
        self.health = health
        self.money = money

    def AddMoney(self):
        self.money = self.money + 1

    def getMoney(self):
        return self.money

    def takeDamage(self):
        self.health = self.health - 1

    def getHealth(self):
        return self.health
