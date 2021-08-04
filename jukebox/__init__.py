from .jukebox import Jukebox


def setup(bot):
    bot.add_cog(Jukebox(bot))