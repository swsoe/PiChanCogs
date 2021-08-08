class Player():

    def __init__(self, playerData):
        self.currentLife = playerData["currentLife"]
        self.maxLife = playerData["maxLife"]
        self.coolPoints = playerData["coolPoints"]
        self.coins = playerData["coins"]
        self.xp = playerData["xp"]
        self.trophies = playerData["inventory"]["trophies"]
        self.consumables = playerData["inventory"]["consumables"]

        self.requiredXP = [ # The XP required for a particular level, for levels 1 through 30.
            0, 100, 300, 600, 1000, 1500, 2100, 2800, 3600, 4500,
            5500, 6600, 7800, 9100, 10500, 12000, 13600, 15300, 17100, 19000,
            22000, 26000, 31000, 37000, 45000, 54000, 64000, 75000, 87000, 100000 ]

    def ToDictionary(self):
        return {
            "currentLife": self.currentLife,
            "maxLife": self.maxLife,
            "coolPoints": self.coolPoints,
            "coins": self.coins,
            "xp": self.xp,
            "inventory": {
                "trophies": self.trophies,
                "consumables": self.consumables
            }
        }

    def GetCurrentLife(self) -> int:
        return self.currentLife

    def GetMaxLife(self) -> int:
        return self.maxLife

    def GetCoolPoints(self) -> int:
        return self.coolPoints

    def GetCoins(self) -> int:
        return self.coins

    def AddCoins(self, coins: int) -> bool:
        self.coins += coins
        return True

    def SetCoins(self, coins: int) -> bool:
        self.coins = coins
        return True

    def GetXP(self) -> int:
        return self.xp

    def AddXP(self, xp: int) -> bool:
        currentLevel = self.GetLevel()
        self.xp += xp
        newLevel = self.GetLevel()
        if currentLevel < newLevel:
            return True
        return False

    def GetLevel(self) -> int:
        level = 0
        for x in self.requiredXP:
            if x > self.xp:
                break
            level += 1
        return level

    def GetRemainingXP(self) -> int:
        level = self.GetLevel()
        if level >= len(self.requiredXP):
            return 0
        else:
            return self.requiredXP[level] - self.GetXP()
