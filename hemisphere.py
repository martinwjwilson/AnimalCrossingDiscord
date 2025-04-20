# Imports
from enum import Enum
import datetime
from dateutil.relativedelta import relativedelta


class Hemisphere(Enum):
    NORTH = "north"
    SOUTH = "south"

    def calculate_current_month(self) -> str:
        if self == self.NORTH:
            return datetime.datetime.now().strftime("%B")
        else:
            return (datetime.datetime.now() + relativedelta(months=6)).strftime("%B")

    @staticmethod
    def convert_to_hemisphere(raw_hemisphere: str):
        """
        param raw_hemisphere: Example input = 'north'
        """
        if raw_hemisphere == Hemisphere.SOUTH.value:
            return Hemisphere.SOUTH
        else:
            return Hemisphere.NORTH
