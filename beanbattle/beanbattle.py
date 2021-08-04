from redbot.core import commands
from redbot.cogs import audio
from redbot.core import Config
from redbot.core.utils.chat_formatting import box, pagify
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core.data_manager import cog_data_path
from typing import List
import discord
import random
from .beanlibrary import BeanLibrary

class BeanBattle(commands.Cog):
    "Bean Battle Cog"

    @commands.command()
    async def battle(self, ctx: commands.context.Context):
        """Command description here"""
        returnEmbed = discord.Embed(title="Bean Battle")
        
        beanList = BeanLibrary.GetBeans()
        beanIndex = random.randint(0,len(beanList)-1)
        beanSelected = beanList[beanIndex]
        
        attackRoll = random.randint(1,20)
        
        battleStart = ":crossed_swords: {userName} encounters the {beanName} Bean!\n".format(
            userName=ctx.author.display_name,
            beanName=beanSelected.name
        )

        attack = ":game_die: {userName} attacks and rolls a {roll}".format(
            userName=ctx.author.display_name,
            roll=str(attackRoll)
        )
        
        outcome = ""
        if attackRoll >= beanSelected.ac:
            outcome = ":crossed_swords: {userName} deals {damage} damage! The {beanName} is defeated!\n :sparkles: **VICTORY** :sparkles:".format(
                userName=ctx.author.display_name,
                damage=str(max(1, attackRoll-beanSelected.ac)),
                beanName=beanSelected.name
            )
        else:
            outcome = await self.GetLossMessage(ctx.author.display_name, beanSelected.name, ctx)

        returnEmbed.add_field(name="---",value=battleStart,inline=False)
        returnEmbed.add_field(name="---",value=attack,inline=False)
        returnEmbed.add_field(name="---",value=outcome,inline=False)
        returnEmbed.color = discord.Color.from_rgb(
            beanSelected.color[0],
            beanSelected.color[1],
            beanSelected.color[2]
        )
        returnEmbed.set_image(url="https://cdn.discordapp.com/attachments/872495284574388286/872495612644425738/killbean.gif")
        await ctx.send(embed=returnEmbed)

    async def GetLossMessage(self, user: str, bean: str, ctx) -> str:
        messages = BeanLibrary.GetDefeatedMessage()
        messageIndex = random.randint(0,len(messages)-1)
        if messageIndex == 0:
            channel = ctx.guild.get_channel(674052950620110859)
            await ctx.author.move_to(channel)
        return messages[messageIndex].format(
            userName=user,
            beanName=bean
        )
