import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone
from utils import constants

class RestrictedChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != constants.DO_NOT_TYPE_HERE_ID:
            return
        
        if any(role.id in constants.MOD_ROLES for role in message.author.roles):
            return
        
        await message.delete()
        
        mute_cog = self.bot.get_cog("Mute")
        purge_cog = self.bot.get_cog("Purge")
        
        if mute_cog:
            await mute_cog.mute_user(
                user = message.author,
                duration = timedelta(days=28)
            )

        if purge_cog:
            await purge_cog.purge_user(
                guild = message.guild,
                user = message.author,
                duration = datetime.now(timezone.utc) - timedelta(minutes=1)
            )


def setup(bot):
    bot.add_cog(RestrictedChannel(bot))
