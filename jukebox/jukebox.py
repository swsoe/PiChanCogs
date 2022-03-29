from email.policy import default
from multiprocessing.dummy import Array
from redbot.core import Config
from redbot.core import commands
from redbot.core.utils.chat_formatting import box, pagify
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from typing import List
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

                messages = await jukeboxChannel.history(oldest_first=True).flatten()

                #await ctx.send(messages[-1].content)
                links = []
                discard: int = 0
                save: int = 0
                m: discord.Message
                for m in messages:
                    if m.content is None or re.search(regex, m.content) is None:
                        await m.add_reaction("❌")
                        discard += 1
                    else:
                        match = re.search(regex, m.content)
                        links.append(match.group())
                        await m.add_reaction("✅")
                        save += 1
                
                await ctx.send("Saved {} messages".format(save))
                await ctx.send("Discarded {} messages".format(discard))
                
                savedLinks: Array = await self.config.guild(ctx.guild).links()
                savedLinks.append(links)
                await self.config.guild(ctx.guild).links.set(savedLinks)

                await ctx.send("List saved")

        except BaseException as ex:
            await ctx.send(str(ex))

    @commands.command()
    async def GetList(self, ctx: commands.context.Context):
        savedLinks: Array = await self.config.guild(ctx.guild).links()
        await self.pageinateList(ctx, savedLinks)

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
