from redbot.core import commands
from redbot.core import Config
import discord

class Player(commands.Cog):
    """Cog for the framework for a player's individual data. Each user in the Discord server is a "player". """

    def __init__(self):
        self.config = Config.get_conf(self, 677362587088)
        default_user = {
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
        self.config.register_user(**default_user)

        self.requiredXP = [ # The XP required for a particular level, for levels 1 through 30.
            0, 100, 300, 600, 1000, 1500, 2100, 2800, 3600, 4500,
            5500, 6600, 7800, 9100, 10500, 12000, 13600, 15300, 17100, 19000,
            22000, 26000, 31000, 37000, 45000, 54000, 64000, 75000, 87000, 100000 ]

    @commands.command()
    async def stats(self, ctx: commands.context.Context, user: discord.User = None):
        if user is None:
            user = ctx.author
        
        
        data = await self.config.user(user).stats()
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
    async def printstats(self, ctx:commands.context.Context, user:discord.User = None):
        if user is None:
            user = ctx.author
        
        titleString = "{}'s Stat Code".format(str(ctx.author.display_name))
        data = await self.config.user(user).stats()
        e = discord.Embed(title=titleString, description="```"+str(data)+"```")
        await ctx.send(embed=e)

    @commands.command()
    async def iamahumblebeggar(self, ctx:commands.context.Context):
        user = ctx.author

        data = await self.config.user(user).stats()
        coins = data["currentCoins"]

        if coins >= 10:
            return
        else:
            await self.config.user(user).stats.currentCoins.set(10)
            await ctx.send("I spare you a crumb. You now have **10** :coin:.")

    @commands.command()
    async def addxp(self, ctx: commands.context.Context, xp: int):
        try:
            data = await self.config.user(ctx.author).stats()
            data["currentXP"] = data["currentXP"] + xp
            await ctx.send(data["currentXP"])
            await self.config.user(ctx.author).stats.set(data)
        except Exception as e:
            await ctx.send("Unexpected error:"+ str(e))
