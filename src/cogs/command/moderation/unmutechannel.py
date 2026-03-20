import discord
from discord.ext import commands
from discord.ext.commands import MissingAnyRole
from src.utils import constants


class UnmuteChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(guild_ids=constants.GUILD_ID, name="unmutechannel", description="Unmute a channel")
    @commands.has_any_role(*constants.MOD_ROLES)
    async def unmutechannel(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)

        embed = discord.Embed(title="Success!", description="You have unmuted this channel", color=discord.Color.random())
        await ctx.respond(embed=embed, ephemeral=True)

        channel = discord.utils.get(ctx.guild.channels, id=constants.MOD_LOGS_ID)
        mod_logs_embed = discord.Embed(description=f"{ctx.author.mention} unmuted <#{ctx.channel.id}>", color=discord.Color.random())
        await channel.send(embed=mod_logs_embed)

    @unmutechannel.error
    async def unmutechannel_error(self, ctx, error):
        if isinstance(error, MissingAnyRole):
            embed = constants.NOT_A_MODERATOR_MESSAGE
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            raise error


def setup(bot):
    bot.add_cog(UnmuteChannel(bot))
