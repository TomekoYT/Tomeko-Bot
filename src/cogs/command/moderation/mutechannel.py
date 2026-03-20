import discord
from discord.ext import commands
from discord.ext.commands import MissingAnyRole
from src.utils import constants


class MuteChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(guild_ids=constants.GUILD_ID, name="mutechannel", description="Mute a channel")
    @commands.has_any_role(*constants.MOD_ROLES)
    async def mutechannel(self, ctx):
        if ctx.channel.id in constants.RESTRICTED_MUTE_CHANNELS:
            embed = discord.Embed(title="Failure!", description="You cannot use this command here", color=discord.Color.random())
            await ctx.respond(embed=embed, ephemeral=True)
            return

        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)

        embed = discord.Embed(title="Success!", description="You have muted this channel", color=discord.Color.random())
        await ctx.respond(embed=embed, ephemeral=True)

        channel = discord.utils.get(ctx.guild.channels, id=constants.MOD_LOGS_ID)
        mod_logs_embed = discord.Embed(description=f"{ctx.author.mention} muted <#{ctx.channel.id}>", color=discord.Color.random())
        await channel.send(embed=mod_logs_embed)

    @mutechannel.error
    async def mutechannel_error(self, ctx, error):
        if isinstance(error, MissingAnyRole):
            embed = constants.NOT_A_MODERATOR_MESSAGE
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            raise error


def setup(bot):
    bot.add_cog(MuteChannel(bot))
