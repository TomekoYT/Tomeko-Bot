import discord
from discord.ext import commands
from src.utils import constants


class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(guild_ids=constants.GUILD_ID, name="report", description="Report the user")
    async def report(self, ctx,
                     user: discord.Option(discord.Member, description="Mention the user to report", required=True),
                     reason: discord.Option(str, description="Provide the reason for report", required=True)):
        embed = discord.Embed(title="Success!", color=discord.Color.random())
        embed.add_field(name="Reported:", value=f"{user.mention} has been reported.", inline=False)
        embed.add_field(name="Reason:", value=f"**{reason}**", inline=False)
        await ctx.respond(embed=embed, ephemeral=True)

        mod_channel = discord.utils.get(ctx.guild.channels, id=constants.REPORTS_ID)
        mod_role = discord.utils.get(ctx.guild.roles, id=constants.MOD)
        mod_logs_embed = discord.Embed(
            description=f"{user.mention} has been reported by {ctx.author.mention} for **{reason}** on channel <#{ctx.channel.id}>",
            color=discord.Color.random())
        await mod_channel.send(f"{mod_role.mention}!")
        await mod_channel.send(embed=mod_logs_embed)


def setup(bot):
    bot.add_cog(Report(bot))
