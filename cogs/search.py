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
            # print("THIS 1")
            for month in dict_of_all_months:
                if dict_of_all_months[month] >= start_month_int and dict_of_all_months[month] <= end_month_int:
                    list_of_months_available.append(month)
        # if end month is less than start month, include everything greater or equal to start month and less than or = end month
        else:
            # print("THIS 2")
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
        # print(f"Current month is: {current_month}")
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
        critters_availble_list = [] # list of critters available this month
        # check each critter against the current date
        for critter in list_of_critters:
            # check if the critter is a fish or a bug
            if critter[1] == "Fish":
                # check availability this month
                if await self.availability_review(critter[6]):
                    critters_availble_list.append(critter[0])
            else:
                # check availability this month
                if await self.availability_review(critter[5]):
                    critters_availble_list.append(critter[0])
        return critters_availble_list

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
        critters_availble_list = await self.this_month_critter_filter(fish_list)
        print("This is a list of all the fish available this month...")
        for critter in critters_availble_list:
            description_f = description_f + f"\n{critter}"
        # get a list of all bugs available this month
        critters_availble_list = await self.this_month_critter_filter(bug_list)
        print("This is a list of all the bugs available this month...")
        for critter in critters_availble_list:
            description_b = description_b + f"\n{critter}"

        embed_f = discord.Embed(title = "List of Fish available this month", description = description_f)
        embed_b = discord.Embed(title = "List of Bugs available this month", description = description_b)
        await ctx.send(embed = embed_f)
        await ctx.send(embed = embed_b)

    async def final_month_check(self, critter_month: str):
        """
        Check the if this is the last month available for a critter
        """
        # get this months month
        current_month = date.today().strftime("%B")
        # print(f"Current month is: {current_month}")
        northern_months = critter_month.split("/")[0] # split the critter month into Northern and Southern
        northern_months = northern_months.split("(")[0].strip() # remove the (northern) section
        if "," in northern_months: # if critter is available twice a year, split it up
            periods = northern_months.split(",")
            period_1 = periods[0]
            period_2 = periods[1]
            # get start and end months from each period
            period_1 = period_1.split("-")
            end_month_1 = period_1[1].strip()
            if "-" in period_2:
                period_2 = period_2.split("-")
            else: # if it's a ladybug... :v
                period_2 = [period_2, period_2]
            end_month_2 = period_2[1].strip()
            if((current_month == end_month_1) or (current_month == end_month_2)):
                return True
        elif "-" in northern_months: # there is one period per year
            # get start and end months
            start_month, end_month = northern_months.split("-")
            # generate a list of months critter is available
            if current_month == end_month:
                return True
        else: # it is available for a single month per year
            if current_month == northern_months:
                return True
        return False

    async def final_month_critter_filter(self, list_of_critters: list):
        """
        Filters list of all bugs and fish to ones leaving this month
        """
        critters_availble_list = [] # list of critters available this month
        # check each critter against the current date
        for critter in list_of_critters:
            # check if the critter is a fish or a bug
            if critter[1] == "Fish":
                # check availability this month
                if await self.final_month_check(critter[6]):
                    critters_availble_list.append(critter[0])
            else:
                # check availability this month
                if await self.final_month_check(critter[5]):
                    critters_availble_list.append(critter[0])
        return critters_availble_list

    @commands.command()
    async def leaving(self, ctx):
        """
        Get a list of all fish and bugs leaving at the end of the current month
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
        critters_availble_list = await self.final_month_critter_filter(fish_list)
        print("This is a list of all the fish available this month...")
        for critter in critters_availble_list:
            description_f = description_f + f"\n{critter}"
        # get a list of all bugs available this month
        critters_availble_list = await self.final_month_critter_filter(bug_list)
        print("This is a list of all the bugs available this month...")
        for critter in critters_availble_list:
            description_b = description_b + f"\n{critter}"
        embed_f = discord.Embed(title = "List of Fish leaving this month", description = description_f)
        embed_b = discord.Embed(title = "List of Bugs leaving this month", description = description_b)
        await ctx.send(embed = embed_f)
        await ctx.send(embed = embed_b)

    async def first_month_check(self, critter_month: str):
        """
        Check the if this is the first month available for a critter
        """
        # get this months month
        current_month = date.today().strftime("%B")
        # print(f"Current month is: {current_month}")
        northern_months = critter_month.split("/")[0] # split the critter month into Northern and Southern
        northern_months = northern_months.split("(")[0].strip() # remove the (northern) section
        print(f"\nCritter months: {northern_months}")
        if "," in northern_months: # if critter is available twice a year, split it up
            periods = northern_months.split(",")
            period_1 = periods[0]
            period_2 = periods[1]
            # get start and end months from each period
            period_1 = period_1.split("-")
            start_month_1 = period_1[0].strip()
            if "-" in period_2:
                period_2 = period_2.split("-")
            else: # if it's a ladybug... :v
                period_2 = [period_2, period_2]
            start_month_2 = period_2[0].strip()
            if((current_month == start_month_1) or (current_month == start_month_2)):
                return True
        elif "-" in northern_months: # there is one period per year
            # get start and end months
            start_month, end_month = northern_months.split("-")
            # generate a list of months critter is available
            if current_month == start_month:
                return True
        else: # it is available for a single month per year
            if current_month == northern_months:
                return True
        return False

    async def first_month_critter_filter(self, list_of_critters: list):
        """
        Filters list of all bugs and fish to ones leaving this month
        """
        critters_availble_list = [] # list of critters available this month
        # check each critter against the current date
        for critter in list_of_critters:
            # check if the critter is a fish or a bug
            if critter[1] == "Fish":
                # check availability this month
                if await self.first_month_check(critter[6]):
                    critters_availble_list.append(critter[0])
            else:
                # check availability this month
                if await self.first_month_check(critter[5]):
                    critters_availble_list.append(critter[0])
        return critters_availble_list

    @commands.command()
    async def new(self, ctx):
        """
        Get a list of all fish and bugs arriving this month
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
        critters_availble_list = await self.first_month_critter_filter(fish_list)
        print("This is a list of all the fish available this month...")
        for critter in critters_availble_list:
            description_f = description_f + f"\n{critter}"
        # get a list of all bugs available this month
        critters_availble_list = await self.first_month_critter_filter(bug_list)
        print("This is a list of all the bugs available this month...")
        for critter in critters_availble_list:
            description_b = description_b + f"\n{critter}"
        embed_f = discord.Embed(title = "List of Fish arriving this month", description = description_f)
        embed_b = discord.Embed(title = "List of Bugs arriving this month", description = description_b)
        await ctx.send(embed = embed_f)
        await ctx.send(embed = embed_b)

    async def all_critter_by_species(self, species_type: str, starts_with: str):
        """
        Get a list from the database of all critters of a given species
        Restrict the search to names starting with the 'starts_with' variable if provided
        """
        # check if the search should be restricted
        if starts_with != "":
            starts_with = utils.format_input(starts_with) # format the input
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
        critter_name = utils.format_input(critter_name) # format the input
        # Check both fish and bug tables
        c.execute(utils.check_for_critter("fish", critter_name))
        try:
            fish_list = list(c.fetchone())
        except Exception as e:
            pass
        c.execute(utils.check_for_critter("bugs", critter_name))
        try:
            bug_list = list(c.fetchone())
        except Exception as e:
            pass
        # check which one returned a value if any
        critter_list = False
        try:
            print(fish_list)
            critter_list = fish_list
        except Exception as e:
            pass
        try:
            critter_list = bug_list
            print(bug_list)
        except Exception as e:
            pass
        # if there is a match from the DB
        if critter_list:
            # create embed
            embed = discord.Embed(title = f'{critter_list[1]} Info', description = f"Everything you need to know about the {critter_list[0]}")
            embed.add_field(name = "Name:", value = critter_list[0], inline = False)
            embed.add_field(name = "Type:", value = critter_list[1], inline = False)
            embed.add_field(name = "Location:", value = critter_list[2], inline = False)
            if len(critter_list) == 7:
                embed.add_field(name = "Size:", value = critter_list[3], inline = False)
                embed.add_field(name = "Value:", value = critter_list[4], inline = False)
                embed.add_field(name = "Time:", value = critter_list[5], inline = False)
                embed.add_field(name = "Month:", value = critter_list[6], inline = False)
            else:
                embed.add_field(name = "Value:", value = critter_list[3], inline = False)
                embed.add_field(name = "Time:", value = critter_list[4], inline = False)
                embed.add_field(name = "Month:", value = critter_list[5], inline = False)
            await ctx.send(embed = embed)
        else:
            await ctx.send(f"Sorry, {critter_name} is not a valid critter name")
            # embed = discord.Embed(title = f'Good job !', description = f"{critter_name} was not in the Critterpedia")
            # embed.set_image(url = 'https://en.meming.world/images/en/thumb/3/3f/Professional_Retard.jpg/300px-Professional_Retard.jpg')
            # await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Search(bot))
