import disnake
from disnake.ext import commands
import utils
import sqlite3
import typing

from critter import Critter
from hemisphere import Hemisphere

# db
conn = sqlite3.connect("ailurus.db")
c = conn.cursor()


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    dictionary_of_all_months = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12}

    @staticmethod
    async def format_input(input_string: str) -> str:
        """
        Format a string to match the style of the db entries
        """
        str_input = "".join(input_string)  # join arguments together
        # fix casing
        word_list = str_input.lower().split(" ")  # make the string lowercase then split each word by space
        output = []
        for word in word_list:
            output.append(word.capitalize())  # capitalise all lowercase words in list
        return " ".join(output)  # join words back together with a space between them

    async def month_list(self, start_month: str, end_month: str):
        """
        Return a list of months from the start month until the end month
        """
        dict_of_all_months = {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12}
        start_month_int = dict_of_all_months[start_month]  # 'November'
        end_month_int = dict_of_all_months[end_month]

    #     list_of_months_available = []
    #     # if start month is less than end month, include everything greater than start month and less than or = end month
    #     if start_month_int < end_month_int:
    #         for month in dict_of_all_months:
    #             if dict_of_all_months[month] >= start_month_int and dict_of_all_months[month] <= end_month_int:
    #                 list_of_months_available.append(month)
    #     # if end month is less than start month, include everything greater or equal to start month and less than or = end month
    #     else:
    #         for month in dict_of_all_months:
    #             if dict_of_all_months[month] >= start_month_int or dict_of_all_months[month] <= end_month_int:
    #                 list_of_months_available.append(month)
    #     # check if current month is in list
    #     return list_of_months_available

    @staticmethod
    async def availability_review(self, critter_month: str):
        """
        Check the availability for an individual critter
        """
        # check if the critter is all year round
        if critter_month.startswith("Year"):
            return True
        #     # get this months month
        #     current_month = date.today().strftime("%B")
        #     northern_months = critter_month.split("/")[0] # split the critter month into Northern and Southern
        #     northern_months = northern_months.split("(")[0].strip() # remove the (northern) section
        #
        #     if "," in northern_months: # if critter is available twice a year, split it up
        #         periods = northern_months.split(",")
        #         period_1 = periods[0]
        #         period_2 = periods[1]
        #         # get start and end months from each period
        #         period_1 = period_1.split("-")
        #         start_month_1 = period_1[0].strip()
        #         end_month_1 = period_1[1].strip()
        #         if "-" in period_2:
        #             period_2 = period_2.split("-")
        #         else: # if it's a ladybug... :v
        #             period_2 = [period_2, period_2]
        #         start_month_2 = period_2[0].strip()
        #         end_month_2 = period_2[1].strip()
        #         if (current_month in await self.month_list(start_month_1, end_month_1)) or (current_month in await self.month_list(start_month_2.strip(), end_month_2)):
        #             return True
        #     elif "-" in northern_months: # there is one period per year
        #         # get start and end months
        #         start_month, end_month = northern_months.split("-")
        #         # generate a list of months critter is available
        #         if current_month in await self.month_list(start_month, end_month):
        #             return True
        #     else: # it is available for a single month per year
        #         if current_month == northern_months:
        #             return True
        return False

    @staticmethod
    async def this_month_critter_filter(self, list_of_critters: [Critter]) -> [Critter]:
        """
        filters list of critters to ones available this month
        """
        critters_available_list = []  # list of critters available this month
        # check each critter against the current date
        for critter in list_of_critters:
            if await self.availability_review(critter):
                critters_available_list.append(critter)
        return critters_available_list

    @commands.command()
    async def month(self, ctx):
        """
        Get a list of all fish and bugs available this month
        """
        # get all fish
        c.execute(utils.search_all_critters("Fish", ""))  # Execute the SQL check
        fish_list = await self.create_critter_list(list(c.fetchall()))
        # get all bugs
        c.execute(utils.search_all_critters("Bugs", ""))  # Execute the SQL check
        bug_list = await self.create_critter_list(list(c.fetchall()))
        # get a list of all fish available this month
        fish_available_list = await self.this_month_critter_filter(self, fish_list)
        description_f = await self.critter_list_to_string_of_names(fish_available_list)
        # get a list of all bugs available this month
        bug_available_list = await self.this_month_critter_filter(self, bug_list)
        description_b = await self.critter_list_to_string_of_names(bug_available_list)
        # create embeds
        embed_f = disnake.Embed(title="List of Fish available this month", description=description_f)
        embed_b = disnake.Embed(title="List of Bugs available this month", description=description_b)
        await ctx.send(embed=embed_f)
        await ctx.send(embed=embed_b)

    # async def critter_available_twice_per_year(self, current_month: str, critter_months: str, change_type: str) -> bool:
    #     periods = critter_months.split(",")
    #     period_1 = periods[0]
    #     period_2 = periods[1]
    #     if((await self.critter_available_once_per_year(current_month, period_1, change_type)) or (await self.critter_available_once_per_year(current_month, period_2, change_type))):
    #         return True
    #     else:
    #         return False

    # async def critter_available_once_per_year(self, current_month: str, critter_months: str, change_type: str) -> bool:
    #     # get start and end months
    #     start_month, end_month = critter_months.split("-")
    #     # check change type
    #     if change_type == "arriving":
    #         if current_month == start_month:
    #             return True
    #         else:
    #             return False
    #     elif change_type == "leaving":
    #         if current_month == end_month:
    #             return True
    #         else:
    #             return False

    async def critter_fits_change_check(self, critter: Critter, change_type: str, hemisphere: Hemisphere) -> bool:
        """
        Check if a critter follows the change being checked against
        Return a bool representing if the critter does or doesn't follow the change
        e.g. a critter leaves in June and the check is for all critters leaving in June. Return True
        """
        # check if the current month matches the critter availability
        if change_type == "arriving" and critter.is_arriving(hemisphere):
            return True
        elif change_type == "leaving" and critter.is_leaving(hemisphere):
            return True
        else:
            return False

    async def critter_filter_by_changing(self, list_of_critters: [Critter], change_type: str, hemisphere: Hemisphere) -> [
        Critter]:
        """
        Filters list of all bugs and fish to ones arriving or leaving this month
        """
        critters_available_list = []  # list of critters available this month
        # check each critter against the current date
        for critter in list_of_critters:
            if await self.critter_fits_change_check(critter, change_type, hemisphere):
                critters_available_list.append(critter)
        return critters_available_list

    @staticmethod
    async def list_of_critter_changing(self, species: str, change_type: str, hemisphere: Hemisphere) -> [Critter]:
        """
        Formats and returns a list of all critters of a given species leaving or arriving depending on the command called
        """
        # get the full list of critters of the specified species
        c.execute(utils.search_all_critters(species, ""))
        all_critter_list = await self.create_critter_list(list(c.fetchall()))
        # filter the list to only show changing critters
        critters_available_list = await self.critter_filter_by_changing(all_critter_list, change_type, hemisphere)
        return critters_available_list

    @staticmethod
    async def display_list_of_changing_critters(self, ctx, critter_type, change_type: str, hemisphere: Hemisphere):
        """
        Displays lists of all critters of the specified type that are arriving or leaving
        """
        # get a list of all critters
        all_critters_list = await self.list_of_critter_changing(self, critter_type, change_type, hemisphere)
        # get a list of all critter names as strings
        all_critters_string = await self.critter_list_to_string_of_names(all_critters_list)
        # create embeds
        embed = disnake.Embed(title=f"List of {critter_type} {change_type} this month",
                              description=all_critters_string)
        # send embed
        await ctx.send(embed=embed)

    @commands.command()
    async def arriving(self, ctx, user_hemisphere: typing.Optional[str] = "n"):
        """
        Display a list of all fish and bugs arriving in the current month
        """
        # Convert the user input to work out which hemisphere is being checked
        hemisphere = Hemisphere.convert_text_to_hemisphere(user_hemisphere)
        # Display lists of the critters arriving
        # fish
        await self.display_list_of_changing_critters(self, ctx, "Fish", "arriving", hemisphere)
        # bugs
        await self.display_list_of_changing_critters(self, ctx, "Bug", "arriving", hemisphere)

    @commands.command()
    async def leaving(self, ctx, user_hemisphere: typing.Optional[str] = "n"):
        """
        Display a list of all fish and bugs leaving in the current month
        """
        # Convert the user input to work out which hemisphere is being checked
        hemisphere = Hemisphere.convert_text_to_hemisphere(user_hemisphere)
        # Display lists of the critters arriving
        # fish
        await self.display_list_of_changing_critters(self, ctx, "Fish", "leaving", hemisphere)
        # bugs
        await self.display_list_of_changing_critters(self, ctx, "Bug", "leaving", hemisphere)

    async def all_critter_by_species(self, species_type: str, starts_with: str) -> [Critter]:
        """
        Get a list from the database of all critters of a given species
        Restrict the search to names starting with the 'starts_with' variable if provided
        """
        # check if the search should be restricted
        if starts_with != "":
            starts_with = await self.format_input(starts_with)  # format the input
            starts_with = f"AND critter_name LIKE '{starts_with}%'"  # add sql for search
        c.execute(utils.search_all_critters(species_type, starts_with))  # Execute the SQL check
        critter_list = await self.create_critter_list(list(c.fetchall()))
        return critter_list

    @staticmethod
    async def critter_list_to_string_of_names(critter_list: [Critter]) -> str:
        critter_names = ""
        for critter in critter_list:
            critter_names = critter_names + f"{critter.name}\n"
        return critter_names

    @staticmethod
    async def create_critter(critter: list) -> Critter:
        return Critter(
            name=critter[0],
            species=critter[1],
            location=critter[2],
            size=critter[3],
            value=critter[4],
            start_time=critter[5],
            end_time=critter[6],
            alt_start_time=critter[7],
            alt_end_time=critter[8],
            start_month=critter[9],
            end_month=critter[10],
            alt_start_month=critter[11],
            alt_end_month=critter[12],
            image_url=critter[13]
        )

    @staticmethod
    async def create_critter_list(critter_list: list) -> [Critter]:
        critter_class_list = []
        for critter in critter_list:
            critter_class_list.append(Critter(
                name=critter[0],
                species=critter[1],
                location=critter[2],
                size=critter[3],
                value=critter[4],
                start_time=critter[5],
                end_time=critter[6],
                alt_start_time=critter[7],
                alt_end_time=critter[8],
                start_month=critter[9],
                end_month=critter[10],
                alt_start_month=critter[11],
                alt_end_month=critter[12],
                image_url=critter[13]
            ))
        return critter_class_list

    @commands.command()
    async def fish(self, ctx, starts_with: typing.Optional[str] = ""):
        """
        Display a list of all fish by name
        If input is provided then find names beginning with the input
        """
        fish_list = await self.all_critter_by_species("Fish", starts_with)  # get a list of all fish
        fish_names = await self.critter_list_to_string_of_names(fish_list)  # convert fish to list of their names
        embed = disnake.Embed(title="Fish search", description=fish_names)
        await ctx.send(embed=embed)

    @commands.command()
    async def bug(self, ctx, starts_with: typing.Optional[str] = ""):
        """
        Display a list of all bugs by name
        If input is provided then find names beginning with the input
        """
        bug_list = await self.all_critter_by_species("Bug", starts_with)  # get a list of all bug names
        bug_names = await self.critter_list_to_string_of_names(bug_list)
        embed = disnake.Embed(title="Bug search", description=bug_names)
        await ctx.send(embed=embed)

    @commands.command()
    async def s(self, ctx, *, critter_name: str):
        """
        Search for a critter by name and display all of its information
        """
        critter_name = await self.format_input(critter_name)  # alter the user input to match the db format
        # Check the critter table to see if any of the critter names match the user input
        c.execute(utils.check_for_critter(critter_name))
        try:
            critter = await self.create_critter(list(c.fetchone()))
            # create embed
            embed = disnake.Embed(title=f'{critter.name} Info',
                                  description=f"Everything you need to know about the {critter.name}")
            embed.add_field(name="Name:", value=critter.name, inline=False)
            embed.add_field(name="Type:", value=critter.species, inline=False)
            embed.add_field(name="Location:", value=critter.location, inline=False)
            if critter.species == 'Fish':  # if critter was a fish
                embed.add_field(name="Size:", value=critter.size, inline=False)
            embed.add_field(name="Value:", value=critter.value, inline=False)
            embed.add_field(name="Time:", value=f"{critter.start_time} - {critter.end_time}", inline=False)
            embed.add_field(name="Month:", value=f"{critter.start_month} - {critter.end_month}", inline=False)
            embed.set_image(url=critter.image_url)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(
                f"Sorry, {critter_name} is not a valid critter name\nPlease try using the `bug` or `fish` "
                f"commands to check your spelling against the listed species")


def setup(bot):
    bot.add_cog(Search(bot))
