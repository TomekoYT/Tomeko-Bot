import discord
from discord.ext import commands
from discord.ext.commands import MissingAnyRole
from utils import constants


class AddRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=constants.GUILD_ID, name="addrole", description="Add a role to the user")
    @commands.has_any_role(*constants.MOD_ROLES)
    async def addrole(self, ctx,
                      user: discord.Option(discord.Member, description="Mention the user", required=True),
                      role: discord.Option(discord.Role, description="Mention the role to add", required=True)):
        if role.id in constants.RESTRICTED_GIVE_ROLES:
            embed = discord.Embed(title="Failure!", description="You cannot add that role!", color=discord.Color.random())
            await ctx.respond(embed=embed, ephemeral=True)
            return

        if role.id in user.roles:
            embed = discord.Embed(title="Failure!", description=f"{user.mention} already has a role {role.mention}", color=discord.Color.random())
            await ctx.respond(embed=embed, ephemeral=True)
            return

        await user.add_roles(role)
        embed = discord.Embed(title="Success!", color=discord.Color.random())
        embed.add_field(name="Added a role:", value=f"{user.mention} got a role {role.mention}.", inline=False)
        await ctx.respond(embed=embed, ephemeral=True)

        channel = discord.utils.get(ctx.guild.channels, id=constants.MOD_LOGS_ID)
        mod_logs_embed = discord.Embed(description=f"{ctx.author.mention} added a role {role.mention} to {user.mention}.", color=discord.Color.random())
        await channel.send(embed=mod_logs_embed)

    @addrole.error
    async def addrole_error(self, ctx, error):
        if isinstance(error, MissingAnyRole):
            embed = constants.NOT_A_MODERATOR_MESSAGE
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            raise error


def setup(bot):
    bot.add_cog(AddRole(bot))
