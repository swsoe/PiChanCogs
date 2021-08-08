from redbot.core import commands
from redbot.core import Config
from .models.player import Player
import discord
import random

from .utils import Utils

class RPG(commands.Cog):
    def __init__(self):
        self.config = Config.get_conf(self, 677362587088)
        default_member = {
            "player": {
                "currentLife": 100,
                "maxLife": 100,
                "coolPoints": 0,
                "coins": 0,
                "xp": 0,
                "inventory": {
                    "trophies": {},
                    "consumables": {}
                }
            }
        }

        self.config.register_member(**default_member)

    @commands.command()
    async def stats(self, ctx: commands.context.Context, member: discord.Member = None):
        try:
            if member is None:
                member = ctx.author
            
            player = Player(await self.config.member(member).player())
            statLines = [
                "Life Points: **{}** / **{}**".format(player.GetCurrentLife(), player.GetMaxLife()),
                "Cool Points: **{}**".format(player.GetCoolPoints()),
                "", # Compulsory blank line
                "**{}** XP".format(player.GetXP()),
                "",
                "**{}** :coin:".format(player.GetCoins())
            ]

            titleString = ":trophy: {}'s Statistics :bar_chart:".format(str(ctx.author.display_name))
            descriptionString = "\n".join(statLines)
            
            e = discord.Embed(title=titleString, description=descriptionString)
            await ctx.send(embed=e)
        except Exception as e:
            await ctx.send("Unexpected error:"+ str(e))

    @commands.command()
    async def printstats(self, ctx:commands.context.Context, member:discord.Member = None):
        try:
            if member is None:
                member = ctx.author
            
            titleString = "{}'s Stat Code".format(str(ctx.author.display_name))
            player = await self.config.member(member).player()
            e = discord.Embed(title=titleString, description="```"+str(player)+"```")
            await ctx.send(embed=e)
        except Exception as e:
            await ctx.send("Unexpected error:"+ str(e))

    @commands.command(aliases=["beg"])
    async def iamahumblebeggar(self, ctx:commands.context.Context):
        try:
            member = ctx.author

            player = Player(await self.config.member(member).player())
            coins = player.GetCoins()

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
                player.AddCoins(10)
                await self.config.member(member).player.set(player.ToDictionary())
                randNum = random.randint(0, len(beggarStrings)-1)
                await ctx.send("{} You now have **10** :coin:.".format(beggarStrings[randNum]))
        except Exception as e:
            await ctx.send("Unexpected error:"+ str(e))

    @commands.command()
    async def bankruptme(self, ctx:commands.context.Context):
        try:
            member = ctx.author
            player = Player(await self.config.member(member).player())

            bankruptStrings = [
                "A hungry ~~bean~~ nature spirit answers your call and consumes your funds!",
                "You throw your coin purse into the nearest river.",
                "With great might, you crush your coin purse in the palm of your hand.",
                "You suddenly discover your money has been replaced with play money."
            ]
            
            randNum = random.randint(0, len(bankruptStrings)-1)
            player.SetCoins(0)
            await self.config.member(member).player.set(player.ToDictionary())
            await ctx.send("{} You now have **0** :coin:.".format(bankruptStrings[randNum]))
        except Exception as e:
            await ctx.send("Unexpected error:"+ str(e))

    @commands.command()
    async def addxp(self, ctx: commands.context.Context, xp: int):
            player = await self.config.member(ctx.author).player()
            player.xp += xp
            await ctx.send(player.xp)
            await self.config.member(ctx.author).player.set(player)

    @commands.command()
    async def rolecheck(self, ctx: commands.context.Context, member: discord.Member, role: str):
        try:
            output = await Utils.MemberHasRole(member, role)
            await ctx.send(str(output))
        except Exception as e:
            await ctx.send("Unexpected error:"+ str(e))

    @commands.command()
    async def testModel(self, ctx: commands.context.Context):
        try:
            p = Player(self, ctx.author)
            await ctx.send("Current life:" + str(await p.GetCurrentLife()))
        except Exception as e:
            await ctx.send("Unexpected error:"+ str(e))