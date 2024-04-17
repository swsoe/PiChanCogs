from redbot.core import commands
from redbot.core import Config
from redbot.core import app_commands
from redbot.core.utils.menus import menu, close_menu
import discord

class Texts():

    fortuneText = app_commands.Group(name="fortune-text", description="Commands for fortune texts")

    @fortuneText.command(name="add")
    @app_commands.describe(text="Add a new fortune text to the list")
    async def text_add(self, interaction: discord.Interaction, text: str):
        ctx = await self.bot.get_context(interaction)

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
    
    @fortuneText.command(name="list")
    async def text_list(self, interaction: discord.Interaction):  
        texts: list = await self.config.guild(interaction.guild).texts()
        await menu(await self.bot.get_context(interaction), texts)

    @fortuneText.command(name="remove")
    @app_commands.describe(index="The index of the fortune text you wish to remove")
    async def text_add(self, interaction: discord.Interaction, index: int):
        texts: list = await self.config.guild(interaction.guild).texts()
        length = len(texts)
        if index.isnumeric() and (index-1) in range(0,length):
            texts.pop(index-1)
            await self.config.guild(interaction.guild).texts.set(texts)
        else:
            await interaction.response.send_message("Please enter a number between 1 and {}".format(str(length)))