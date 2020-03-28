import discord
from discord.ext import commands

list_of_developers = {
    "Plugs": 146737110974595073,
    "RedVelvetUnderground": 449997098956488724
}

# check if a developer is using the command
def check_if_it_is_dev(ctx):
    if ctx.message.author.id in list_of_developers.values():
        return True


# SQL STATEMENTS
def check_for_fish(fish_name):
    return f"""SELECT *
                FROM fish
                WHERE name = '{fish_name}'"""
