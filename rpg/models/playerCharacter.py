from json import JSONEncoder

class PlayerCharacter(JSONEncoder):
    
    def default(self, o):   
            return o.__dict__

    def __init__(self, currentLife: int, maxLife: int, coolPoints: int, coins: int, xp: int):
        self.currentLife = currentLife
        self.maxLife = maxLife
        self.coolPoints = coolPoints
        self.coins = coins
        self.xp = xp