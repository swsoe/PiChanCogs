from .beanbattle import BeanBattle

async def setup(bot):
    await bot.add_cog(BeanBattle())