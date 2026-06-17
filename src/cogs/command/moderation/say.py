import discord
from discord.ext import commands
from discord.ext.commands import MissingAnyRole
from utils import constants


class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(guild_ids=constants.GUILD_ID, name="say", description="Say something")
    @commands.has_any_role(*constants.MOD_ROLES)
    async def say(self, ctx, message: discord.Option(str, description="Provide a message", required=True)):
        embed = discord.Embed(title="Success!", color=discord.Color.random())
        await ctx.respond(embed=embed, ephemeral=True)
        await ctx.send(message)

    @say.error
    async def say_error(self, ctx, error):
        if isinstance(error, MissingAnyRole):
            embed = constants.NOT_A_MODERATOR_MESSAGE
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            raise error


def setup(bot):
    bot.add_cog(Say(bot))
