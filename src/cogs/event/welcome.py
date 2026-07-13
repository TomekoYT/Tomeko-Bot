import discord
from discord.ext import commands
from utils import constants


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, user):
        for role in constants.AUTO_ROLES:
            auto_role = discord.utils.get(user.guild.roles, id=role)
            await user.add_roles(auto_role)

        channel = discord.utils.get(user.guild.channels, id=constants.LOBBY_ID)

        welcome_embed = discord.Embed(title="NEW MEMBER 🥳", color=discord.Color.random())
        welcome_embed.add_field(name="Welcome to Tomeko's World!",
                                value=f"Hello {user.mention}! You are user #{user.guild.member_count}!", inline=False)
        welcome_embed.set_image(url=user.avatar)
        await channel.send(embed=welcome_embed)

    @commands.Cog.listener()
    async def on_member_remove(self, user):
        channel = discord.utils.get(user.guild.channels, id=constants.LOBBY_ID)
        await channel.send(f"Goodbye {user.mention}! 😢")


def setup(bot):
    bot.add_cog(Welcome(bot))
