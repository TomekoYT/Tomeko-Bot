import discord
from discord.ext import commands
from discord.ext.commands import MissingAnyRole
from src.utils import constants
from datetime import timedelta


class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(guild_ids=constants.GUILD_ID, name="mute", description="Mute the user")
    @commands.has_any_role(*constants.MOD_ROLES)
    async def mute(self, ctx,
                   user: discord.Option(discord.Member, description="Mention the user to mute", required=True),
                   reason: discord.Option(str, description="Provide a reason", required=True),
                   days: discord.Option(int, description="Number of days to mute", required=False),
                   hours: discord.Option(int, description="Number of hours to mute", required=False),
                   minutes: discord.Option(int, description="Number of minutes to mute", required=False)):

        if any(discord.utils.get(ctx.guild.roles, id=id) in user.roles for id in constants.RESTRICTED_BAN_ROLES):
            embed = discord.Embed(title="Failure!", description="You cannot mute a Moderator!", color=discord.Color.random())
            await ctx.respond(embed=embed, ephemeral=True)
            return

        if days is None and hours is None and minutes is None:
            embed = discord.Embed(title="Failure!", description="You didn't provide any time for mute!", color=discord.Color.random())
            await ctx.respond(embed=embed, ephemeral=True)
            return

        days = days or 0
        hours = hours or 0
        minutes = minutes or 0

        duration = timedelta(days=days, hours=hours, minutes=minutes, seconds=0)
        await user.timeout_for(duration)

        embed = discord.Embed(title="Success!", color=discord.Color.random())
        embed.add_field(name="Muted:", value=f"{user.mention} has been muted from the server by {ctx.author.mention}.", inline=False)
        embed.add_field(name="Duration:", value=f"{duration}")
        embed.add_field(name="Reason:", value=reason, inline=False)
        await ctx.respond(embed=embed, ephemeral=True)

        channel = discord.utils.get(ctx.guild.channels, id=constants.MOD_LOGS_ID)
        mod_logs_embed = discord.Embed(description=f"{user.mention} was muted by {ctx.author.mention}. Duration: {duration}. Reason: {reason}", color=discord.Color.random())
        await channel.send(embed=mod_logs_embed)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, MissingAnyRole):
            embed = constants.NOT_A_MODERATOR_MESSAGE
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            raise error


def setup(bot):
    bot.add_cog(Mute(bot))
