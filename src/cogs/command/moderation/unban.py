import discord
from discord.ext import commands
from discord.ext.commands import MissingAnyRole
from src.utils import constants


class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(guild_ids=constants.GUILD_ID, name="unban", description="Unban the user")
    @commands.has_any_role(*constants.MOD_ROLES)
    async def unban(self, ctx, user: discord.Option(discord.Member, description="Mention the user to unban", required=True)):
        await ctx.guild.unban(user)

        embed = discord.Embed(title="Success!", color=discord.Color.random())
        embed.add_field(name="Unbanned:", value=f"{user.name} has been unbanned from the server by {ctx.author.mention}.", inline=False)
        await ctx.respond(embed=embed, ephemeral=True)

        channel = discord.utils.get(ctx.guild.channels, id=constants.MOD_LOGS_ID)
        mod_logs_embed = discord.Embed(description=f"{user.name} was unbanned by {ctx.author.mention}.", color=discord.Color.random())
        await channel.send(embed=mod_logs_embed)

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, MissingAnyRole):
            embed = constants.NOT_A_MODERATOR_MESSAGE
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            raise error


def setup(bot):
    bot.add_cog(Unban(bot))
