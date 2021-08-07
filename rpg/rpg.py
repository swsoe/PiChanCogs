from redbot.core import commands
from redbot.core import Config
from models.player import Player
import discord
import random

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

        default_user = {
            "player" : Player(100, 100, 0, 0, 0)
        } 

        self.config.register_member(**default_member)
        self.config.register_user(**default_user)

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

    @commands.command(aliases=["beg"])
    async def iamahumblebeggar(self, ctx:commands.context.Context):
        member = ctx.author

        data = await self.config.member(member).stats()
        coins = data["currentCoins"]

        beggarStrings = [
            "\"I spare you a crumb.\"",
            "\"A tuppence for you, my boy!\"",
            "\"Keep your distance, filth!\" A man you approach throws some money at you before briskly walking away!",
            "You encounter a dead bourgeois on the side of the road and decide to feast on his flesh."
        ]

        nopeStrings = [
            "You must be **THIS POOR** to receive this handout.",
            "Not so fast, greedyguts.",
            "You've got *pleeenty* of money already.",
            "Did you forget your wallet at home or something?"
        ]

        if coins >= 10:
            randNum = random.randint(0, len(nopeStrings)-1)
            await ctx.send("{} You must have fewer than **10** :coin: to humbly beg.".format(nopeStrings[randNum]))
        else:
            await self.config.member(member).stats.currentCoins.set(10)
            randNum = random.randint(0, len(beggarStrings)-1)
            await ctx.send("{} You now have **10** :coin:.".format(beggarStrings[randNum]))

    @commands.command()
    async def bankruptme(self, ctx:commands.context.Context):
        member = ctx.author
        data = await self.config.member(member).stats()

        bankruptStrings = [
            "A hungry ~~bean~~ nature spirit answers your call and consumes your funds!",
            "You throw your coin purse into the nearest river.",
            "With great might, you crush your coin purse in the palm of your hand.",
            "You suddenly discover your money has been replaced with play money."
        ]
        
        randNum = random.randint(0, len(bankruptStrings)-1)
        await self.config.member(member).stats.currentCoins.set(0)
        await ctx.send("{} You now have **0** :coin:.".format(bankruptStrings[randNum]))

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

    @commands.command()
    async def printuserstats(self, ctx: commands.context.Context):
        try:
            player = await self.config.user(ctx.author).player
            await ctx.send(player.currentLife)
        except Exception as e:
            await ctx.send("Unexpected error:"+ str(e))