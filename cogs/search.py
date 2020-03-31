import discord
from discord.ext import commands
import utils
import sqlite3
import typing
from datetime import date


# db
conn = sqlite3.connect("critterpedia.db")
c = conn.cursor()


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.check(utils.check_if_it_is_dev)
    async def test(self, ctx):
        current_month = date.today().strftime("%B")
        await ctx.send(current_month)


    async def availability_review(self, critter_month: str):
        # check if the critter is all year round
        if critter_month.startswith("Year"):
            return True

        # get this months month
        current_month = date.today().strftime("%B")
        print(f"Current month is: {current_month}")
        northern_months = critter_month.split("/")[0] # split the critter month into Northern and Southern
        northern_months = northern_months.split("(")[0] # remove the (northern) section

        if "," in northern_months: # if critter is available twice a year, split it up
            periods = northern_months.split(",")
            period_1 = periods[0]
            period_2 = periods[1]
            # get start and end months from each period
            start_month_1, end_month_1 = period_1.split("-")
            print(f"Start month period 1: {start_month_1}\nEnd Month period 1: {end_month_1}\n")
            start_month_2, end_month_2 = period_2.split("-")
            print(f"Start month period 2: {start_month_2}\nEnd Month period 2: {end_month_2}\n")
        elif "-" in northern_months: # there is one period per year
            # get start and end months
            start_month, end_month = northern_months.split("-")
            print(f"Start month: {start_month}\nEnd Month: {end_month}\n")
            # generate a list of months critter is available
        else: # it is available for a single month per year
            print(f"{northern_months}\n")


    async def this_month_critter_filter(self, list_of_critters: list):
        critter_availble_list = [] # list of critters available this month
        # check each critter against the current date
        for critter in list_of_critters:
            # check if the critter is a fish or a bug
            if critter[1] == "Fish":
                # check availability this month
                print(f"Name: {critter[0]}\nType: {critter[1]}\nMonth: {critter[6]}\n")
                if await self.availability_review(critter[6]):
                    pass
            else:
                # check availability this month
                # print(f"Name: {critter[0]}\nType: {critter[1]}\nMonth: {critter[5]}\n")
                if await self.availability_review(critter[5]):
                    pass


    @commands.command()
    async def month(self, ctx):
        # get all fish
        c.execute(utils.search_all_critters("fish", "")) # Execute the SQL check
        fish_list = list(c.fetchall())
        # get all bugs
        c.execute(utils.search_all_critters("bugs", "")) # Execute the SQL check
        bug_list = list(c.fetchall())

        # get a list of all fish leaving this month
        await self.this_month_critter_filter(fish_list)


    @commands.command()
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
        embed.add_field(name = "Month:", value = fish_list[6], inline = False)
        await ctx.send(embed = embed)


    @commands.command()
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
        embed.add_field(name = "Month:", value = bug_list[5], inline = False)
        await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(Search(bot))
