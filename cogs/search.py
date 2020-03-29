import discord
from discord.ext import commands
import utils
import sqlite3
import typing


# db
conn = sqlite3.connect("critterpedia.db")
c = conn.cursor()


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def test(self, ctx, input):
        await ctx.send("nothing here")


    @commands.command()
    @commands.check(utils.check_if_it_is_dev)
    async def fish(self, ctx, starts_with: typing.Optional[str] = ""):
        # check if there was a letter
        if starts_with != "":
            starts_with = utils.format_input(starts_with) # format the input
            starts_with = f"WHERE name LIKE '{starts_with}%'" # add sql for search

        c.execute(utils.search_all_critters("fish", starts_with)) # Execute the SQL check
        fish_list = list(c.fetchall())
        fish_names = ""
        for fish in fish_list:
            fish_names = fish_names + f"{fish[0]}\n"
        embed = discord.Embed(title = "Fish search", description = fish_names)
        await ctx.send(embed = embed)


    @commands.command()
    @commands.check(utils.check_if_it_is_dev)
    async def bug(self, ctx, starts_with: typing.Optional[str] = ""):
        # check if there was a letter
        if starts_with != "":
            starts_with = utils.format_input(starts_with) # format the input
            starts_with = f"WHERE name LIKE '{starts_with}%'" # add sql for search

        c.execute(utils.search_all_critters("bugs", starts_with)) # Execute the SQL check
        bug_list = list(c.fetchall())
        bug_names = ""
        for bug in bug_list:
            bug_names = bug_names + f"{bug[0]}\n"
        embed = discord.Embed(title = "Bug search", description = bug_names)
        await ctx.send(embed = embed)


    @commands.command()
    @commands.check(utils.check_if_it_is_dev)
    async def f(self, ctx, *,  fish_name: str):
        fish_name = utils.format_input(fish_name) # format the input
        c.execute(utils.check_for_critter("fish", fish_name)) # Execute the SQL check
        fish_list = list(c.fetchone())

        # create embed
        embed = discord.Embed(title = 'Fish Info', description = f"Everything you need to know about the {fish_list[0]}")
        embed.add_field(name = "Name:", value = fish_list[0], inline = False)
        embed.add_field(name = "Type:", value = fish_list[1], inline = False)
        embed.add_field(name = "Location:", value = fish_list[2], inline = False)
        embed.add_field(name = "Size:", value = fish_list[3], inline = False)
        embed.add_field(name = "Value:", value = fish_list[4], inline = False)
        embed.add_field(name = "Time:", value = fish_list[5], inline = False)
        embed.add_field(name = "Location:", value = fish_list[6], inline = False)
        await ctx.send(embed = embed)


    @commands.command()
    @commands.check(utils.check_if_it_is_dev)
    async def b(self, ctx, *,  bug_name: str):
        bug_name = utils.format_input(bug_name) # format the input
        c.execute(utils.check_for_critter("bugs", bug_name)) # Execute the SQL check
        bug_list = list(c.fetchone())

        # create embed
        embed = discord.Embed(title = 'Bug Info', description = f"Everything you need to know about the {bug_list[0]}")
        embed.add_field(name = "Name:", value = bug_list[0], inline = False)
        embed.add_field(name = "Type:", value = bug_list[1], inline = False)
        embed.add_field(name = "Location:", value = bug_list[2], inline = False)
        embed.add_field(name = "Value:", value = bug_list[3], inline = False)
        embed.add_field(name = "Time:", value = bug_list[4], inline = False)
        embed.add_field(name = "Location:", value = bug_list[5], inline = False)
        await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(Search(bot))
