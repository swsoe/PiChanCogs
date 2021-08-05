from redbot.core import commands
from redbot.core import Config
import discord

from .utils import Utils

class RPG(commands.Cog):
    def __init__(self):
        self.config = Config.get_conf(self, 677362587088)
        default_member = {
            "stats": {
                "currentLife": 100,
                "maxLife": 100,
                "currentCool": 0,
                "currentCoins": 0,
                "currentXP": 0,
                "inventory": {
                    "trophies": {},
                    "consumables": {}
                }
            }
        }
        self.config.register_member(**default_member)

    @commands.command()
    async def stats(self, ctx: commands.context.Context, member: discord.Member = None):
        if member is None:
            member = ctx.author
        
        data = await self.config.member(member).stats()
        statLines = [
            "Life Points: **{}** / **{}**".format(data["currentLife"], data["maxLife"]),
            "Cool Points: **{}**".format(data["currentCool"]),
            "", # Compulsory blank line
            "**{}** XP".format(data["currentXP"]),
            "",
            "**{}** :coin:".format(data["currentCoins"])
        ]

        titleString = ":trophy: {}'s Statistics :bar_chart:".format(str(ctx.author.display_name))
        descriptionString = "\n".join(statLines)
        
        e = discord.Embed(title=titleString, description=descriptionString)
        await ctx.send(embed=e)

    @commands.command()
    async def printstats(self, ctx:commands.context.Context, member:discord.Member = None):
        if member is None:
            member = ctx.author
        
        titleString = "{}'s Stat Code".format(str(ctx.author.display_name))
        data = await self.config.member(member).stats()
        e = discord.Embed(title=titleString, description="```"+str(data)+"```")
        await ctx.send(embed=e)

    @commands.command()
    async def iamahumblebeggar(self, ctx:commands.context.Context):
        member = ctx.author

        data = await self.config.member(member).stats()
        coins = data["currentCoins"]

        if coins >= 10:
            return
        else:
            await self.config.member(member).stats.currentCoins.set(10)
            await ctx.send("I spare you a crumb. You now have **10** :coin:.")

    @commands.command()
    async def addxp(self, ctx: commands.context.Context, xp: int):
        try:
            data = await self.config.member(ctx.author).stats()
            data["currentXP"] = data["currentXP"] + xp
            await ctx.send(data["currentXP"])
            await self.config.member(ctx.author).stats.set(data)
        except Exception as e:
            await ctx.send("Unexpected error:"+ str(e))

    @commands.command()
    async def rolecheck(self, ctx: commands.context.Context, member: discord.Member, role: str):
        try:
            output = await Utils.MemberHasRole(member, role)
            await ctx.send(str(output))
        except Exception as e:
            await ctx.send("Unexpected error:"+ str(e))