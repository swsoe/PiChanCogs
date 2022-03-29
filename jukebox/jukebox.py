from email.policy import default
from redbot.core import Config
from redbot.core import commands
import discord

class Jukebox(commands.Cog):

    def __init__(self, bot):
        self.config = Config.get_conf(self, 159753258460)
        default_guild = {
            "channelID": ""
        }
        self.config.register_guild(**default_guild)

    @commands.command()
    async def SetChannel(self, ctx: commands.context.Context, channel):
        await self.config.guild(ctx.guild).channelID.set(channel)
        await ctx.send("Channel set to: " + channel)


    @commands.command()
    async def ParseChannel(self, ctx: commands.context.Context):
        try:
            channelID = self.config.guild(ctx.guild).channelID()
            if channelID is None:
                await ctx.send("Channel is not set")
            else:
                ctx.channel
                jukeboxChannel = await ctx.bot.fetch_channel(channelID)
                await ctx.send(jukeboxChannel.type)
        except BaseException as ex:
            await ctx.send(str(ex))
