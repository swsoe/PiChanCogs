from .redrog import RedRog

async def setup(bot):
    await bot.add_cog(RedRog())