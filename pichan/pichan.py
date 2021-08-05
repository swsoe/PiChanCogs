from redbot.core import commands
from redbot.cogs import audio
from redbot.core import Config
from redbot.core.utils.chat_formatting import box, pagify
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core.data_manager import cog_data_path
from typing import List
import discord
import random

class PiChan(commands.Cog):
    """Testing Cog"""
    
    def __init__(self):
        self.config = Config.get_conf(self, 159753258456)
        default_global = {
            "fortunes": [],
            "fortunePics": [],
            "fileTypes": [".jpg", "jpeg", ".png", ".gif", "gifv"],
            "lastFortune": 0,
            "lastPic": 0
        }
        self.config.register_global(**default_global)

    @commands.command()
    async def weebitup(self, ctx: commands.context.Context):
        """This might do stuff"""
        await ctx.send("Nya! :3")
        
    @commands.command()
    async def pichan(self, ctx: commands.context.Context):
        await ctx.send("Hi! I'm PiChan!")
        
    @commands.command()
    async def avatar(self, ctx: commands.context.Context, user: discord.Member = None):
        if user is None:
            user = ctx.me
        await ctx.send("https://cdn.discordapp.com/avatars/"+str(user.id)+"/"+str(user.avatar)+".png?size=512")
        
    @commands.command()
    async def cafe(self, ctx: commands.context.Context):
        await audio.play(self, ctx, query='https://www.youtube.com/watch?v=D6KRIMASing')

    @commands.command()
    async def fortunecookie(self, ctx: commands.context.Context):
        f = await self.config.fortunes()
        p = await self.config.fortunePics()
        titles = [ "{} - Confucius Say", "{}'s Daily Dose of Wisdom", "{}'s Bequeathed Knowledge", "{} Assigned Brain Nectar", "Our:tm: Family-friendly Message to {}", "Tip of the Day for {}", "{}'s Pro-tip" ]
        titleString = "{}'s Fortune".format(str(ctx.author.display_name))
        if random.randint(1, 4) == 4:
            tnum = random.randint(0, len(titles) - 1)
            titleString = titles[tnum].format(str(ctx.author.display_name))
        fnum = random.randint(0, len(f) - 1)
        pnum = random.randint(0, len(p) - 1)
        lastfnum = await self.config.lastFortune()
        lastpnum = await self.config.lastPic()
        while fnum == lastfnum:
            fnum = random.randint(0, len(f) - 1)
        while pnum == lastpnum:
            pnum = random.randint(0, len(p) - 1)
        e = discord.Embed(title=titleString, description=f[fnum]).set_image(url=p[pnum])
        await self.config.lastFortune.set(fnum)
        await self.config.lastPic.set(pnum)
        await ctx.send(embed=e)
    
    @commands.command()
    async def fortuneadd(self, ctx: commands.context.Context, fortune: str):
        await ctx.send("Fortune specified: " + fortune)
        f = await self.config.fortunes()
        if fortune is None or fortune == "":
            await ctx.send("Please enter a fortune")
        elif fortune in f:
            await ctx.send("Fortune already present")
        else:
            f.append(fortune)
            await self.config.fortunes.set(f)
            await ctx.send("Fortune added")


    @commands.command()
    async def fortunepicadd(self, ctx: commands.context.Context, pic):
        await ctx.send("Picture specified: ")
        await ctx.send(pic)
        p = await self.config.fortunePics()
        fileTypes = await self.config.fileTypes()
        lastFour = pic[-4:]
        if pic is None or pic == "":
            await ctx.send("Please enter a picture link")
        elif pic in p:
            await ctx.send("Picture already present")
        elif lastFour.upper() not in (fileType.upper() for fileType in fileTypes):
            await ctx.send("Picture link not of supported type")
        else:
            p.append(pic)
            await self.config.fortunePics.set(p)
            await ctx.send("Picture link added")

    @commands.command()
    async def fortunelist(self, ctx: commands.context.Context):
        f = await self.config.fortunes()
        p = await self.config.fortunePics()
        await self.pageinateList(ctx, f)
        await self.pageinateList(ctx, p)

    @commands.command()
    async def fortunesclear(self, ctx: commands.context.Context):
        await self.config.fortunes.set([])
        await ctx.send("Fortune list clear")

    @commands.command()
    async def fortunepicsclear(self, ctx: commands.context.Context):
        await self.config.fortunePics.set([])
        await ctx.send("Fortune pic list clear")

    @commands.command()
    async def fortuneremove(self, ctx: commands.context.Context, item: int):
        f = await self.config.fortunes()
        try:
            i = int(item) - 1
            fortune = f[i]
            del f[i]
            await self.config.fortunes.set(f)
            await ctx.send("Fortune '" + fortune + "' removed.")
        except:
            await ctx.send("Item number must be present in list of fortunes")

    @commands.command()
    async def fortunepicremove(self, ctx: commands.context.Context, item: int):
        p = await self.config.fortunePics()
        try:
            i = int(item) - 1
            fortunePic = p[i]
            del p[i]
            await self.config.fortunePics.set(p)
            await ctx.send("Fortune '" + fortunePic + "' removed.")
        except:
            await ctx.send("Item number must be present in list of fortunes")

    async def pageinateList(self, ctx: commands.context.Context, items: List[str]):
        for x in range(len(items)):
            items[x] = str(x+1) + " " + items[x]
        message = "\n".join(items)
        temp = list(pagify(message, delims=["\n"], page_length=1850))
        item_list = []
        count = 0
        for page in temp:
            count += 1
            page = page.lstrip("\n")
            page = (
                ("Items:\n")
                + page
                + ("\n\nPage {page}/{total}").format(page=count, total=len(temp))
            )
            item_list.append(box("".join(page), "diff"))
        if len(item_list) == 1:
            await ctx.send(item_list[0])
            return
        await menu(ctx, item_list, DEFAULT_CONTROLS)

    """Returns whether a user has a given role. The 'role' argument can either be the role as an object, or the exact name of the role."""
    async def UserHasRole(self, user : discord.User, role):
        ctx = commands.context.Context

        if isinstance(role, str):
            role = discord.utils.get(ctx.guild.roles, name=role)
        if role is None:
            print("The given role does not exist, returning false!")
            return False
        else:
            member = ctx.guild.fetchMember(user.id)
            roles = member.roles
            for i in roles:
                if i.id == role.id:
                    return True
            return False

    @commands.command()
    async def rolecheck(self, ctx: commands.context.Context, user: discord.Member, role: str):
        output = await self.UserHasRole(user, role)
        await ctx.send(str(output))