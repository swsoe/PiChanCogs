from .fortunes import Fortunes

async def setup(bot):
    await bot.add_cog(Fortunes())