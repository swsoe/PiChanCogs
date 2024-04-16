from redbot.core import commands
from redbot.core import app_commands
from redbot.core import Config
from redbot.core.utils.chat_formatting import box, pagify
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core.data_manager import cog_data_path
from typing import List
from . import texts
import discord
import random

class Fortunes(texts.Texts, commands.Cog):
    """Fortunes Cog - Generates random foruntes (image plus text) based on user entered data"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 159753258457)
        default_guild = {
            "texts": [],
            "pics": [],
            "fileTypes": [".jpg", "jpeg", ".png", ".gif", "gifv"],
            "textBag": [],
            "picBag": []
        }
        self.config.register_guild(**default_guild)

    fortune = app_commands.Group(name="fortune", description="Fortune related commands")

    @app_commands.command(name="cookie", description="Generate a new fortune")
    async def cookie(self, interaction: discord.Interaction):
        textBag: list = await self.config.guild(interaction.guild).textBag()
        picBag: list = await self.config.guild(interaction.guild).picBag()
        
        if len(textBag) == 0:
            "refill textBag"
            textBag = await self.RefillTextBag(interaction)

        if len(picBag) == 0:
            "refill picBag"
            picBag = await self.RefillPicBag(interaction)

        titles = [ "{} - Confucius Say", "{}'s Daily Dose of Wisdom", "{}'s Bequeathed Knowledge", "{} Assigned Brain Nectar", "Our:tm: Family-friendly Message to {}", "Tip of the Day for {}", "{}'s Pro-tip" ]
        titleString = "{}'s Fortune".format(str(interaction.author.display_name))
        
        if random.randint(1, 4) == 4:
            tnum = random.randint(0, len(titles) - 1)
            titleString = titles[tnum].format(str(interaction.author.display_name))
        
        textBagIndex: int = random.randint(0, len(textBag) - 1)
        textsIndex: int = textBag.pop(textBagIndex)
        
        picBagIndex: int = random.randint(0, len(picBag) - 1)
        picsIndex: int = picBag.pop(picBagIndex)

        texts: list = await self.config.guild(interaction.guild).texts()
        pics: list = await self.config.guild(interaction.guild).pics()

        e = discord.Embed(title=titleString, description=texts[textsIndex]).set_image(url=pics[picsIndex])
        
        await self.config.guild(interaction.guild).textBag.set(textBag)
        await self.config.guild(interaction.guild).picBag.set(picBag)
        
        await interaction.send(embed=e)

    async def RefillPicBag(self, interaction: commands.context.Context):
        pics: list = await self.config.guild(interaction.guild).pics()
        picBag: list = []

        for index in range(len(pics)):
            picBag.append(index)

        await self.config.guild(interaction.guild).picBag.set(picBag)

        return picBag

    async def RefillTextBag(self, interaction: commands.context.Context):
        texts: list = await self.config.guild(interaction.guild).texts()
        textBag: list = []

        for index in range(len(texts)):
            textBag.append(index)

        await self.config.guild(interaction.guild).textBag.set(textBag)

        return textBag