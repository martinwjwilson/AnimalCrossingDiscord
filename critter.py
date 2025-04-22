# IMPORTS
from hemisphere import Hemisphere


class Critter:
    def __init__(self, name, species, location, size, value, start_time, end_time, alt_start_time, alt_end_time, start_month, end_month, alt_start_month, alt_end_month, image_url):
        self.name = name
        self.species = species
        self.location = location
        self.size = size
        self.value = value
        self.start_time = start_time
        self.end_time = end_time
        self.alt_start_time = alt_start_time
        self.alt_end_time = alt_end_time
        self.start_month = start_month
        self.end_month = end_month
        self.alt_start_month = alt_start_month
        self.alt_end_month = alt_end_month
        self.image_url = image_url

    def get_critter_time_period(self):
        print(self.start_month)

    def is_arriving(self, current_hemisphere: Hemisphere) -> bool:
        """
        Check if the critter is arriving based on a given hemisphere
        """
        if self.availability_changing([self.start_month, self.alt_start_month], current_hemisphere):
            return True
        else:
            return False

    def is_leaving(self, current_hemisphere: Hemisphere) -> bool:
        """
        Check if a critter is leaving based on a given hemisphere
        """
        if self.availability_changing([self.end_month, self.alt_end_month], current_hemisphere):
            return True
        else:
            return False

    @staticmethod
    def availability_changing(months_to_check: [str], current_hemisphere: Hemisphere) -> bool:
        """
        Takes a list of months and checks if any match the current month based on the hemisphere
        """
        current_month_name = Hemisphere.calculate_current_month(current_hemisphere)
        for month in months_to_check:
            if month == current_month_name:
                return True
        return False
