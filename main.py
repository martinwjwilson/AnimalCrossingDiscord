import discord
from discord.ext import commands
import json
import utils
import typing

# load cogs
bot = commands.Bot(command_prefix=">", help_command=None)
extensions = ["admin", "search"]  # list of cogs to call

# laod bot token
with open("token.json", 'r') as f:
    token = json.load(f)['TOKEN']


@bot.event
async def on_ready():
    print(f"{bot.user.name} - {bot.user.id}")  # name of bot and ID
    print(discord.__version__)  # current version of discord
    print("Ready...")


@bot.command()
async def help(ctx, command_name: typing.Optional[str] = ""):
    """
    Custom help messages for each command
    """
    if command_name == "":
        embed = discord.Embed(title="Command List",
                              description="Here are all of the bot commands!\nFor information on using a specific command, use `>help {command}`")
        embed.add_field(name="Search:", value="s\nfish\nbug\nmonth\narriving\nleaving")
    elif command_name == "s":
        embed = discord.Embed(title=">s critter_name",
                              description="Search for a critter by name and display all related information")
        embed.add_field(name="Example",
                        value="`>s bitterling` will return all of the details about the bitterling such as size, value, etc")
    elif command_name == "fish":
        embed = discord.Embed(title=">fish starts_with",
                              description="Display a list of all fish in alphabetical order. If the optional `starts_with` is provided then the list will show fish starting with the input")
        embed.add_field(name="Example 1", value="`>fish` will return all fish in the game in alphabetical order")
        embed.add_field(name="Example 2", value="`>fish se` will return:\n- Sea Bass\n- Sea Butterfly\n- Sea Horse",
                        inline=False)
    elif command_name == "bug":
        embed = discord.Embed(title=">bug starts_with",
                              description="Display a list of all bugs in alphabetical order. If the optional `starts_with` is provided then the list will show bugs starting with the input")
        embed.add_field(name="Example 1", value="`>bug` will return all bugs in the game in alphabetical order")
        embed.add_field(name="Example 2", value="`>bug sc` will return:\n- Scarab Beetle\n- Scorpion", inline=False)
    # elif command_name == "month":
    #     embed = discord.Embed(title = ">month", description = "Get a list of all fish and bugs available this month")
    #     embed.add_field(name = "Notes:", value = "Currently this command only works for the northern hemisphere")
    # elif command_name == "arriving":
    #     embed = discord.Embed(title = ">arriving hemisphere", description = "Display a list of all fish and bugs arriving in the current month. The hemisphere is optional, `n` for northern and `s` for southern. The default hemisphere is `n`")
    #     embed.add_field(name = "Example 1", value = "`>arriving` will rdisplay a list of all the fish and bugs arriving in the current month in the northern hemisphere")
    #     embed.add_field(name = "Example 2", value = "`>arriving s` will rdisplay a list of all the fish and bugs arriving in the current month in the southern hemisphere")
    # elif command_name == "leaving":
    #     embed = discord.Embed(title = ">leaving hemisphere", description = "Display a list of all fish and bugs leaving in the current month. The hemisphere is optional, `n` for northern and `s` for southern. The default hemisphere is `n`")
    #     embed.add_field(name = "Example 1", value = "`>leaving` will rdisplay a list of all the fish and bugs leaving in the current month in the northern hemisphere")
    #     embed.add_field(name = "Example 2", value = "`>leaving s` will rdisplay a list of all the fish and bugs leaving in the current month in the southern hemisphere")
    embed.add_field(name="Support the bot!", value="*https://ko-fi.com/plugs*", inline=False)
    await ctx.send(embed=embed)


# immediately stop the bot
@bot.command(hidden=True)
@commands.check(utils.check_if_it_is_dev)
async def stop(ctx):
    await bot.logout()  # log the bot off


# manually load a cog
@bot.command(hidden=True)
@commands.check(utils.check_if_it_is_dev)
async def load(ctx, extension):
    try:
        bot.load_extension(f"cogs.{extension}")
        print(f"Loaded {extension}.\n")
    except Exception as error:
        print(f"{extension} could not be loaded. [{error}]")


# manually unload a cog
@bot.command(hidden=True)
@commands.check(utils.check_if_it_is_dev)
async def unload(ctx, extension):
    try:
        bot.unload_extension(f"cogs.{extension}")
        print(f"Unloaded {extension}.\n")
    except Exception as error:
        print(f"{extension} could not be unloaded. [{error}]")


# manually reload a cog
@bot.command(hidden=True)
@commands.check(utils.check_if_it_is_dev)
async def reload(ctx, extension):
    try:
        bot.reload_extension(f"cogs.{extension}")
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
