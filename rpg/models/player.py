class Player():

    def __init__(self, playerData):
        self.currentLife = playerData["currentLife"]
        self.maxLife = playerData["maxLife"]
        self.coolPoints = playerData["coolPoints"]
        self.coins = playerData["coins"]
        self.xp = playerData["xp"]
        self.trophies = playerData["inventory"]["trophies"]
        self.consumables = playerData["inventory"]["consumables"]

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