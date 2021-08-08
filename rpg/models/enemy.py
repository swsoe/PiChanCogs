import random

class Enemy():
    def __init__(self):
        # Turn an upper and lower bound of coin drops into a range of coin integers (example: [5, 9] to [5, 6, 7, 8, 9])
        if len(self.coins) == 2 and self.coinsIsRange == True:
            self.coins = list(range[self.coins[0], self.coins[1]+1])
    
    def GetName(self) -> str:
        return self.name

    def GetBasicAttacks(self) -> list:
        return self.attacks

    def GetDesperationAttacks(self) -> list:
        return self.desperationAttacks

    def GetCurrentLife(self) -> int:
        return self.currentLife

    def GetCurrentHealth(self) -> int:
        return self.currentHealth

    def GetTotalHealth(self) -> int:
        return self.totalHealth

    def GetDamage(self) -> int:
        return self.damage

    def GetXP(self) -> int:
        return self.xp

    # Returns the entire list of possible coin payouts
    def GetCoins(self) -> list:
        return self.coins

    # Returns a single value, randomly determined from the available coin payouts
    def GetRandomCoins(self) -> int:
        return random.choose(self.GetCoins())

    # TODO: Functions for random attacks:
    # - determining if desperation attack procs,
    # - fetching one of the attack strings (if multiple)
    # - getting a random damage value (if valid)
    # - returning it as a dictionary (or maybe an Attack-class object?)
