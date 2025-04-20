from datetime import datetime
from dateutil.relativedelta import relativedelta
import utils
import sqlite3
import typing

from critter import Critter
from hemisphere import Hemisphere

# db
conn = sqlite3.connect("ailurus.db")
c = conn.cursor()


class Search(commands.Cog):
    @staticmethod
    def format_input(input_string: str) -> str:
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

    @staticmethod
    def availability_review(critter: Critter):
        """
        Check the availability for an individual critter
        """
        # check if the critter is available all year
        if critter.start_month == "All Year":
            return True
        # get the current month
        current_month = Hemisphere.calculate_current_month(Hemisphere.NORTH)
        # check the current month against the start months
        if critter.start_month == current_month or critter.alt_start_month == current_month:
            return True
        # check if the current month is within the start and end months
        temp_month = datetime.strptime(critter.start_month, '%B')
        while temp_month.strftime("%B") != critter.end_month:
            temp_month = temp_month + relativedelta(months=1)
            if temp_month.strftime("%B") == current_month:
                return True
        # check if the current month is withing the alternate start and end months
        if critter.alt_end_month != "None":
            temp_month = datetime.strptime(critter.alt_start_month, '%B')
            while temp_month.strftime("%B") != critter.alt_end_month:
                temp_month = temp_month + relativedelta(months=1)
                if temp_month.strftime("%B") == current_month:
                    return True
        return False

    @staticmethod
    def this_month_critter_filter(self, list_of_critters: [Critter]) -> [Critter]:
        """
        filters list of critters to ones available this month
        """
        critters_available_list = []  # list of critters available this month
        # check each critter against the current date
        for critter in list_of_critters:
            if await self.availability_review(critter):
                critters_available_list.append(critter)
        return critters_available_list

    def month(self, ctx):
        """
        Get a list of all fish and bugs available this month
        """
        # get all fish
        c.execute(utils.search_all_critters("Fish", ""))  # Execute the SQL check
        fish_list = await self.create_critter_list(list(c.fetchall()))
        # get all bugs
        c.execute(utils.search_all_critters("Bug", ""))  # Execute the SQL check
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

    @staticmethod
    def critter_fits_change_check(critter: Critter, change_type: str, hemisphere: Hemisphere) -> bool:
        """
        Check if a critter follows the change being checked against
        Return a bool representing if the critter does or doesn't follow the change
        e.g. a critter leaves in June and the check is for all critters leaving in June. Return True
        """
        # check if the current month matches the critter availability
        if change_type == "arriving" and critter.is_arriving(hemisphere):
            return True
        elif change_type == "leaving" and critter.is_leaving(hemisphere):
            print(critter.name)
            return True
        else:
            return False

    def critter_filter_by_changing(self, list_of_critters: [Critter], change_type: str,
                                         hemisphere: Hemisphere) -> [Critter]:
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
    def list_of_critter_changing(self, species: str, change_type: str, hemisphere: Hemisphere) -> [Critter]:
        """
        Formats and returns a list of all critters of a given species leaving or arriving
        """
        # get the full list of critters of the specified species
        c.execute(utils.search_all_critters(species, ""))
        all_critter_list = await self.create_critter_list(list(c.fetchall()))
        # filter the list to only show changing critters
        critters_available_list = await self.critter_filter_by_changing(all_critter_list, change_type, hemisphere)
        return critters_available_list

    @staticmethod
    def display_list_of_changing_critters(self, ctx, critter_type, change_type: str, hemisphere: Hemisphere):
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

    def arriving(self, ctx, user_hemisphere: typing.Optional[str] = "n"):
        """
        Display a list of all fish and bugs arriving in the current month
        """
        # Convert the user input to work out which hemisphere is being checked
        clean_user_hemisphere = user_hemisphere.strip().lower()
        hemisphere = Hemisphere.convert_text_to_hemisphere(clean_user_hemisphere)
        # Display lists of the critters arriving
        # fish
        await self.display_list_of_changing_critters(self, ctx, "Fish", "arriving", hemisphere)
        # bugs
        await self.display_list_of_changing_critters(self, ctx, "Bug", "arriving", hemisphere)

    def leaving(self, ctx, user_hemisphere: typing.Optional[str] = "n"):
        """
        Display a list of all fish and bugs leaving in the current month
        """
        # Convert the user input to work out which hemisphere is being checked
        clean_user_hemisphere = user_hemisphere.strip().lower()
        hemisphere = Hemisphere.convert_text_to_hemisphere(clean_user_hemisphere)
        # Display lists of the critters arriving
        # fish
        await self.display_list_of_changing_critters(self, ctx, "Fish", "leaving", hemisphere)
        # bugs
        await self.display_list_of_changing_critters(self, ctx, "Bug", "leaving", hemisphere)

    def all_critter_by_species(self, species_type: str, starts_with: str) -> [Critter]:
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
    def critter_list_to_string_of_names(critter_list: [Critter]) -> str:
        critter_names = ""
        for critter in critter_list:
            critter_names = critter_names + f"{critter.name}\n"
        return critter_names

    @staticmethod
    def create_critter(critter: list) -> Critter:
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
    def create_critter_list(critter_list: list) -> [Critter]:
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

    def fish(self, ctx, starts_with: typing.Optional[str] = ""):
        """
        Display a list of all fish by name
        If input is provided then find names beginning with the input
        """
        fish_list = await self.all_critter_by_species("Fish", starts_with)  # get a list of all fish
        fish_names = await self.critter_list_to_string_of_names(fish_list)  # convert fish to list of their names
        embed = disnake.Embed(title="Fish search", description=fish_names)
        await ctx.send(embed=embed)

    def bug(self, ctx, starts_with: typing.Optional[str] = ""):
        """
        Display a list of all bugs by name
        If input is provided then find names beginning with the input
        """
        bug_list = await self.all_critter_by_species("Bug", starts_with)  # get a list of all bug names
        bug_names = await self.critter_list_to_string_of_names(bug_list)
        embed = disnake.Embed(title="Bug search", description=bug_names)
        await ctx.send(embed=embed)

    def s(self, ctx, *, critter_name: str):
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
