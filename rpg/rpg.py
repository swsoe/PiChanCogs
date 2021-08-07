from redbot.core import commands
from redbot.core import Config
from .models.playerCharacter import PlayerCharacter
import discord
import random

from .utils import Utils

class RPG(commands.Cog):
    def __init__(self):
        self.config = Config.get_conf(self, 677362587088)
        defaultPlayer = PlayerCharacter(100, 100, 0, 0, 0)
        default_member = {
            "playerContainer" : defaultPlayer
        }

        self.config.register_member(**default_member)

    @commands.command()
    async def stats(self, ctx: commands.context.Context, member: discord.Member = None):
        try:
            if member is None:
                member = ctx.author
            
            player = await self.config.member(member).playerContainer()
            statLines = [
                "Life Points: **{}** / **{}**".format(player.currentLife, player.maxLife),
                "Cool Points: **{}**".format(player.coolPoints),
                "", # Compulsory blank line
                "**{}** XP".format(player.xp),
                "",
                "**{}** :coin:".format(player.coins)
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
            player = await self.config.member(member).playerContainer()
            e = discord.Embed(title=titleString, description="```"+str(player)+"```")
            await ctx.send(embed=e)
        except Exception as e:
            await ctx.send("Unexpected error:"+ str(e))

    @commands.command(aliases=["beg"])
    async def iamahumblebeggar(self, ctx:commands.context.Context):
        try:
            member = ctx.author

            player: PlayerCharacter = await self.config.member(member).playerContainer()
            coins = player.coins

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
                player.coins += 10
                await self.config.member(member).playerContainer.set(player)
                randNum = random.randint(0, len(beggarStrings)-1)
                await ctx.send("{} You now have **10** :coin:.".format(beggarStrings[randNum]))
        except Exception as e:
            await ctx.send("Unexpected error:"+ str(e))

    @commands.command()
    async def bankruptme(self, ctx:commands.context.Context):
        try:
            member = ctx.author
            player: PlayerCharacter = await self.config.member(member).playerContainer()

            bankruptStrings = [
                "A hungry ~~bean~~ nature spirit answers your call and consumes your funds!",
                "You throw your coin purse into the nearest river.",
                "With great might, you crush your coin purse in the palm of your hand.",
                "You suddenly discover your money has been replaced with play money."
            ]
            
            randNum = random.randint(0, len(bankruptStrings)-1)
            player.coins = 0
            await self.config.member(member).playerContainer.set(player)
            await ctx.send("{} You now have **0** :coin:.".format(bankruptStrings[randNum]))
        except Exception as e:
            await ctx.send("Unexpected error:"+ str(e))

    @commands.command()
    async def addxp(self, ctx: commands.context.Context, xp: int):
            player: PlayerCharacter = await self.config.member(ctx.author).playerContainer()
            player.xp += xp
            await ctx.send(player.xp)
            await self.config.member(ctx.author).playerContainer.set(player)

    @commands.command()
    async def rolecheck(self, ctx: commands.context.Context, member: discord.Member, role: str):
        try:
            output = await Utils.MemberHasRole(member, role)
            await ctx.send(str(output))
        except Exception as e:
            await ctx.send("Unexpected error:"+ str(e))

    @commands.command()
    async def printtest(self, ctx: commands.context.Context):
        print("test")