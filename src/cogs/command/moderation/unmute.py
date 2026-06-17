import discord
from discord.ext import commands
from discord.ext.commands import MissingAnyRole
from utils import constants


class Unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(guild_ids=constants.GUILD_ID, name="unmute", description="Unmute the user")
    @commands.has_any_role(*constants.MOD_ROLES)
    async def unmute(self, ctx, user: discord.Option(discord.Member, description="Mention the user to unmute", required=True)):
        await user.remove_timeout()

        embed = discord.Embed(title="Success!", color=discord.Color.random())
        embed.add_field(name="Unmuted:", value=f"{user.mention} has been unmuted from the server by {ctx.author.mention}.", inline=False)
        await ctx.respond(embed=embed, ephemeral=True)

        channel = discord.utils.get(ctx.guild.channels, id=constants.MOD_LOGS_ID)
        mod_logs_embed = discord.Embed(description=f"{user.mention} was unmuted by {ctx.author.mention}.", color=discord.Color.random())
        await channel.send(embed=mod_logs_embed)

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, MissingAnyRole):
            embed = constants.NOT_A_MODERATOR_MESSAGE
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            raise error


def setup(bot):
    bot.add_cog(Unmute(bot))
