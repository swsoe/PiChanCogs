from redbot.core import commands
from redbot.core import Config
from redbot.core import app_commands
from redbot.core.utils.chat_formatting import box, pagify
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS, close_menu
import discord

class Pics():

    fortunePic = app_commands.Group(name="fortune-pic", description="Commands for fortune pics")

    @fortunePic.command(name="add", description="Add a pic link to the list")
    async def pic_add(self, interaction: discord.Interaction, picLink: str):
        ctx = await self.bot.get_context(interaction)
        try:
            pics: list = await self.config.guild(ctx.guild).pics()
            fileTypes: list = await self.config.guild(ctx.guild).fileTypes()
            
            lastFour = picLink[-4:]
            if picLink is None or picLink == "":
                await ctx.send("Please enter a picture link")
            elif picLink in pics:
                await ctx.send("Picture already present")
            elif lastFour.upper() not in (fileType.upper() for fileType in fileTypes):
                await ctx.send("Picture link not of supported type")
            else:
                async def control_yes(ctx, pages, controls, message, page, timeout, emoji):
                    await close_menu(ctx, pages, controls, message, page, timeout, emoji)
                    return True

                async def control_no(ctx, pages, controls, message, page, timeout, emoji):
                    await close_menu(ctx, pages, controls, message, page, timeout, emoji)
                    return False

                controls = {
                    "\N{WHITE HEAVY CHECK MARK}": control_yes,
                    "\N{CROSS MARK}": control_no,
                }
                reply = await menu(ctx, ["Add this fortune pic? '{}'".format(picLink)], controls)

                if reply:
                    pics.append(picLink)
                    await self.config.guild(ctx.guild).pics.set(pics)
                    await ctx.send("Fortune pic added")
                    return
                else:
                    await ctx.send("Got cold feet on that one huh?")
                    return
        except BaseException as ex:
            await ctx.send(str(ex))
    
    @fortunePic.command(name="list", description="Display all pic links currently saved")
    async def pic_list(self, interaction: discord.Interaction):  
        ctx = await self.bot.get_context(interaction)
        try:
            pics: list = await self.config.guild(interaction.guild).pics()
            await self.pageinateList(ctx, pics)
        except BaseException as ex:
            await ctx.send(str(ex))


    @fortunePic.command(name="remove", description="Remove a pic link")
    async def pic_remove(self, interaction: discord.Interaction, index: int):
        ctx = await self.bot.get_context(interaction)
        try:
            pics: list = await self.config.guild(interaction.guild).pics()
            length = len(pics)
            if (index-1) in range(0,length):
                removedPic: str = pics.pop(index-1)
                await self.config.guild(interaction.guild).pics.set(pics)
                await ctx.send("Fortune pic removed: " + removedPic)
            else:
                await interaction.response.send_message("Please enter a number between 1 and {}".format(str(length)))
        except BaseException as ex:
            await ctx.send(str(ex))

    
    async def pageinateList(self, ctx: commands.context.Context, items: list[str]):
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