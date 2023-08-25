from .pichan import PiChan

async def setup(bot):
    await bot.add_cog(PiChan())