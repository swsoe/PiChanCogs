from email.policy import default
from redbot.core import Config
from redbot.core import commands
import discord
import re

class Jukebox(commands.Cog):

    def __init__(self, bot):
        self.config = Config.get_conf(self, 159753258460)
        default_guild = {
            "channelID": "",
            "links": []
        }
        self.config.register_guild(**default_guild)

    @commands.command()
    async def SetChannel(self, ctx: commands.context.Context, channel):
        await self.config.guild(ctx.guild).channelID.set(channel)
        await ctx.send("Channel set to: " + channel)


    @commands.command()
    async def ParseChannel(self, ctx: commands.context.Context):
        try:
            channelID = await self.config.guild(ctx.guild).channelID()
            regex = "^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
            if channelID is None:
                await ctx.send("Channel is not set")
            else:
                jukeboxChannel = await ctx.bot.fetch_channel(channelID)
                await ctx.send("Parsing messages in : " + jukeboxChannel.name)

                messages = await jukeboxChannel.history(limit=10, oldest_first=False).flatten()

                #await ctx.send(messages[-1].content)
                links = []
                m: discord.Message
                for m in messages:
                    if m.content is None or re.search(regex, m.content) is None:
                        await m.add_reaction("❌")
                    else:
                        match = re.search(regex, m.content)
                        links.append(match.group())
                        await m.add_reaction("✅")
                
                await ctx.send(links)
                
        except BaseException as ex:
            await ctx.send(str(ex))
