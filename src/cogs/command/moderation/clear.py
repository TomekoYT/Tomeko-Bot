import discord
from discord.ext import commands
from discord.ext.commands import MissingAnyRole
from utils import constants


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clearnumber = 0

    @discord.slash_command(guild_ids=constants.GUILD_ID, name="clear", description="Clears a set number of messages")
    @commands.has_any_role(*constants.MOD_ROLES)
    async def clear(self, ctx, number: discord.Option(int, description="Pick a number of messages to clear", required=True)):
        if number <= 0:
            embed = discord.Embed(title="Failure!", description="You must provide a number greater than 0", color=discord.Color.random())
            await ctx.respond(embed=embed, ephemeral=True)
            return

        if ctx.channel.id in constants.RESTRICTED_CLEAR_CHANNELS:
            embed = discord.Embed(title="Failure!", description="You cannot use this command here", color=discord.Color.random())
            await ctx.respond(embed=embed, ephemeral=True)
            return
        
        embed = discord.Embed(title="Success!", color=discord.Color.random())
        embed.add_field(name="You have cleared:", value=f"{number} message(s).", inline=False)
        await ctx.respond(embed=embed, ephemeral=True)

        channel = discord.utils.get(ctx.guild.channels, id=constants.MOD_LOGS_ID)
        mod_logs_embed = discord.Embed(description=f"{ctx.author.mention} cleared {number} message(s) from <#{ctx.channel.id}>", color=discord.Color.random())
        await channel.send(embed=mod_logs_embed)

        self.clearnumber = number
        await ctx.channel.purge(limit=number)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingAnyRole):
            embed = constants.NOT_A_MODERATOR_MESSAGE
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            raise error


def setup(bot):
    bot.add_cog(Clear(bot))
