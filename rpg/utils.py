from redbot.core import Config
import discord

class Utils():
    """Returns whether a user has a given role. The 'role' argument can either be the role as an object, or the exact name of the role."""
    async def MemberHasRole(member, role):
        if isinstance(role, str):
            role = discord.utils.get(member.guild.roles, name=role)
        if role is None:
            print("The given role does not exist, returning false!")
            return False
        else:
            roles = member.roles
            for i in roles:
                if i.id == role.id:
                    return True
            return False