from redbot.core import commands
from redbot.cogs import audio
from redbot.core import Config
from redbot.core.utils.chat_formatting import box, pagify
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from typing import List
import discord
import random
from random import choice
import re
from redbot.core.utils.chat_formatting import (
    bold,
    escape,
    italics,
    humanize_number,
    humanize_timedelta,
)

class RedRog(commands.Cog):
    """The Red Cog"""

    @commands.command(usage="<first> <second> [others...]")
    async def choose(self, ctx, *choices):
        """Choose between multiple options.
        There must be at least 2 options to pick from.
        Options are separated by spaces.
        To denote options which include whitespace, you should enclose the options in double quotes.
        """
        choices = [escape(c, mass_mentions=True) for c in choices if c]
        if len(choices) < 2:
            await ctx.send(("Not enough options to pick from."))
        else:
            await ctx.send(choice(choices))
    
    @commands.command(pass_context=True)
    async def roll(self, ctx, inputString = ""):
        """Rolls random number (between 1 and user choice)
 
        Defaults to 100.
 
        To roll and sum multiple dice at once, type #d# and any modifiers you want after it
        Ex: roll 5d6 + 5 - 8 will roll 5 six-sided dice, add 5 to the result, and subtract 7 from that
        Supports +, -, *, /, and modulo modifiers
        """
        author = ctx.author
        #format content to accept spaces
        if len(ctx.message.content) > 5:
            inputString = ctx.message.content[5:]
            while inputString[0] is ' ':
                inputString = inputString[1:]
 
        #standard roll 100 if they just roll
        if len(inputString) is 0:
            n = str(random.randint(1, 100))
            return await ctx.send("{} :game_die: {} :game_die:".format(author.mention, n))
        else:
            allNums = list(map(int, re.findall(r'\d+', inputString)))
            if len(allNums) is 0:
                n = str(random.randint(1, 100))
                return await ctx.send("{} You didn't put any numbers so I'm going to just roll 100 :game_die: {} :game_die:".format(author.mention, n))
            elif len(allNums) is 1:
                n = str(random.randint(1, allNums[0]))
                return await ctx.send("{} :game_die: {} :game_die:".format(author.mention, n))
            else:
                #get each component of the command to parse accordingly
                components = []
                while len(inputString) > 0:
                    if inputString[0].isdigit():
                        n = list(map(int, re.findall(r'\d+', inputString)))[0]
                        components.append(n)
                        inputString = inputString[len(str(n)):]
                    elif inputString[0] in ['d','+','-','*','/','%']:
                        components += inputString[0]
                        inputString = inputString[1:]
                    else:
                        inputString = inputString[1:]
 
                results = ""
                total = 0
                # edge case: if they chose to not say d but still want to do math, roll the first number
                if 'd' not in components:
                    if isinstance(components[0], int ):
                        if components[0] < 1:
                            return await self.bot.say("{} Can't roll less than 1, that's not how dice work".format(author.mention))
                        n = random.randint(1, components[0])
                        results += str(n)
                        total += n
                for i in range(0, len(components)):
                    if components[i] is 'd':
                        numrolls = 1
                        diesize = 100
                        if i is not 0 and isinstance(components[i-1], int ):
                            numrolls = components[i-1]
                        if i + 1 < len(components) and isinstance(components[i+1], int ):
                            diesize = components[i+1]
                        else:
                            return await self.bot.say("Cannot roll; number of sides not specified (<number of dice>d<number of sides>)")
                       
                        for j in range(0, numrolls):
                            n = random.randint(1, diesize)
                            total += n;
                            results += str(n)
                            if j is not numrolls - 1:
                                results += " + "
                            elif numrolls is not 1:
                                results += " = " + str(total)
 
                    elif components[i] is'+':
                        if i + 1 < len(components) and isinstance(components[i+1], int ):
                            results += " + {} = {}".format(str(components[i+1]), str(total + components[i+1]))
                            total += components[i+1]
                        else:
                            return await ctx.send("Cannot roll; no number to add after +")
                    elif components[i] is'-':
                        if i + 1 < len(components) and isinstance(components[i+1], int ):
                            results += " - {} = {}".format(str(components[i+1]), str(total - components[i+1]))
                            total -= components[i+1]
                        else:
                            return await ctx.send("Cannot roll; no number to subtract with after -")
                    elif components[i] is'*':
                        if i + 1 < len(components) and isinstance(components[i+1], int ):
                            results += " * {} = {}".format(str(components[i+1]), str(total * components[i+1]))
                            total *= components[i+1]
                        else:
                            return await ctx.send("Cannot roll; no number to multiply by after *")
                    elif components[i] is'/':
                        if i + 1 < len(components) and isinstance(components[i+1], int ):
                            results += " / {} = {}".format(str(components[i+1]), str(total / components[i+1]))
                            total /= components[i+1]
                        else:
                            return await ctx.send("Cannot roll; no number to divide by after /")
                    elif components[i] is'%':
                        if i + 1 < len(components) and isinstance(components[i+1], int ):
                            results += " % {} = {}".format(str(components[i+1]), str(total % components[i+1]))
                            total %= components[i+1]
                        else:
                            return await ctx.send("Cannot roll; no number to modulo with")
 
                return await ctx.send("{} :game_die: {} :game_die:".format(author.mention, results))