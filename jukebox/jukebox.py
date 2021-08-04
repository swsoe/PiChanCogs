from typing import ContextManager
from redbot.core import commands
import discord

class Jukebox(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mycom(self, ctx: commands.context.Context):
        ctx.send()
        await ctx.send("I can do stuff!")