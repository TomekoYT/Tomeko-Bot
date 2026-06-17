import discord
from discord.ext import commands
from discord.ext.commands import MissingAnyRole
from datetime import datetime, timedelta, timezone
from utils import constants


class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(guild_ids=constants.GUILD_ID, name="purge", description="Purge user's messages from the last 24 hours")
    @commands.has_any_role(*constants.MOD_ROLES)
    async def purge(self, ctx,
                  user: discord.Option(discord.Member, description="Mention the user to purge", required=True),
                  reason: discord.Option(str, description="Provide a reason", required=True)):
        if any(discord.utils.get(ctx.guild.roles, id=role_id) in user.roles for role_id in constants.RESTRICTED_BAN_ROLES):
            embed = discord.Embed(title="Failure!", description="You cannot purge a Moderator!", color=discord.Color.random())
            await ctx.respond(embed=embed, ephemeral=True)
            return
        
        embed = discord.Embed(title="Success!", color=discord.Color.random())
        embed.add_field(name="Purged:", value=f"{ctx.author.mention} purged all {user.mention} messages from the last 24 hours.",
                        inline=False)
        embed.add_field(name="Reason:", value=reason, inline=False)
        await ctx.respond(embed=embed, ephemeral=True)

        channel = discord.utils.get(ctx.guild.channels, id=constants.MOD_LOGS_ID)
        mod_logs_embed = discord.Embed(description=f"{ctx.author.mention} purged all {user.mention} messages from the last 24 hours. Reason: {reason}",
                                       color=discord.Color.random())
        await channel.send(embed=mod_logs_embed)

        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)

        for channel in ctx.guild.text_channels:
            if channel.id in constants.RESTRICTED_CLEAR_CHANNELS:
                continue

            await channel.purge(
                limit = None,
                check = lambda m: (
                    m.author.id == user.id and m.created_at >= cutoff
                ),
                bulk = True
            )

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, MissingAnyRole):
            embed = constants.NOT_A_MODERATOR_MESSAGE
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            raise error


def setup(bot):
    bot.add_cog(Purge(bot))
