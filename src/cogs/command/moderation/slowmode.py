import discord
from discord.ext import commands
from discord.ext.commands import MissingAnyRole
from utils import constants


class Slowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(guild_ids=constants.GUILD_ID, name="slowmode", description="Set a channel slowmode")
    @commands.has_any_role(*constants.MOD_ROLES)
    async def slowmode(self, ctx, seconds: discord.Option(int, description="Pick a number of seconds to set", required=True)):
        await ctx.channel.edit(slowmode_delay=seconds)

        embed = discord.Embed(title="Success!", color=discord.Color.random())
        embed.add_field(name="You have set slowmode to:", value=f"{seconds} seconds.", inline=False)
        await ctx.respond(embed=embed, ephemeral=True)

        channel = discord.utils.get(ctx.guild.channels, id=constants.MOD_LOGS_ID)
        mod_logs_embed = discord.Embed(description=f"{ctx.author.mention} set a slowmode to {seconds} seconds in <#{ctx.channel.id}>", color=discord.Color.random())
        await channel.send(embed=mod_logs_embed)

    @slowmode.error
    async def slowmode_error(self, ctx, error):
        if isinstance(error, MissingAnyRole):
            embed = constants.NOT_A_MODERATOR_MESSAGE
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            raise error


def setup(bot):
    bot.add_cog(Slowmode(bot))
