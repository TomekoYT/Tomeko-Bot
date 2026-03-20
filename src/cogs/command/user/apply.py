import discord
from discord.ext import commands
from src.utils import constants


class Apply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(guild_ids=constants.GUILD_ID, name="apply", description="Apply for a role")
    async def apply(self, ctx,
                    role: discord.Option(discord.Role, description="Mention the role you want to apply", required=True),
                    message: discord.Option(str, description="Useful info, links, etc", required=True)):
        if role.id not in constants.APPLY_ROLES:
            embed = discord.Embed(title="Failure!", description="You cannot apply for that role!",
                                  color=discord.Color.random())
            await ctx.respond(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(title="Success!", color=discord.Color.random())
        embed.add_field(name="Applied for:", value=f"Role **{role.name}**", inline=False)
        embed.add_field(name="Your message:", value=message, inline=False)
        await ctx.send(embed=embed)

        channel = discord.utils.get(ctx.guild.channels, id=constants.APPLIES_ID)
        apply_embed = discord.Embed(
            description=f"{ctx.author.mention} wants to apply for {role.mention}. Their message: {message}",
            color=discord.Color.random())
        await channel.send(embed=apply_embed)


def setup(bot):
    bot.add_cog(Apply(bot))
