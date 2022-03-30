from email.policy import default
from multiprocessing.dummy import Array
from redbot.core import Config
from redbot.core import commands
from redbot.core.utils.chat_formatting import box, pagify
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from typing import List
import discord
import re
import random

class Jukebox(commands.Cog):

    def __init__(self, bot):
        self.config = Config.get_conf(self, 159753258460)
        default_guild = {
            "channelID": "",
            "links": [],
            "userMessageCount": {}
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
            userMessageCount: dict = {}
            regex = "^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
            if channelID is None:
                await ctx.send("Channel is not set")
            else:
                jukeboxChannel = await ctx.bot.fetch_channel(channelID)
                await ctx.send("Parsing messages in : " + jukeboxChannel.name)

                messages = await self.GetMessages(ctx, jukeboxChannel)

                links: List[str] = []
                discard: int = 0
                save: int = 0
                m: discord.Message
                for m in messages:
                    await m.clear_reaction("❌")
                    await m.clear_reaction("✅")

                    if m.content is None:
                        await m.add_reaction("❌")
                        discard += 1
                    else:
                        potentialLinks: List[str] = m.content.split("\n")
                        for p in potentialLinks:
                            if re.search(regex, p) is None or p in links:
                                await m.add_reaction("❌")
                                discard += 1
                            else:
                                match = re.search(regex, p)
                                links.append(match.group(0))
                                await m.add_reaction("✅")
                                save += 1
                                userName = m.author.name
                                if userName in userMessageCount.keys():
                                    userMessageCount[userName] += 1
                                else:
                                    userMessageCount[userName] = 1
                
                await ctx.send("Saved {} messages".format(save))
                await ctx.send("Discarded {} messages".format(discard))
                
                await self.config.guild(ctx.guild).links.set(links)
                await self.config.guild(ctx.guild).userMessageCount.set(userMessageCount)

                await ctx.send("List saved")

        except BaseException as ex:
            await ctx.send(str(ex))

    @commands.command()
    async def GetList(self, ctx: commands.context.Context):
        try:
            savedLinks: List[str] = await self.config.guild(ctx.guild).links()
            await self.pageinateList(ctx, savedLinks)
        except BaseException as ex:
            await ctx.send(str(ex))

    @commands.command()
    async def ClearList(self, ctx: commands.context.Context):
        await self.config.guild(ctx.guild).links.set([])
        await ctx.send("Link list cleared")

    @commands.command()
    async def PlayJukebox(self, ctx: commands.context.Context, queue: int):
        try:
            savedLinks: List[str] = await self.config.guild(ctx.guild).links()
            rolledTracks: List[str] = []
            await ctx.send("Starting jukebox")
            for q in range(queue):
                r: int = random.randint(0, len(savedLinks))
                rolledTracks.append(savedLinks.pop(r))

            for s in rolledTracks:
                await ctx.invoke(ctx.bot.get_command("play"), query=s)
        except BaseException as ex:
            await ctx.send(str(ex))

    @commands.command()
    async def JukeboxStats(self, ctx: commands.context.Context):
        try:
            savedLinks: List[str] = await self.config.guild(ctx.guild).links()
            userMessageCount: dict = await self.config.guild(ctx.guild).userMessageCount()
            await ctx.send("Jukebox stats:")
            await ctx.send("Total tracks: {}".format(len(savedLinks)))
            await ctx.send("Total contributors: {}".format(len(userMessageCount)))
            await ctx.send("Tracks per user:")
            p: tuple
            for k, v in userMessageCount.items():
                await ctx.send("{} : {}".format(k, v))
        except BaseException as ex:
            await ctx.send(str(ex))

    async def GetMessages(self, ctx: commands.context.Context, channel: discord.channel.TextChannel) -> List[discord.Message]:
        try:
            returnList: List[discord.Message] = channel.history(oldest_first=True).flatten()
            tempList: List[discord.Message] = channel.history(oldest_first=True, after=returnList[-1]).flatten()
            await ctx.send("Return list length: {}".format(len(returnList)))
            await ctx.send("Temp list length: {}".format(len(tempList)))
            while len(tempList) == 100:
                returnList.extend(tempList)
                tempList = channel.history(oldest_first=True, after=returnList[-1]).flatten()
            returnList.extend(tempList)
            await ctx.send("Pulled down {} messages".format(len(returnList)))
            return returnList
        except BaseException as ex:
            ctx.send(str(ex))
            

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
