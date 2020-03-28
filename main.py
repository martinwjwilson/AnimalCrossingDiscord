import discord
from discord.ext import commands
import json

# load cogs
bot = commands.Bot(command_prefix = ">")
extensions = ["search"] # list of cogs to call

# laod bot token
with open("token.json", 'r') as f:
    token = json.load(f)['TOKEN']


@bot.event
async def on_ready():
    print(f"{bot.user.name} - {bot.user.id}") # name of bot and ID
    print(discord.__version__) # current version of discord
    print("Ready...")


# immediately stop the bot
@bot.command(hidden = True)
async def stop(ctx):
    await bot.logout() # log the bot off


# manually load a cog
@bot.command(hidden = True)
async def load(ctx, extension):
    try:
        bot.load_extension(extension)
        print(f"Loaded {extension}.\n")
    except Exception as error:
        print(f"{extension} could not be loaded. [{error}]")


# manually unload a cog
@bot.command(hidden = True)
async def unload(ctx, extension):
    try:
        bot.unload_extension(extension)
        print(f"Unloaded {extension}.\n")
    except Exception as error:
        print(f"{extension} could not be unloaded. [{error}]")


# manually reload a cog
@bot.command(hidden = True)
async def reload(ctx, extension):
    try:
        bot.reload_extension(extension)
        print(f"Reloaded {extension}.\n")
    except Exception as error:
        print(f"{extension} could not be reloaded. [{error}]")

# automatically try to load all cogs in list and then run the bot
if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(f"cogs.{extension}")
            print(f"Loaded cog: {extension}")
        except Exception as error:
            print(f"{extension} could not be loaded. [{error}]")
    bot.run(token)
