import discord
from discord.ext import commands
from discord.ext.commands import MissingAnyRole
from utils import constants


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(guild_ids=constants.GUILD_ID, name="kick", description="Kick the user out of the server")
    @commands.has_any_role(*constants.MOD_ROLES)
    async def kick(self, ctx,
                   user: discord.Option(discord.Member, description="Mention the user to kick", required=True),
                   reason: discord.Option(str, description="Provide a reason", required=True)):
        if any(discord.utils.get(ctx.guild.roles, id=role_id) in user.roles for role_id in constants.RESTRICTED_BAN_ROLES):
            embed = discord.Embed(title="Failure!", description="You cannot kick a Moderator!", color=discord.Color.random())
            await ctx.respond(embed=embed, ephemeral=True)
            return

        await ctx.guild.kick(user)
        embed = discord.Embed(title="Success!", color=discord.Color.random())
        embed.add_field(name="Kicked:", value=f"{user.mention} has been kicked from the server by {ctx.author.mention}.",
                        inline=False)
        embed.add_field(name="Reason:", value=reason, inline=False)
        await ctx.respond(embed=embed, ephemeral=True)

        channel = discord.utils.get(ctx.guild.channels, id=constants.MOD_LOGS_ID)
        mod_logs_embed = discord.Embed(description=f"{user.mention} was kicked by {ctx.author.mention}. Reason: {reason}",
                                       color=discord.Color.random())
        await channel.send(embed=mod_logs_embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingAnyRole):
            embed = constants.NOT_A_MODERATOR_MESSAGE
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            raise error


def setup(bot):
    bot.add_cog(Kick(bot))
