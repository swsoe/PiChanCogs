from redbot.core import commands
from redbot.core import Config
from redbot.core import app_commands
from redbot.core.utils.chat_formatting import box, pagify
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS, close_menu
import discord

class Texts():

    fortuneText = app_commands.Group(name="fortune-text", description="Commands for fortune texts")

    @fortuneText.command(name="add")
    @app_commands.describe(text="Add a new fortune text to the list")
    async def text_add(self, interaction: discord.Interaction, text: str):
        ctx = await self.bot.get_context(interaction)
        try:
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
            reply = await menu(ctx, ["Add this fortune? '{}'".format(text)], controls)

            if reply:
                texts: list = await self.config.guild(ctx.guild).texts()
                texts.append(text)
                await self.config.guild(ctx.guild).texts.set(texts)
                await ctx.send("Fortune text added")
                return
            else:
                await ctx.send("Got cold feet on that one huh?")
                return
        except BaseException as ex:
            await ctx.send(str(ex))
    
    @fortuneText.command(name="list")
    async def text_list(self, interaction: discord.Interaction):  
        ctx = await self.bot.get_context(interaction)
        try:
            texts: list = await self.config.guild(interaction.guild).texts()
            await self.pageinateList(ctx, texts)
        except BaseException as ex:
            await ctx.send(str(ex))


    @fortuneText.command(name="remove")
    @app_commands.describe(index="The index of the fortune text you wish to remove")
    async def text_add(self, interaction: discord.Interaction, index: int):
        ctx = await self.bot.get_context(interaction)
        try:
            texts: list = await self.config.guild(interaction.guild).texts()
            length = len(texts)
            if index.isnumeric() and (index-1) in range(0,length):
                texts.pop(index-1)
                await self.config.guild(interaction.guild).texts.set(texts)
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