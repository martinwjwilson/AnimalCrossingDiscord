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

    @commands.command(hidden=True)
    @commands.check(utils.check_if_it_is_dev)
    async def test(self, ctx):
        await ctx.send(file=discord.File("ProfessionalRetard.jpg"))

    async def format_input(self, input):
        """
        Format a string to match the style of the db entries
        """
        str_input = "".join(input) # join arguments together
        # fix casing
        word_list = str_input.lower().split(" ") # split each word by space and make lowercase
        output = []
        for word in word_list:
            output.append(word.capitalize()) # capitalise all lowercase words in list
        return " ".join(output) # join words back together with a space between them

    async def month_list(self, start_month: str, end_month: str):
        """
        Return a list of months from the start month until the end month
        """
        dict_of_all_months = {
            "January":1,
            "February":2,
            "March":3,
            "April":4,
            "May":5,
            "June":6,
            "July":7,
            "August":8,
            "September":9,
            "October":10,
            "November":11,
            "December":12}
        start_month_int = dict_of_all_months[start_month] # ' November'
        end_month_int = dict_of_all_months[end_month]
        list_of_months_available = []
        # if start month is less than end month, include everything greater than start month and less than or = end month
        if start_month_int < end_month_int:
            for month in dict_of_all_months:
                if dict_of_all_months[month] >= start_month_int and dict_of_all_months[month] <= end_month_int:
                    list_of_months_available.append(month)
        # if end month is less than start month, include everything greater or equal to start month and less than or = end month
        else:
            for month in dict_of_all_months:
                if dict_of_all_months[month] >= start_month_int or dict_of_all_months[month] <= end_month_int:
                    list_of_months_available.append(month)
        # check if current month is in list
        return list_of_months_available


    async def availability_review(self, critter_month: str):
        """
        Check the availability for an individual critter
        """
        # check if the critter is all year round
        if critter_month.startswith("Year"):
            return True
        # get this months month
        current_month = date.today().strftime("%B")
        northern_months = critter_month.split("/")[0] # split the critter month into Northern and Southern
        northern_months = northern_months.split("(")[0].strip() # remove the (northern) section

        if "," in northern_months: # if critter is available twice a year, split it up
            periods = northern_months.split(",")
            period_1 = periods[0]
            period_2 = periods[1]
            # get start and end months from each period
            period_1 = period_1.split("-")
            start_month_1 = period_1[0].strip()
            end_month_1 = period_1[1].strip()
            if "-" in period_2:
                period_2 = period_2.split("-")
            else: # if it's a ladybug... :v
                period_2 = [period_2, period_2]
            start_month_2 = period_2[0].strip()
            end_month_2 = period_2[1].strip()
            if (current_month in await self.month_list(start_month_1, end_month_1)) or (current_month in await self.month_list(start_month_2.strip(), end_month_2)):
                return True
        elif "-" in northern_months: # there is one period per year
            # get start and end months
            start_month, end_month = northern_months.split("-")
            # generate a list of months critter is available
            if current_month in await self.month_list(start_month, end_month):
                return True
        else: # it is available for a single month per year
            if current_month == northern_months:
                return True
        return False

    async def this_month_critter_filter(self, list_of_critters: list):
        """
        filters list of all bugs and fish to ones available this month
        """
        critters_available_list = [] # list of critters available this month
        # check each critter against the current date
        for critter in list_of_critters:
            # check if the critter is a fish or a bug
            if critter[1] == "Fish":
                # check availability this month
                if await self.availability_review(critter[6]):
                    critters_available_list.append(critter[0])
            else:
                # check availability this month
                if await self.availability_review(critter[5]):
                    critters_available_list.append(critter[0])
        return critters_available_list

    @commands.command()
    async def month(self, ctx):
        """
        Get a list of all fish and bugs available this month
        """
        # get all fish
        c.execute(utils.search_all_critters("fish", "")) # Execute the SQL check
        fish_list = list(c.fetchall())
        # get all bugs
        c.execute(utils.search_all_critters("bugs", "")) # Execute the SQL check
        bug_list = list(c.fetchall())
        description_f = ""
        description_b = ""
        # get a list of all fish available this month
        critters_available_list = await self.this_month_critter_filter(fish_list)
        for critter in critters_available_list:
            description_f = description_f + f"\n{critter}"
        # get a list of all bugs available this month
        critters_available_list = await self.this_month_critter_filter(bug_list)
        for critter in critters_available_list:
            description_b = description_b + f"\n{critter}"

        embed_f = discord.Embed(title = "List of Fish available this month", description = description_f)
        embed_b = discord.Embed(title = "List of Bugs available this month", description = description_b)
        await ctx.send(embed = embed_f)
        await ctx.send(embed = embed_b)

    async def critter_available_twice_per_year(self, current_month: str, critter_months: str, change_type: str) -> bool:
        periods = critter_months.split(",")
        period_1 = periods[0]
        period_2 = periods[1]
        if((await self.critter_available_once_per_year(current_month, period_1, change_type)) or (await self.critter_available_once_per_year(current_month, period_2, change_type))):
            return True
        else:
            return False

    async def critter_available_once_per_year(self, current_month: str, critter_months: str, change_type: str) -> bool:
        # get start and end months
        start_month, end_month = critter_months.split("-")
        # check change type
        if change_type == "arriving":
            if current_month == start_month:
                return True
            else:
                return False
        elif change_type == "leaving":
            if current_month == end_month:
                return True
            else:
                return False

    async def critter_fits_change_check(self, critter_month: str, change_type: str, hemisphere: str) -> bool:
        """
        Check if a critter follows the change being checked against
        Return a bool representing if the critter does or doesn't follow the change
        e.g. a critter leaves in June and the check is for all critters leaving in June. Return True
        """
        # get the current momnth in the desired format
        current_month = date.today().strftime("%B")
        if critter_month == "Year-round (Northern and Southern)": # check if the critter is available all year
            return False
        critter_northern_period, critter_southern_period = critter_month.split("/") # split the critter month into Northern and Southern
        critter_northern_months = critter_northern_period.split("(")[0].strip() # remove the word Northern
        critter_southern_months = critter_southern_period.split("(")[0].strip()# remove the word Southern
        # check if the current month matches the critter availability
        if hemisphere == "n": # Northern
            if "," in critter_northern_months: # if critter is available in two periods per year
                return await self.critter_available_twice_per_year(current_month, critter_northern_months, change_type)
            elif "-" in critter_northern_months: # there is one period per year
                return await self.critter_available_once_per_year(current_month, critter_northern_months, change_type)
            elif current_month == critter_northern_months: # critter is available one month of the year
                return True
            return False
        elif hemisphere == "s": # Southern
            if "," in critter_southern_months: # if critter is available in two periods per year
                return await self.critter_available_twice_per_year(current_month, critter_southern_months, change_type)
            elif "-" in critter_southern_months: # there is one period per year
                return await self.critter_available_once_per_year(current_month, critter_southern_months, change_type)
            elif current_month == critter_southern_months: # critter is available one month of the year
                return True
            return False

    async def critter_filter_by_changing(self, list_of_critters: list, change_type: str, hemisphere: str) -> list:
        """
        Filters list of all bugs and fish to ones arriving or leaving this month
        """
        critters_available_list = [] # list of critters available this month
        # check each critter against the current date
        for critter in list_of_critters:
            # check if the critter is a fish or a bug as db tables are different
            if critter[1] == "Fish":
                if await self.critter_fits_change_check(critter[6], change_type, hemisphere):
                    critters_available_list.append(critter[0])
            else:
                if await self.critter_fits_change_check(critter[5], change_type, hemisphere):
                    critters_available_list.append(critter[0])
        return critters_available_list

    async def list_of_critter_changing(self, species: str, change_type: str, hemisphere: str) -> str:
        """
        Formats and returns a str of all critters of a given species leaving or arriving depending on the command called
        """
        # get the full list of species
        c.execute(utils.search_all_critters(species, ""))
        all_critter_list = list(c.fetchall())
        # check if arriving or leaving command was called
        if change_type == "arriving":
            critters_available_list = await self.critter_filter_by_changing(all_critter_list, change_type, hemisphere)
        elif change_type == "leaving":
            critters_available_list = await self.critter_filter_by_changing(all_critter_list, change_type, hemisphere)
        # convert the list into a string
        critter_string = ""
        for critter in critters_available_list:
            critter_string = critter_string + f"\n{critter}"
        # return the finalised string
        return critter_string

    async def arriving_or_leaving(self, ctx, change_type: str, hemisphere: str):
        """
        Display a list of all fish and bugs arriving in the current month
        """
        # check that hemisphere is valid
        if hemisphere != "n" and hemisphere != "s":
            await ctx.send("Invalid hemisphere. Must be either `n` or `s`. (No input will default to `n`)")
            return
        # create embeds
        embed_f = discord.Embed(title = "List of Fish leaving this month", description = await self.list_of_critter_changing("fish", change_type, hemisphere))
        embed_b = discord.Embed(title = "List of Bugs leaving this month", description = await self.list_of_critter_changing("bugs", change_type, hemisphere))
        # send embeds
        await ctx.send(embed = embed_f)
        await ctx.send(embed = embed_b)

    @commands.command()
    async def arriving(self, ctx, hemisphere: typing.Optional[str] = "n"):
        """
        Display a list of all fish and bugs arriving in the current month
        """
        await self.arriving_or_leaving(ctx, "arriving", hemisphere)

    @commands.command()
    async def leaving(self, ctx, hemisphere: typing.Optional[str] = "n"):
        """
        Display a list of all fish and bugs leaving at the end of the current month
        """
        await self.arriving_or_leaving(ctx, "leaving", hemisphere)

    async def all_critter_by_species(self, species_type: str, starts_with: str):
        """
        Get a list from the database of all critters of a given species
        Restrict the search to names starting with the 'starts_with' variable if provided
        """
        # check if the search should be restricted
        if starts_with != "":
            starts_with = await self.format_input(starts_with) # format the input
            starts_with = f"WHERE name LIKE '{starts_with}%'" # add sql for search
        c.execute(utils.search_all_critters(species_type, starts_with)) # Execute the SQL check
        critter_list = list(c.fetchall())
        critter_names = ""
        for critter in critter_list:
            critter_names = critter_names + f"{critter[0]}\n"
        return critter_names

    @commands.command()
    async def fish(self, ctx, starts_with: typing.Optional[str] = ""):
        """
        Display a list of all fish by name
        If input is provided then find names beginning with the input
        """
        fish_names = await self.all_critter_by_species("fish", starts_with)
        embed = discord.Embed(title = "Fish search", description = fish_names)
        await ctx.send(embed = embed)

    @commands.command()
    async def bug(self, ctx, starts_with: typing.Optional[str] = ""):
        """
        Display a list of all bugs by name
        If input is provided then find names beginning with the input
        """
        bug_names = await self.all_critter_by_species("bugs", starts_with)
        embed = discord.Embed(title = "Bug search", description = bug_names)
        await ctx.send(embed = embed)

    @commands.command()
    async def s(self, ctx, *, critter_name: str):
        """
        Search for a critter by name and display all of its information
        """
        critter_name = await self.format_input(critter_name) # format the input
        # Check both fish and bug tables
        critter_list = False
        c.execute(utils.check_for_critter("fish", critter_name))
        try:
            fish_list = list(c.fetchone())
            critter_list = fish_list
        except Exception as e:
            pass
        c.execute(utils.check_for_critter("bugs", critter_name))
        try:
            bug_list = list(c.fetchone())
            critter_list = bug_list
        except Exception as e:
            pass
        # if there is a match from the DB
        if critter_list:
            # create embed
            embed = discord.Embed(title = f'{critter_list[1]} Info', description = f"Everything you need to know about the {critter_list[0]}")
            embed.add_field(name = "Name:", value = critter_list[0], inline = False)
            embed.add_field(name = "Type:", value = critter_list[1], inline = False)
            embed.add_field(name = "Location:", value = critter_list[2], inline = False)
            print(critter_list[1])
            if critter_list[1] == 'Fish': # if critter was a fish
                embed.add_field(name = "Size:", value = critter_list[3], inline = False)
                embed.add_field(name = "Value:", value = critter_list[4], inline = False)
                embed.add_field(name = "Time:", value = critter_list[5], inline = False)
                embed.add_field(name = "Month:", value = critter_list[6], inline = False)
                embed.set_image(url = critter_list[7])
            else: # if critter was a bug
                embed.add_field(name = "Value:", value = critter_list[3], inline = False)
                embed.add_field(name = "Time:", value = critter_list[4], inline = False)
                embed.add_field(name = "Month:", value = critter_list[5], inline = False)
                embed.set_image(url = critter_list[6])
            await ctx.send(embed = embed)
        else:
            await ctx.send(f"Sorry, {critter_name} is not a valid critter name\nPlease try using the `bug` or `fish` commands to check your spelling")

def setup(bot):
    bot.add_cog(Search(bot))
