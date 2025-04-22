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


class Search:
    def month(self):
        """
        Get a list of all fish and bugs available this month
        """
        # get all fish
        c.execute(utils.search_all_critters("Fish"))
        fish_list = self._create_critter_list(list(c.fetchall()))
        # get all bugs
        c.execute(utils.search_all_critters("Bug"))
        bug_list = self._create_critter_list(list(c.fetchall()))
        # get a list of all fish available this month
        fish_available_list = self._this_month_critter_filter(fish_list)
        fish_available_names = self._critter_list_to_string_of_names(fish_available_list)
        # get a list of all bugs available this month
        bug_available_list = self._this_month_critter_filter(bug_list)
        bugs_available_names = self._critter_list_to_string_of_names(bug_available_list)
        print(fish_available_names)
        print(bugs_available_names)

    def arriving(self, user_hemisphere: typing.Optional[str] = "n"):
        """
        Display a list of all fish and bugs arriving in the current month
        """
        # Convert the user input to work out which hemisphere is being checked
        clean_user_hemisphere = user_hemisphere.strip().lower()
        hemisphere = Hemisphere.convert_to_hemisphere(clean_user_hemisphere)
        # Display lists of the critters arriving
        self._display_list_of_changing_critters(self, "Fish", "arriving", hemisphere)
        self._display_list_of_changing_critters(self, "Bug", "arriving", hemisphere)

    def leaving(self, user_hemisphere: typing.Optional[str] = "n"):
        """
        Display a list of all fish and bugs leaving in the current month
        """
        # Convert the user input to work out which hemisphere is being checked
        clean_user_hemisphere = user_hemisphere.strip().lower()
        hemisphere = Hemisphere.convert_to_hemisphere(clean_user_hemisphere)
        # Display lists of the critters arriving
        self._display_list_of_changing_critters(self, "Fish", "leaving", hemisphere)
        self._display_list_of_changing_critters(self, "Bug", "leaving", hemisphere)

    def fish(self, starts_with: typing.Optional[str] = ""):
        """
        Display a list of all fish by name
        If input is provided then find names beginning with the input
        """
        fish_list = self._all_critter_by_species("Fish", starts_with)
        fish_names = self._critter_list_to_string_of_names(fish_list)
        print(f"Fish Search: \n{fish_names}")

    def bug(self, starts_with: typing.Optional[str] = ""):
        """
        Display a list of all bugs by name
        If input is provided then find names beginning with the input
        """
        bug_list = self._all_critter_by_species("Bug", starts_with)
        bug_names = self._critter_list_to_string_of_names(bug_list)
        print(f"Bug Search: \n{bug_names}")

    def s(self, critter_name: str):
        """
        Search for a critter by name and display all of its information
        """
        critter_name = self._format_input(critter_name)  # alter the user input to match the db format
        # Check the critter table to see if any of the critter names match the user input
        c.execute(utils.check_for_critter(critter_name))
        try:
            critter = self._create_critter(list(c.fetchone()))
            print(f"{critter.name} Info\n"
                  f"Everything you need to know about the {critter.name}")
            print(f"Name: {critter.name}")
            print(f"Type: {critter.species}")
            print(f"Location: {critter.location}")
            if critter.species == 'Fish':
                print(f"Size: {critter.size}")
            print(f"Value: {critter.value}")
            print(f"Time: {critter.start_time} - {critter.end_time}")
            print(f"Month: {critter.start_month} - {critter.end_month}\n")
        except Exception:
            print(f"Sorry, {critter_name} is not a valid critter name\n"
                  f"Please try using the 'bug' or 'fish' commands to check your spelling against the listed species\n")

    # PRIVATE

    @staticmethod
    def _format_input(input_string: str) -> str:
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

    def _list_of_critter_changing(self, species: str, change_type: str, hemisphere: Hemisphere) -> [Critter]:
        """
        Formats and returns a list of all critters of a given species leaving or arriving
        """
        # get the full list of critters of the specified species
        c.execute(utils.search_all_critters(species, ""))
        all_critter_list = self._create_critter_list(list(c.fetchall()))
        # filter the list to only show changing critters
        critters_available_list = self._critter_filter_by_changing(all_critter_list, change_type, hemisphere)
        return critters_available_list

    @staticmethod
    def _availability_review(critter: Critter):
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

    def _this_month_critter_filter(self, list_of_critters: [Critter]) -> [Critter]:
        """
        filters list of critters to ones available this month
        """
        critters_available_list = []  # list of critters available this month
        # check each critter against the current date
        for critter in list_of_critters:
            if self._availability_review(critter):
                critters_available_list.append(critter)
        return critters_available_list

    @staticmethod
    def _critter_fits_change_check(critter: Critter, change_type: str, hemisphere: Hemisphere) -> bool:
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

    def _critter_filter_by_changing(self, list_of_critters: [Critter], change_type: str,
                                    hemisphere: Hemisphere) -> [Critter]:
        """
        Filters list of all bugs and fish to ones arriving or leaving this month
        """
        critters_available_list = []
        # check each critter against the current date
        for critter in list_of_critters:
            if self._critter_fits_change_check(critter, change_type, hemisphere):
                critters_available_list.append(critter)
        return critters_available_list

    @staticmethod
    def _display_list_of_changing_critters(self, critter_type, change_type: str, hemisphere: Hemisphere):
        """
        Displays lists of all critters of the specified type that are arriving or leaving
        """
        # get a list of all critters
        all_critters_list = self._list_of_critter_changing(critter_type, change_type, hemisphere)
        # get a list of all critter names as strings
        all_critters_string = self._critter_list_to_string_of_names(all_critters_list)
        print(f"List of {critter_type} {change_type} this month: \n{all_critters_string}")

    def _all_critter_by_species(self, species_type: str, starts_with: str) -> [Critter]:
        """
        Get a list from the database of all critters of a given species
        Restrict the search to names starting with the 'starts_with' variable if provided
        """
        # check if the search should be restricted
        if starts_with != "":
            starts_with = self._format_input(starts_with)  # format the input
            starts_with = f"AND critter_name LIKE '{starts_with}%'"  # add sql for search
        c.execute(utils.search_all_critters(species_type, starts_with))  # Execute the SQL check
        critter_list = self._create_critter_list(list(c.fetchall()))
        return critter_list

    @staticmethod
    def _critter_list_to_string_of_names(critter_list: [Critter]) -> str:
        critter_names = ""
        for critter in critter_list:
            critter_names = critter_names + f"{critter.name}\n"
        return critter_names

    @staticmethod
    def _create_critter(critter: list) -> Critter:
        # https://www.reddit.com/r/learnpython/comments/pg9yv7/how_to_turn_json_into_objects_in_python/
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
    def _create_critter_list(critter_list: list) -> [Critter]:
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
