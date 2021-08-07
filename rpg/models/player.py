from discord import Member

class Player():

    def __init__(self, rpgCore, member: "Member"):
        self.rpgCore = rpgCore
        self.member = member

    async def GetPlayer(self):
        return await self.rpgCore.config.member(self.member).player()

    async def GetCurrentLife(self) -> int:
        playerData = await self.GetPlayer()
        return playerData["currentLife"]