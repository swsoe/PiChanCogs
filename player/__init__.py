from .player import Player

async def setup(bot):
    await bot.add_cog(Player())