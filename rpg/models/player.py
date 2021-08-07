class Player():
    
    def __init__(self, currentLife: int, maxLife: int, coolPoints: int, coins: int, xp: int):
        self.currentLife = currentLife
        self.maxLife = maxLife
        self.coolPoints = coolPoints
        self.coins = coins
        self.xp = xp

    # def __str__(self):
    #     return "HP: {currentLife}/{maxLife} Cool Points: {coolPoints}, Coins: {coins}, XP: {xp}".format(
    #         currentLife = self.currentLife,
    #         maxLife = self.maxLife,
    #         coolPoints = self.coolPoints,
    #         coins = self.coins,
    #         xp = self.xp
    #     )