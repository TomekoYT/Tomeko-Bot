import discord
from discord.ext import commands
import os
from utils import constants

bot = commands.Bot(command_prefix=constants.PREFIX, intents=discord.Intents.all(), activity=constants.ACTIVITY)

@bot.event
async def on_ready():
    print("Bot is online!")

for root, dirs, files in os.walk("src/cogs"):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file).replace("\\", "/").replace("/", ".")
            path = path[4:-3]
            print("Cog: " + path + " loading...")
            bot.load_extension(path)
            print("Cog: " + path + " loaded!")

bot.run(constants.TOKEN)